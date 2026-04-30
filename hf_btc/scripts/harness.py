#!/usr/bin/env python3
"""Bull-HF-BTC harness — orchestrates each 5-min tick.

Sub-commands (called by run_loop.sh in order):

    prepare              build /tmp/hf_prompt.md + /tmp/hf_context.json
    post                 parse /tmp/hf_decision_envelope.json (claude output),
                         validate, execute in sim, check TP/SL hits on opens,
                         mark-to-market, telegram (anti-spam gated), git commit.
    sleep_until_next     align to next 5-min boundary UTC.
    tick_dry             prepare + fake HOLD decision + post (no claude call) — for testing.
    daily                end-of-day stats report (call at 23:55 UTC).
"""

from __future__ import annotations

import json
import math
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent  # hf_btc/
REPO = ROOT.parent  # thashi-ai/
sys.path.insert(0, str(HERE))

import btc_data  # noqa: E402
import chart_img_client  # noqa: E402
import sim_portfolio  # noqa: E402
import stats  # noqa: E402
import telegram_hf  # noqa: E402
import trade_tracker  # noqa: E402

STATE_DIR = ROOT / "state"
PROMPT_FILE = Path("/tmp/hf_prompt.md")
CONTEXT_FILE = Path("/tmp/hf_context.json")
ENVELOPE_FILE = Path("/tmp/hf_decision_envelope.json")
DECISION_FILE = Path("/tmp/hf_decision.json")
LAST_NOTIF_FILE = STATE_DIR / "last_notif.json"
RUNS_FILE = STATE_DIR / "runs.jsonl"

# Guardrails (immutable in code, the LLM cannot widen them)
SIZING_MIN_PCT = 2.0
SIZING_MAX_PCT = 12.0
RR_FLOOR = 1.3
COOLDOWN_MIN = 15
DAILY_LOSS_CAP_PCT = -3.0
MAX_OPEN = 1

# Heartbeat & anti-spam
HEARTBEAT_QUIET_MIN = 10  # if a trade-event was sent in last 10min, skip heartbeat
DAILY_REPORT_HOUR_UTC = 23
DAILY_REPORT_MIN_UTC = 55


def _utc() -> datetime:
    return datetime.now(timezone.utc)


def _iso() -> str:
    return _utc().isoformat()


# ───────── signal score → gates chart-img opportunistic fetch ─────────


def _signal_score(snap: dict[str, Any]) -> tuple[int, list[str]]:
    """Heuristic 0-5: BB squeeze, RSI extreme, MACD cross, volume spike, MA test."""
    score = 0
    reasons: list[str] = []
    tf5 = snap.get("5Min", {})
    bb = tf5.get("bollinger", {})
    bw = bb.get("bandwidth_pct", float("nan"))
    if not math.isnan(bw) and bw < 0.4:
        score += 1
        reasons.append(f"BB squeeze {bw:.2f}%")
    rsi5 = tf5.get("rsi_14", float("nan"))
    if not math.isnan(rsi5) and (rsi5 < 30 or rsi5 > 70):
        score += 1
        reasons.append(f"RSI 5m extreme {rsi5:.0f}")
    macd5 = tf5.get("macd", {})
    h = macd5.get("hist", float("nan"))
    if not math.isnan(h) and abs(h) < 5:
        score += 1
        reasons.append("MACD near cross")
    vz = tf5.get("volume_z20", float("nan"))
    if not math.isnan(vz) and vz > 2:
        score += 1
        reasons.append(f"vol spike z={vz:.1f}")
    d20 = tf5.get("dist_ema20_pct", float("nan"))
    if not math.isnan(d20) and abs(d20) < 0.1:
        score += 1
        reasons.append(f"on EMA20 ({d20:+.2f}%)")
    return score, reasons


def _should_fetch_baseline(now: datetime) -> bool:
    """True if we're in the first 5 minutes after each UTC hour AND haven't fetched baseline this hour yet."""
    if now.minute >= 5:
        return False
    q = chart_img_client._load_quota()
    today = now.strftime("%Y-%m-%d")
    if q.get("date_utc") != today:
        return True
    hour = now.strftime("%H")
    for h in q.get("history", []):
        if h.get("reason") == "baseline" and h.get("ts", "").startswith(today.replace("-", "") + "T" + hour):
            return False
    return True


