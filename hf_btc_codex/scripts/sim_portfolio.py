#!/usr/bin/env python3
"""$3000 sim portfolio for Bull-HF-BTC. LONG + SHORT virtual.

Single-position cap (max 1 open trade). Binance Futures-like fees per fill.
P&L-based accounting: equity = starting + realized + unrealized.

State files:
  state/sim_portfolio.json   — cash, equity, peak, max_dd, win/loss counters, equity_curve
  state/open_trades.json     — list of open trades
  state/trade_log.jsonl      — append-only log of every action

Usage:
    python sim_portfolio.py snapshot
    python sim_portfolio.py open long  --price 67432.5 --sizing 8 --tp 68100 --sl 67100 --reason "test"
    python sim_portfolio.py open short --price 67432.5 --sizing 8 --tp 67000 --sl 67700 --reason "test"
    python sim_portfolio.py close <id> --price 68000 --reason "tp hit"
    python sim_portfolio.py mark --price 67800
    python sim_portfolio.py reset
"""

from __future__ import annotations

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_DIR = Path(__file__).resolve().parent.parent / "state"
PORT_FILE = STATE_DIR / "sim_portfolio.json"
OPEN_FILE = STATE_DIR / "open_trades.json"
LOG_FILE = STATE_DIR / "trade_log.jsonl"

SLIPPAGE_PCT = float(os.environ.get("HF_SIM_SLIPPAGE_PCT", "0.01"))
BINANCE_MAKER_FEE_PCT = float(os.environ.get("HF_SIM_MAKER_FEE_PCT", "0.02"))
BINANCE_TAKER_FEE_PCT = float(os.environ.get("HF_SIM_TAKER_FEE_PCT", "0.05"))
EXECUTION_LIQUIDITY = os.environ.get("HF_SIM_LIQUIDITY", "taker").strip().lower()
MAX_OPEN = 1


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_port() -> dict[str, Any]:
    return json.loads(PORT_FILE.read_text())


def _save_port(p: dict[str, Any]) -> None:
    PORT_FILE.write_text(json.dumps(p, indent=2))


def _load_open() -> dict[str, Any]:
    return json.loads(OPEN_FILE.read_text())


def _save_open(o: dict[str, Any]) -> None:
    OPEN_FILE.write_text(json.dumps(o, indent=2))


def _append_log(record: dict[str, Any]) -> None:
    with LOG_FILE.open("a") as f:
        f.write(json.dumps(record) + "\n")


def _apply_slippage(price: float, side: str, action: str) -> float:
    """Adverse slippage: LONG entry pays up, LONG exit gets less, mirror for SHORT."""
    s = SLIPPAGE_PCT / 100.0
    if action == "open":
        return price * (1 + s) if side == "long" else price * (1 - s)
    if action == "close":
        return price * (1 - s) if side == "long" else price * (1 + s)
    return price


def _fee_rate_pct() -> float:
    if EXECUTION_LIQUIDITY == "maker":
        return BINANCE_MAKER_FEE_PCT
    return BINANCE_TAKER_FEE_PCT


def _fee_usd(notional: float) -> float:
    return notional * (_fee_rate_pct() / 100.0)


def _unrealized(trade: dict[str, Any], mark: float) -> float:
    if trade["side"] == "long":
        return (mark - trade["entry"]) * trade["qty"]
    return (trade["entry"] - mark) * trade["qty"]


def _recompute_equity(port: dict[str, Any], opens: dict[str, Any], mark: float | None) -> None:
    realized = port["equity"] - port["starting_equity"]  # invariant from prior closes
    # We instead derive equity from the canonical "realized so far" stored implicitly.
    # Cleaner: maintain a "realized_pnl" accumulator. Migrate equity = starting + realized + unrealized.
    realized = port.get("realized_pnl", 0.0)
    unr = sum(_unrealized(t, mark) for t in opens["trades"]) if mark is not None and opens["trades"] else 0.0
    eq = port["starting_equity"] + realized + unr
    port["equity"] = round(eq, 4)
    port["cash"] = round(port["starting_equity"] + realized, 4)  # cash is realized-only
    if eq > port["peak_equity"]:
        port["peak_equity"] = round(eq, 4)
    dd = (eq / port["peak_equity"] - 1.0) * 100 if port["peak_equity"] else 0.0
    if dd < port["max_dd_pct"]:
        port["max_dd_pct"] = round(dd, 4)
    if mark is not None:
        port["last_mark_ts"] = _now()
        port["last_mark_price"] = mark
        port["equity_curve"].append([port["last_mark_ts"], round(eq, 4)])
        if len(port["equity_curve"]) > 5000:
            port["equity_curve"] = port["equity_curve"][-5000:]


def open_position(side: str, price: float, sizing_pct: float, tp: float, sl: float, reason: str = "") -> dict[str, Any]:
    if side not in ("long", "short"):
        raise SystemExit(f"side must be long|short, got {side}")
    if not (0 < sizing_pct <= 100):
        raise SystemExit("sizing_pct out of range")
    port = _load_port()
    opens = _load_open()
    if len(opens["trades"]) >= MAX_OPEN:
        raise SystemExit(f"max {MAX_OPEN} open trade(s) — close existing first")
    fill = _apply_slippage(price, side, "open")
    notional = port["equity"] * (sizing_pct / 100.0)
    open_fee = _fee_usd(notional)
    qty = notional / fill
    tid = uuid.uuid4().hex[:8]
    trade = {
        "id": tid, "side": side, "entry": fill, "raw_price": price,
        "qty": round(qty, 8), "sizing_pct": sizing_pct, "tp": tp, "sl": sl,
        "opened_at": _now(), "reason": reason, "notional_at_open": round(notional, 4),
        "fee_model": f"binance_futures_{EXECUTION_LIQUIDITY}",
        "fee_rate_pct": _fee_rate_pct(),
        "open_fee_usd": round(open_fee, 4),
    }
    opens["trades"].append(trade)
    _save_open(opens)
    port["realized_pnl"] = port.get("realized_pnl", 0.0) - open_fee
    port["fees_paid"] = round(port.get("fees_paid", 0.0) + open_fee, 4)
    _recompute_equity(port, opens, fill)
    _save_port(port)
    _append_log({"ts": _now(), "type": "open", "trade": trade, "equity_after": port["equity"]})
    return trade


