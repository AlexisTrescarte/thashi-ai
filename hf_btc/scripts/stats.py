#!/usr/bin/env python3
"""Daily/all-time stats from sim_portfolio + trade_log.

Computes: hit rate, profit factor, Sharpe (per-tick equity diffs annualised),
max DD, Calmar, avg R, distribution by horizon, longest win/loss streak.

Usage:
    python stats.py daily          # today UTC only
    python stats.py all            # all-time
    python stats.py report_fr      # FR Telegram-ready block (today)
"""

from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_DIR = Path(__file__).resolve().parent.parent / "state"
PORT_FILE = STATE_DIR / "sim_portfolio.json"
LOG_FILE = STATE_DIR / "trade_log.jsonl"

TICKS_PER_YEAR = 96 * 365  # 15min ticks, 24/7


def _read_log() -> list[dict[str, Any]]:
    if not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0:
        return []
    return [json.loads(l) for l in LOG_FILE.read_text().splitlines() if l.strip()]


def _closed_trades(scope: str = "all") -> list[dict[str, Any]]:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = []
    for r in _read_log():
        if r.get("type") != "close":
            continue
        if scope == "daily" and not r["ts"].startswith(today):
            continue
        out.append(r["trade"])
    return out


def _streaks(closed: list[dict[str, Any]]) -> tuple[int, int]:
    win_max = loss_max = 0
    win_cur = loss_cur = 0
    for t in closed:
        if t["pnl_usd"] > 0:
            win_cur += 1
            loss_cur = 0
            win_max = max(win_max, win_cur)
        else:
            loss_cur += 1
            win_cur = 0
            loss_max = max(loss_max, loss_cur)
    return win_max, loss_max


def _sharpe(equity_curve: list[list[Any]], scope: str = "all") -> float:
    """Sharpe ratio on per-tick equity returns, annualised."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    pts = [pt for pt in equity_curve if (scope == "all" or pt[0].startswith(today))]
    if len(pts) < 2:
        return float("nan")
    rets = []
    for i in range(1, len(pts)):
        prev, cur = pts[i - 1][1], pts[i][1]
        if prev:
            rets.append(cur / prev - 1.0)
    if len(rets) < 2:
        return float("nan")
    mean = sum(rets) / len(rets)
    var = sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)
    sd = math.sqrt(var)
    if sd == 0:
        return float("nan")
    return mean / sd * math.sqrt(TICKS_PER_YEAR)


def metrics(scope: str = "all") -> dict[str, Any]:
    port = json.loads(PORT_FILE.read_text())
    closed = _closed_trades(scope)
    n = len(closed)
    wins = [t for t in closed if t["pnl_usd"] > 0]
    losses = [t for t in closed if t["pnl_usd"] <= 0]
    gross_w = sum(t["pnl_usd"] for t in wins)
    gross_l = sum(t["pnl_usd"] for t in losses)
    avg_w = gross_w / len(wins) if wins else 0.0
    avg_l = gross_l / len(losses) if losses else 0.0
    pf = gross_w / abs(gross_l) if gross_l else None
    win_max, loss_max = _streaks(closed)
    sh = _sharpe(port.get("equity_curve", []), scope)
    dd = port.get("max_dd_pct", 0.0)
    calmar = (port["equity"] / port["starting_equity"] - 1.0) * 100 / abs(dd) if dd else None

    return {
        "scope": scope,
        "trades": n,
        "wins": len(wins),
        "losses": len(losses),
        "win_rate_pct": round(len(wins) / n * 100, 2) if n else None,
        "gross_win_usd": round(gross_w, 2),
        "gross_loss_usd": round(gross_l, 2),
        "net_pnl_usd": round(gross_w + gross_l, 2),
        "avg_win_usd": round(avg_w, 2),
        "avg_loss_usd": round(avg_l, 2),
        "profit_factor": round(pf, 3) if pf is not None else None,
        "sharpe_annualised": round(sh, 3) if not math.isnan(sh) else None,
        "max_dd_pct_alltime": dd,
        "calmar_alltime": round(calmar, 3) if calmar is not None else None,
        "win_streak_max": win_max,
        "loss_streak_max": loss_max,
        "equity": port["equity"],
        "all_time_pnl_pct": round((port["equity"] / port["starting_equity"] - 1.0) * 100, 3),
        "starting_equity": port["starting_equity"],
    }


def report_fr(scope: str = "daily") -> str:
    m = metrics(scope)
    label = "Bilan jour" if scope == "daily" else "Bilan all-time"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        f"*🐂 BullHF-BTC — {label}*",
        f"_{today} UTC_",
        "",
        "📊 *Sim portfolio*",
        f"• Equity : `${m['equity']:,.2f}` (`{m['all_time_pnl_pct']:+.2f}%` all-time)",
        f"• Max DD : `{m['max_dd_pct_alltime']:.2f}%`",
    ]
    if m["trades"]:
        lines += [
            "",
            f"⚡ *Trades {scope}* : {m['trades']} ({m['wins']}W / {m['losses']}L · {m['win_rate_pct']}% WR)",
            f"• Net : `${m['net_pnl_usd']:+,.2f}` (Σwin `${m['gross_win_usd']:+,.2f}`, Σloss `${m['gross_loss_usd']:+,.2f}`)",
            f"• Avg W : `${m['avg_win_usd']:+,.2f}` · Avg L : `${m['avg_loss_usd']:+,.2f}`",
            f"• Profit factor : `{m['profit_factor']}` · Sharpe : `{m['sharpe_annualised']}`",
            f"• Streak max : 🟢 {m['win_streak_max']} · 🔴 {m['loss_streak_max']}",
        ]
    else:
        lines += ["", f"⚡ *Trades {scope}* : aucun"]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "daily":
        print(json.dumps(metrics("daily"), indent=2, default=str))
    elif cmd == "all":
        print(json.dumps(metrics("all"), indent=2, default=str))
    elif cmd == "report_fr":
        scope = argv[2] if len(argv) > 2 else "daily"
        print(report_fr(scope))
    else:
        print(f"Unknown: {cmd}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