def _build_chart_path(snap: dict[str, Any]) -> str | None:
    now = _utc()
    if _should_fetch_baseline(now):
        time.sleep(1.1)
        r = chart_img_client.fetch(symbol="BINANCE:BTCUSDT", interval="5m", reason="baseline")
        if r.get("ok"):
            return r["path"]
    score, _ = _signal_score(snap)
    if score >= 2:
        time.sleep(1.1)
        r = chart_img_client.fetch(symbol="BINANCE:BTCUSDT", interval="5m", reason="signal")
        if r.get("ok"):
            return r["path"]
    return None


# ───────── prompt builder ─────────


def _read_recent_trade_log(n: int = 30) -> list[dict[str, Any]]:
    if not (STATE_DIR / "trade_log.jsonl").exists():
        return []
    lines = (STATE_DIR / "trade_log.jsonl").read_text().splitlines()
    return [json.loads(l) for l in lines[-n:] if l.strip()]


def _format_indicator_block(label: str, ind: dict[str, Any]) -> str:
    if "error" in ind:
        return f"### {label}\n_{ind['error']}_\n"
    bb = ind.get("bollinger", {})
    macd = ind.get("macd", {})
    rows = [
        f"**{label}** · last_close=`{ind['last_close']:.2f}` · last_ts=`{ind['last_ts']}`",
        f"- RSI(14)=`{ind['rsi_14']:.1f}` · ATR(14)=`{ind['atr_14']:.2f}` (`{ind['atr_pct']:.2f}%`) · Vol z20=`{ind['volume_z20']:+.2f}`",
        f"- MACD=`{macd['macd']:+.2f}` · sig=`{macd['signal']:+.2f}` · hist=`{macd['hist']:+.2f}`",
        f"- BB(20,2): up=`{bb['upper']:.2f}` mid=`{bb['middle']:.2f}` low=`{bb['lower']:.2f}` · bw=`{bb['bandwidth_pct']:.2f}%` · %B=`{bb['pct_b']:.2f}`",
        f"- EMA20=`{ind['ema_20']:.2f}` (`{ind['dist_ema20_pct']:+.2f}%`) · EMA50=`{ind['ema_50']:.2f}` (`{ind['dist_ema50_pct']:+.2f}%`) · EMA200=`{ind['ema_200']:.2f}` (`{ind['dist_ema200_pct']:+.2f}%`)",
        f"- VWAP(session)=`{ind['vwap_session']:.2f}` (`{ind['dist_vwap_pct']:+.2f}%`)",
    ]
    return "\n".join(rows)


def _build_context() -> dict[str, Any]:
    snap = btc_data.snapshot()
    score, reasons = _signal_score(snap)
    chart_path = _build_chart_path(snap)
    port = sim_portfolio.snapshot()
    log_tail = _read_recent_trade_log(30)
    return {
        "tick_utc": _iso(),
        "snapshot": snap,
        "signal_score": {"score": score, "reasons": reasons},
        "chart_path": chart_path,
        "sim_portfolio": port,
        "recent_log": log_tail,
        "guardrails": {
            "sizing_min_pct": SIZING_MIN_PCT,
            "sizing_max_pct": SIZING_MAX_PCT,
            "rr_floor": RR_FLOOR,
            "cooldown_min": COOLDOWN_MIN,
            "daily_loss_cap_pct": DAILY_LOSS_CAP_PCT,
            "max_open": MAX_OPEN,
        },
    }


