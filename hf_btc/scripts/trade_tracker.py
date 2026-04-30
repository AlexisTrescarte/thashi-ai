#!/usr/bin/env python3
"""Detect TP/SL hits between ticks by scanning intra-tick OHLCV bars.

For each open trade, scan 1Min bars from `opened_at` forward and detect:
  LONG  : SL hit if bar.low  <= sl, TP hit if bar.high >= tp
  SHORT : SL hit if bar.high >= sl, TP hit if bar.low  <= tp

Conservative tie-break: if both touched in the same bar, SL is assumed hit first
(worst-case fill). Exit price = level price (sim assumes fill at the stop level,
no gap modelling).

Usage:
    python trade_tracker.py check                       # pull 1m bars + check all opens
    python trade_tracker.py simulate < scenario.json    # test with custom bars
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

STATE_DIR = Path(__file__).resolve().parent.parent / "state"
OPEN_FILE = STATE_DIR / "open_trades.json"


def _parse_iso(ts: str) -> datetime:
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)


def check_hits(open_trades: list[dict[str, Any]], bars: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return a list of close events. Each: {trade_id, exit_price, reason, hit_at, bar_ts}.

    Bars must be ascending by time. Each bar: {t, o, h, l, c, v}.
    """
    events: list[dict[str, Any]] = []
    for t in open_trades:
        opened_at = _parse_iso(t["opened_at"])
        side = t["side"]
        tp = t["tp"]
        sl = t["sl"]
        for b in bars:
            bar_ts = _parse_iso(b["t"])
            if bar_ts < opened_at:
                continue
            sl_hit = (side == "long" and b["l"] <= sl) or (side == "short" and b["h"] >= sl)
            tp_hit = (side == "long" and b["h"] >= tp) or (side == "short" and b["l"] <= tp)
            if sl_hit and tp_hit:
                events.append({
                    "trade_id": t["id"], "exit_price": sl,
                    "reason": "sl-hit (conservative tie-break)",
                    "hit_at": _now_iso(), "bar_ts": b["t"],
                })
                break
            if sl_hit:
                events.append({
                    "trade_id": t["id"], "exit_price": sl,
                    "reason": "sl-hit", "hit_at": _now_iso(), "bar_ts": b["t"],
                })
                break
            if tp_hit:
                events.append({
                    "trade_id": t["id"], "exit_price": tp,
                    "reason": "tp-hit", "hit_at": _now_iso(), "bar_ts": b["t"],
                })
                break
    return events


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def check_live() -> list[dict[str, Any]]:
    """Pull latest 1Min bars and check all open trades."""
    opens = json.loads(OPEN_FILE.read_text())["trades"]
    if not opens:
        return []
    # lazy import to keep this module testable without network
    from btc_data import get_bars  # type: ignore
    earliest = min(_parse_iso(t["opened_at"]) for t in opens)
    minutes_needed = max(int((datetime.now(timezone.utc) - earliest).total_seconds() / 60) + 5, 30)
    bars = get_bars("1Min", limit=min(minutes_needed, 1000))
    return check_hits(opens, bars)


def _pp(obj: Any) -> None:
    print(json.dumps(obj, indent=2, default=str))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "check":
        _pp(check_live())
    elif cmd == "simulate":
        scenario = json.loads(sys.stdin.read())
        _pp(check_hits(scenario["trades"], scenario["bars"]))
    else:
        print(f"Unknown: {cmd}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