def close_position(trade_id: str, price: float, reason: str = "") -> dict[str, Any]:
    port = _load_port()
    opens = _load_open()
    idx = next((i for i, t in enumerate(opens["trades"]) if t["id"] == trade_id), None)
    if idx is None:
        raise SystemExit(f"trade {trade_id} not found")
    t = opens["trades"][idx]
    fill = _apply_slippage(price, t["side"], "close")
    close_notional = fill * t["qty"]
    close_fee = _fee_usd(close_notional)
    gross_pnl = (fill - t["entry"]) * t["qty"] if t["side"] == "long" else (t["entry"] - fill) * t["qty"]
    pnl = gross_pnl - close_fee
    total_fees = float(t.get("open_fee_usd", 0.0)) + close_fee
    pnl_pct = (gross_pnl - total_fees) / t["notional_at_open"] * 100 if t["notional_at_open"] else 0.0
    t.update({
        "closed_at": _now(), "exit": fill, "exit_raw": price,
        "gross_pnl_usd": round(gross_pnl, 4),
        "close_fee_usd": round(close_fee, 4),
        "total_fees_usd": round(total_fees, 4),
        "pnl_usd": round(gross_pnl - total_fees, 4),
        "pnl_pct": round(pnl_pct, 4),
        "close_reason": reason,
    })
    opens["trades"].pop(idx)
    _save_open(opens)
    port["realized_pnl"] = port.get("realized_pnl", 0.0) + pnl
    port["fees_paid"] = round(port.get("fees_paid", 0.0) + close_fee, 4)
    port["closed_trades_count"] += 1
    if pnl > 0:
        port["wins"] += 1
        port["gross_win"] = round(port.get("gross_win", 0.0) + pnl, 4)
    else:
        port["losses"] += 1
        port["gross_loss"] = round(port.get("gross_loss", 0.0) + pnl, 4)
    _recompute_equity(port, opens, fill)
    _save_port(port)
    _append_log({"ts": _now(), "type": "close", "trade": t, "equity_after": port["equity"]})
    return t


def mark_to_market(price: float) -> dict[str, Any]:
    port = _load_port()
    opens = _load_open()
    _recompute_equity(port, opens, price)
    _save_port(port)
    return port


def snapshot() -> dict[str, Any]:
    port = _load_port()
    opens = _load_open()
    pf = (port.get("gross_win", 0.0) / abs(port.get("gross_loss", 1.0))) if port.get("gross_loss") else None
    wr = (port["wins"] / port["closed_trades_count"]) if port["closed_trades_count"] else None
    return {
        "equity": port["equity"],
        "starting_equity": port["starting_equity"],
        "all_time_pnl_pct": round((port["equity"] / port["starting_equity"] - 1.0) * 100, 4),
        "peak_equity": port["peak_equity"],
        "max_dd_pct": port["max_dd_pct"],
        "closed_trades": port["closed_trades_count"],
        "wins": port["wins"], "losses": port["losses"],
        "win_rate": round(wr * 100, 2) if wr is not None else None,
        "profit_factor": round(pf, 3) if pf is not None else None,
        "open_trades": opens["trades"],
        "last_mark_ts": port.get("last_mark_ts"),
        "last_mark_price": port.get("last_mark_price"),
    }


def reset() -> None:
    PORT_FILE.write_text(json.dumps({
        "starting_equity": 3000.0, "cash": 3000.0, "equity": 3000.0,
        "peak_equity": 3000.0, "max_dd_pct": 0.0,
        "realized_pnl": 0.0,
        "closed_trades_count": 0, "wins": 0, "losses": 0,
        "gross_win": 0.0, "gross_loss": 0.0,
        "equity_curve": [], "last_mark_ts": None, "last_mark_price": None,
    }, indent=2))
    OPEN_FILE.write_text(json.dumps({"trades": []}, indent=2))
    LOG_FILE.write_text("")


def _pp(obj: Any) -> None:
    print(json.dumps(obj, indent=2, default=str))


def _arg(argv: list[str], flag: str, conv=str, default=None):
    if flag in argv:
        return conv(argv[argv.index(flag) + 1])
    return default


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "snapshot":
        _pp(snapshot())
    elif cmd == "reset":
        reset()
        print("reset ok")
    elif cmd == "open":
        side = argv[2]
        _pp(open_position(
            side=side,
            price=_arg(argv, "--price", float),
            sizing_pct=_arg(argv, "--sizing", float),
            tp=_arg(argv, "--tp", float),
            sl=_arg(argv, "--sl", float),
            reason=_arg(argv, "--reason", str, ""),
        ))
    elif cmd == "close":
        tid = argv[2]
        _pp(close_position(
            trade_id=tid,
            price=_arg(argv, "--price", float),
            reason=_arg(argv, "--reason", str, ""),
        ))
    elif cmd == "mark":
        _pp(mark_to_market(_arg(argv, "--price", float)))
    else:
        print(f"Unknown: {cmd}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