def _build_prompt(ctx: dict[str, Any]) -> str:
    snap = ctx["snapshot"]
    port = ctx["sim_portfolio"]
    open_trades = port.get("open_trades", [])
    log_tail = ctx["recent_log"]
    chart_path = ctx.get("chart_path")
    score = ctx["signal_score"]
    quote = snap.get("latest_quote", {}) or {}

    lines = [
        "# Bull-HF-BTC — décision du tick (5-min cadence)",
        "",
        f"**Tick UTC** : `{ctx['tick_utc']}`",
        "**Mission** : décider d'ouvrir LONG/SHORT, fermer une position ouverte, ou HOLD/SKIP. Sim-only ($3000).",
        "",
        "## 1. Récupère 5-10 dernières news BTC",
        "Utilise `WebSearch` (1 appel) avec : `BTC bitcoin news {date} ETF flow funding sentiment`. Filtre la dernière fenêtre 6h. Synthétise en 3-5 puces. Tu DOIS faire ce search avant de décider.",
        "",
        "## 2. Contexte de marché (calculé localement)",
        "",
        f"**Quote** : bid=`{quote.get('bp')}` ask=`{quote.get('ap')}` spread=`{((quote.get('ap',0)-quote.get('bp',0))/quote.get('ap',1)*100 if quote.get('ap') else 0):.3f}%`",
        "",
        _format_indicator_block("5Min", snap.get("5Min", {})),
        "",
        _format_indicator_block("15Min", snap.get("15Min", {})),
        "",
        _format_indicator_block("1Hour", snap.get("1Hour", {})),
        "",
        f"**Signal score (heuristique)** : {score['score']}/5 · {', '.join(score['reasons']) if score['reasons'] else 'aucun signal flag'}",
        "",
    ]
    if chart_path:
        lines += [
            "## 3. Chart visuel disponible",
            f"`{chart_path}` (5m, 800×600, RSI+MACD+Volume). Lis-le avec `Read` si pertinent (la tendance et les niveaux y sont plus lisibles).",
            "",
        ]
    lines += [
        "## 4. Sim portfolio",
        f"- Equity: `${port['equity']:.2f}` (all-time `{port['all_time_pnl_pct']:+.2f}%`)",
        f"- Peak: `${port['peak_equity']:.2f}` · Max DD: `{port['max_dd_pct']:.2f}%`",
        f"- Closed: {port['closed_trades']} ({port['wins']}W / {port['losses']}L)",
        f"- Open trades: {len(open_trades)}",
    ]
    for t in open_trades:
        lines.append(f"  - `{t['id']}` {t['side'].upper()} entry=`{t['entry']:.2f}` qty=`{t['qty']:.6f}` tp=`{t['tp']:.2f}` sl=`{t['sl']:.2f}` opened=`{t['opened_at']}`")
    lines += [
        "",
        "## 5. Recent log (10 last events)",
        "```",
    ]
    for r in log_tail[-10:]:
        if r["type"] == "open":
            t = r["trade"]
            lines.append(f"OPEN  {r['ts']}  {t['side']}@{t['entry']:.2f} qty={t['qty']:.6f} tp={t['tp']} sl={t['sl']}")
        elif r["type"] == "close":
            t = r["trade"]
            lines.append(f"CLOSE {r['ts']}  {t['side']}@{t['exit']:.2f} pnl={t['pnl_usd']:+.2f} ({t['pnl_pct']:+.2f}%) reason={t.get('close_reason','')}")
    lines += ["```", ""]
    lines += [
        "## 6. Garde-fous (en dur, infranchissables)",
        f"- Sizing : entre `{SIZING_MIN_PCT}%` et `{SIZING_MAX_PCT}%` du equity",
        f"- R/R floor : `{RR_FLOOR}` (sinon SKIP forcé)",
        f"- Cooldown : `{COOLDOWN_MIN}` min après une fermeture même direction",
        f"- Daily loss cap : `{DAILY_LOSS_CAP_PCT}%` jour → freeze new (HOLD-only)",
        f"- Max {MAX_OPEN} position ouverte. Si déjà ouverte, ta décision se limite à CLOSE/HOLD.",
        "- Spread > 0.15% → SKIP forcé.",
        "",
        "## 7. Format de réponse — JSON STRICT obligatoire",
        "Termine ta réponse avec UN SEUL bloc ` ```json ... ``` ` contenant exactement :",
        "```json",
        "{",
        '  "action": "OPEN_LONG|OPEN_SHORT|CLOSE|HOLD|SKIP",',
        '  "trade_id": "<id si CLOSE, sinon null>",',
        '  "limit_price": 67432.50,',
        '  "tp": 68100.00,',
        '  "sl": 67100.00,',
        '  "sizing_pct": 8,',
        '  "rr_ratio": 2.0,',
        '  "time_horizon_min": 60,',
        '  "confidence": 72,',
        '  "reason_fr": "Squeeze BB 5m + RSI reclaim 32→48 + MACD cross haussier 15m + volume ×1.6 cassure VWAP. News: ETF inflow $48M overnight.",',
        '  "ctqs": {"T": 18, "Q": 16, "S": 14, "C": 12}',
        "}",
        "```",
        "",
        "Règles JSON :",
        "- `action=HOLD` si position ouverte et pas de raison de fermer (laisse SL/TP gérer).",
        "- `action=SKIP` si conditions de marché floues / pas de setup net.",
        "- `action=CLOSE` si tu veux sortir avant TP/SL (ex. thèse cassée par news, ou trail manuel).",
        "- `action=OPEN_LONG/OPEN_SHORT` ne se fait que si AUCUNE position ouverte.",
        "- `tp`/`sl` toujours présents pour OPEN_*. R/R = abs(tp-entry)/abs(entry-sl) ≥ 1.3 sinon le harness rejettera.",
        "- `reason_fr` doit citer 2-3 indicateurs précis ET 1 news. C'est le bloc que l'utilisateur lit en notif.",
        "- `confidence` 0-100. Sub-50 → SKIP de toute façon.",
        "- Pas de markdown autour du JSON, pas de prose dans le JSON.",
    ]
    return "\n".join(lines)


# ───────── prepare command ─────────


def cmd_prepare() -> int:
    ctx = _build_context()
    CONTEXT_FILE.write_text(json.dumps(ctx, indent=2, default=str))
    PROMPT_FILE.write_text(_build_prompt(ctx))
    _append_run({"phase": "prepare", "ts": _iso(), "score": ctx["signal_score"], "chart": ctx.get("chart_path")})
    print(f"prepare ok · prompt={len(PROMPT_FILE.read_text())} chars · score={ctx['signal_score']['score']} · chart={'yes' if ctx['chart_path'] else 'no'}")
    return 0


# ───────── decision parsing ─────────


def _extract_json_block(text: str) -> dict[str, Any] | None:
    """Find the last ```json ... ``` block in text."""
    blocks = re.findall(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if not blocks:
        m = re.search(r"\{[^{}]*\"action\"[^{}]*\}", text, re.DOTALL)
        if not m:
            return None
        blocks = [m.group(0)]
    try:
        return json.loads(blocks[-1])
    except json.JSONDecodeError:
        return None


def _parse_envelope() -> dict[str, Any] | None:
    if not ENVELOPE_FILE.exists():
        return None
    try:
        env = json.loads(ENVELOPE_FILE.read_text())
    except json.JSONDecodeError:
        return None
    text = env.get("result") or env.get("response") or ""
    if not text and isinstance(env.get("messages"), list):
        for msg in reversed(env["messages"]):
            if msg.get("role") == "assistant":
                text = msg.get("content", [{}])[0].get("text", "") if isinstance(msg.get("content"), list) else msg.get("content", "")
                break
    return _extract_json_block(text)


# ───────── guardrails ─────────


def _last_close_for_side(side: str) -> dict[str, Any] | None:
    """Most recent close event matching side."""
    log = _read_recent_trade_log(100)
    for r in reversed(log):
        if r["type"] == "close" and r["trade"]["side"] == side:
            return r
    return None


def _today_realized_pct() -> float:
    today = _utc().strftime("%Y-%m-%d")
    log = _read_recent_trade_log(500)
    port = json.loads((STATE_DIR / "sim_portfolio.json").read_text())
    realized_today = 0.0
    for r in log:
        if r["type"] == "close" and r["ts"].startswith(today):
            realized_today += r["trade"]["pnl_usd"]
    return realized_today / port["starting_equity"] * 100


def _validate(decision: dict[str, Any], ctx: dict[str, Any]) -> tuple[bool, str]:
    a = decision.get("action")
    if a not in ("OPEN_LONG", "OPEN_SHORT", "CLOSE", "HOLD", "SKIP"):
        return False, f"unknown action: {a}"
    if a in ("HOLD", "SKIP"):
        return True, "noop"

    open_trades = ctx["sim_portfolio"]["open_trades"]
    if a == "CLOSE":
        if not open_trades:
            return False, "CLOSE but no open trade"
        return True, "ok"

    # OPEN_*
    if open_trades:
        return False, "OPEN refused: a position is already open"

    if _today_realized_pct() <= DAILY_LOSS_CAP_PCT:
        return False, f"daily loss cap {DAILY_LOSS_CAP_PCT}% reached"

    side = "long" if a == "OPEN_LONG" else "short"
    last_same = _last_close_for_side(side)
    if last_same:
        closed_at = datetime.fromisoformat(last_same["ts"].replace("Z", "+00:00"))
        if (_utc() - closed_at) < timedelta(minutes=COOLDOWN_MIN):
            return False, f"cooldown active for {side} (closed {(_utc() - closed_at).total_seconds()/60:.1f}min ago)"

    sizing = decision.get("sizing_pct", 0)
    if not (SIZING_MIN_PCT <= sizing <= SIZING_MAX_PCT):
        return False, f"sizing {sizing}% out of [{SIZING_MIN_PCT}, {SIZING_MAX_PCT}]"

    entry = decision.get("limit_price") or 0
    tp = decision.get("tp") or 0
    sl = decision.get("sl") or 0
    if entry <= 0 or tp <= 0 or sl <= 0:
        return False, "bad price levels"
    rr = abs(tp - entry) / max(abs(entry - sl), 1e-9)
    if rr < RR_FLOOR:
        return False, f"R/R {rr:.2f} below floor {RR_FLOOR}"
    if side == "long" and not (sl < entry < tp):
        return False, "LONG requires sl < entry < tp"
    if side == "short" and not (tp < entry < sl):
        return False, "SHORT requires tp < entry < sl"

    quote = ctx["snapshot"].get("latest_quote", {}) or {}
    if quote.get("ap") and quote.get("bp"):
        spread_pct = (quote["ap"] - quote["bp"]) / quote["ap"] * 100
        if spread_pct > 0.15:
            return False, f"spread {spread_pct:.3f}% > 0.15%"

    if (decision.get("confidence") or 0) < 50:
        return False, f"confidence {decision.get('confidence')} < 50"
    return True, "ok"


# ───────── execute ─────────


def _execute(decision: dict[str, Any]) -> dict[str, Any]:
    a = decision["action"]
    if a == "HOLD" or a == "SKIP":
        return {"executed": False, "kind": a.lower()}
    if a == "CLOSE":
        port = sim_portfolio.snapshot()
        opens = port["open_trades"]
        tid = decision.get("trade_id") or (opens[0]["id"] if opens else None)
        if not tid:
            return {"executed": False, "kind": "close-noop"}
        latest = btc_data.get_latest_trade()
        price = latest.get("p") or decision.get("limit_price")
        t = sim_portfolio.close_position(tid, float(price), reason=decision.get("reason_fr", "manual close")[:120])
        return {"executed": True, "kind": "close", "trade": t}
    side = "long" if a == "OPEN_LONG" else "short"
    t = sim_portfolio.open_position(
        side=side,
        price=float(decision["limit_price"]),
        sizing_pct=float(decision["sizing_pct"]),
        tp=float(decision["tp"]),
        sl=float(decision["sl"]),
        reason=decision.get("reason_fr", "")[:120],
    )
    return {"executed": True, "kind": "open", "trade": t, "decision": decision}


def _check_hits_and_close() -> list[dict[str, Any]]:
    """Detect TP/SL hits since last tick, close affected trades, return events."""
    open_trades = json.loads((STATE_DIR / "open_trades.json").read_text())["trades"]
    if not open_trades:
        return []
    earliest = min(datetime.fromisoformat(t["opened_at"].replace("Z", "+00:00")) for t in open_trades)
    minutes_needed = max(int((_utc() - earliest).total_seconds() / 60) + 5, 30)
    bars = btc_data.get_bars("1Min", limit=min(minutes_needed, 1000))
    events = trade_tracker.check_hits(open_trades, bars)
    closed: list[dict[str, Any]] = []
    for ev in events:
        try:
            t = sim_portfolio.close_position(ev["trade_id"], ev["exit_price"], reason=ev["reason"])
            closed.append({"event": ev, "trade": t})
        except SystemExit:
            pass
    return closed


# ───────── telegram (anti-spam gated) ─────────


def _load_last_notif() -> dict[str, Any]:
    if not LAST_NOTIF_FILE.exists():
        return {"last_event_ts": None, "last_heartbeat_hour": None, "last_daily_report_date": None}
    return json.loads(LAST_NOTIF_FILE.read_text())


def _save_last_notif(d: dict[str, Any]) -> None:
    LAST_NOTIF_FILE.write_text(json.dumps(d, indent=2))


def _format_open_msg(t: dict[str, Any], decision: dict[str, Any]) -> str:
    side = t["side"].upper()
    rr = decision.get("rr_ratio", "?")
    horizon = decision.get("time_horizon_min", "?")
    conf = decision.get("confidence", "?")
    ctqs = decision.get("ctqs", {})
    tp_pct = abs(t["tp"] / t["entry"] - 1) * 100
    sl_pct = abs(t["sl"] / t["entry"] - 1) * 100
    sign_tp = "+" if t["side"] == "long" else "-"
    sign_sl = "-" if t["side"] == "long" else "+"
    return (
        f"*🐂 BullHF-BTC — Nouveau trade*\n"
        f"_{_iso()[:19].replace('T',' ')} UTC_\n\n"
        f"🎯 *Setup* : {side} · BTC/USD\n"
        f"• Entrée : `${t['entry']:,.2f}`\n"
        f"• TP : `${t['tp']:,.2f}` ({sign_tp}{tp_pct:.2f}%)\n"
        f"• SL : `${t['sl']:,.2f}` ({sign_sl}{sl_pct:.2f}%)\n"
        f"• R/R : `{rr}` · Taille : `{t['sizing_pct']}%` (`${t['notional_at_open']:.2f}`)\n"
        f"• Horizon : `{horizon}` min · Conf : `{conf}/100`\n"
        f"• CTQS : T{ctqs.get('T','?')} Q{ctqs.get('Q','?')} S{ctqs.get('S','?')} C{ctqs.get('C','?')}\n\n"
        f"🧠 *Pourquoi*\n{telegram_hf.escape_md(decision.get('reason_fr','(pas de raison fournie)'))}\n\n"
        f"📊 Sim equity : `${sim_portfolio._load_port()['equity']:,.2f}`"
    )


def _format_close_msg(t: dict[str, Any], reason: str) -> str:
    pnl_sign = "+" if t["pnl_usd"] >= 0 else ""
    emoji = "✅" if t["pnl_usd"] >= 0 else "🔴"
    return (
        f"*🐂 BullHF-BTC — Trade clos {emoji}*\n"
        f"_{_iso()[:19].replace('T',' ')} UTC_\n\n"
        f"• {t['side'].upper()} entry=`{t['entry']:.2f}` exit=`{t['exit']:.2f}`\n"
        f"• P&L : `{pnl_sign}${t['pnl_usd']:.2f}` ({pnl_sign}{t['pnl_pct']:.2f}%)\n"
        f"• Raison : {telegram_hf.escape_md(reason[:200])}\n\n"
        f"📊 Sim equity : `${sim_portfolio._load_port()['equity']:,.2f}`"
    )


def _format_heartbeat(ctx: dict[str, Any] | None = None) -> str:
    port = sim_portfolio.snapshot()
    if ctx is None:
        snap = btc_data.snapshot()
        last = snap.get("5Min", {}).get("last_close", "?")
    else:
        last = ctx["snapshot"].get("5Min", {}).get("last_close", "?")
    last_str = f"${last:,.2f}" if isinstance(last, (int, float)) else str(last)
    open_str = "aucune"
    if port["open_trades"]:
        t = port["open_trades"][0]
        unr = (port["last_mark_price"] - t["entry"]) * t["qty"] if t["side"] == "long" else (t["entry"] - port["last_mark_price"]) * t["qty"]
        unr_pct = unr / t["notional_at_open"] * 100
        open_str = f"{t['side'].upper()} ouverte (`{unr_pct:+.2f}%`)"
    return (
        f"*🐂 BullHF-BTC — Heartbeat*\n"
        f"_{_iso()[:16].replace('T',' ')} UTC_\n\n"
        f"• BTC : `{last_str}`\n"
        f"• Position : {open_str}\n"
        f"• Sim equity : `${port['equity']:,.2f}` ({port['all_time_pnl_pct']:+.2f}% all-time)\n"
        f"• Trades clos : {port['closed_trades']} ({port['win_rate']}% WR)" if port["closed_trades"] else f"• Trades clos : 0"
    )


def _maybe_notify(events: dict[str, Any], ctx: dict[str, Any]) -> None:
    notif = _load_last_notif()
    now = _utc()
    sent_now = False
    chart_path = ctx.get("chart_path")

    # Trade events first (always notify)
    for closed_ev in events.get("auto_closed", []):
        msg = _format_close_msg(closed_ev["trade"], closed_ev["event"]["reason"])
        telegram_hf.send_message(msg)
        sent_now = True

    exec_res = events.get("exec", {})
    if exec_res.get("executed"):
        if exec_res["kind"] == "open":
            msg = _format_open_msg(exec_res["trade"], exec_res["decision"])
            if chart_path and Path(chart_path).exists():
                telegram_hf.send_photo(chart_path, msg)
            else:
                telegram_hf.send_message(msg)
            sent_now = True
        elif exec_res["kind"] == "close":
            telegram_hf.send_message(_format_close_msg(exec_res["trade"], "manual CLOSE"))
            sent_now = True

    if sent_now:
        notif["last_event_ts"] = _iso()
        _save_last_notif(notif)
        return

    # Heartbeat: top-of-hour, skip if event sent in last 10min
    if now.minute < 5:
        last_hb_hour = notif.get("last_heartbeat_hour")
        cur_hour = now.strftime("%Y-%m-%dT%H")
        last_event = notif.get("last_event_ts")
        last_event_dt = datetime.fromisoformat(last_event.replace("Z", "+00:00")) if last_event else None
        if last_hb_hour != cur_hour and (
            last_event_dt is None or (now - last_event_dt) > timedelta(minutes=HEARTBEAT_QUIET_MIN)
        ):
            msg = _format_heartbeat(ctx)
            if chart_path and Path(chart_path).exists():
                telegram_hf.send_photo(chart_path, msg)
            else:
                telegram_hf.send_message(msg)
            notif["last_heartbeat_hour"] = cur_hour
            _save_last_notif(notif)

    # Daily report at 23:55 UTC
    if now.hour == DAILY_REPORT_HOUR_UTC and now.minute >= DAILY_REPORT_MIN_UTC:
        last_date = notif.get("last_daily_report_date")
        today = now.strftime("%Y-%m-%d")
        if last_date != today:
            telegram_hf.send_message(stats.report_fr("daily"))
            notif["last_daily_report_date"] = today
            _save_last_notif(notif)


# ───────── git commit ─────────


def _git_commit(summary: str, material: bool) -> None:
    if not material:
        return
    try:
        subprocess.run(["git", "add", "-A", "hf_btc/state/", "hf_btc/"], cwd=str(REPO), check=True, capture_output=True)
        msg = f"[hf-btc] {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} — {summary}"
        subprocess.run(["git", "commit", "-m", msg], cwd=str(REPO), check=True, capture_output=True)
        subprocess.run(["git", "push"], cwd=str(REPO), check=False, capture_output=True, timeout=30)
    except subprocess.CalledProcessError:
        pass


# ───────── post command ─────────


def _append_run(record: dict[str, Any]) -> None:
    with RUNS_FILE.open("a") as f:
        f.write(json.dumps(record) + "\n")


def cmd_post(force_decision: dict[str, Any] | None = None) -> int:
    if not CONTEXT_FILE.exists():
        print("post error: missing /tmp/hf_context.json")
        return 1
    ctx = json.loads(CONTEXT_FILE.read_text())
    # Refresh portfolio state — sim_portfolio mutates between prepare and post
    # if a previous post opened/closed a trade in the same tick.
    ctx["sim_portfolio"] = sim_portfolio.snapshot()

    decision = force_decision or _parse_envelope()
    if decision is None:
        decision = {"action": "SKIP", "reason_fr": "decision parse failure", "confidence": 0}
        valid = False
        why = "no parseable JSON"
    else:
        valid, why = _validate(decision, ctx)

    if valid:
        exec_res = _execute(decision)
    else:
        exec_res = {"executed": False, "kind": "rejected", "why": why, "decision": decision}

    # Check TP/SL hits regardless
    auto_closed = _check_hits_and_close()

    # Mark-to-market with current price
    latest = btc_data.get_latest_trade()
    mark = latest.get("p")
    if mark:
        sim_portfolio.mark_to_market(float(mark))

    DECISION_FILE.write_text(json.dumps(decision, indent=2))
    events = {"exec": exec_res, "auto_closed": auto_closed}
    _maybe_notify(events, ctx)

    summary_bits = []
    if exec_res.get("executed"):
        summary_bits.append(f"{exec_res['kind']} {exec_res['trade']['side']}@{exec_res['trade'].get('entry') or exec_res['trade'].get('exit')}")
    if auto_closed:
        for c in auto_closed:
            summary_bits.append(f"auto-close {c['trade']['id']} pnl={c['trade']['pnl_usd']:+.2f}")
    if not summary_bits:
        if not valid:
            summary_bits.append(f"reject ({why})")
        else:
            summary_bits.append(decision.get("action", "noop").lower())
    summary = " · ".join(summary_bits)

    _append_run({
        "phase": "post", "ts": _iso(),
        "decision": decision, "valid": valid, "why": why,
        "exec": {k: v for k, v in exec_res.items() if k != "decision"},
        "auto_closed": [c["trade"]["id"] for c in auto_closed],
        "mark_price": mark,
    })

    material = bool(exec_res.get("executed") or auto_closed or _utc().minute < 5)
    _git_commit(summary, material)
    print(f"post ok · {summary} · valid={valid} · why={why}")
    return 0


# ───────── tick_dry / sleep / daily ─────────


def cmd_tick_dry() -> int:
    cmd_prepare()
    print(f"\n--- /tmp/hf_prompt.md ({len(PROMPT_FILE.read_text())} chars) ---")
    print(PROMPT_FILE.read_text()[:2000])
    print("...\n")
    fake = {
        "action": "SKIP", "trade_id": None,
        "limit_price": None, "tp": None, "sl": None,
        "sizing_pct": 0, "rr_ratio": 0, "time_horizon_min": 0,
        "confidence": 30,
        "reason_fr": "DRY-RUN test — no LLM invoked, default SKIP.",
        "ctqs": {"T": 10, "Q": 10, "S": 10, "C": 10},
    }
    return cmd_post(force_decision=fake)


def cmd_sleep_until_next() -> int:
    now = _utc()
    next_min = ((now.minute // 5) + 1) * 5
    if next_min >= 60:
        nxt = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))
    else:
        nxt = now.replace(minute=next_min, second=0, microsecond=0)
    sleep = (nxt - now).total_seconds()
    sleep = max(sleep, 5.0)
    print(f"sleeping {sleep:.0f}s until {nxt.isoformat()}")
    time.sleep(sleep)
    return 0


def cmd_daily() -> int:
    msg = stats.report_fr("daily")
    res = telegram_hf.send_message(msg)
    print(json.dumps(res, indent=2))
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "prepare":
        return cmd_prepare()
    if cmd == "post":
        return cmd_post()
    if cmd == "tick_dry":
        return cmd_tick_dry()
    if cmd == "sleep_until_next":
        return cmd_sleep_until_next()
    if cmd == "daily":
        return cmd_daily()
    print(f"Unknown: {cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
