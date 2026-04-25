#!/usr/bin/env python3
"""Pre-trade safety guards (fat-finger, notional cap, rate-limit, kill-switch).

Stdlib only. Returns JSON contract on stdout.

Usage:
    python scripts/pretrade_guards.py check \\
        --symbol AAPL --side buy --qty 10 --price 175.20 \\
        --equity 100000 --max-position-pct 10 --ref-price 174.80

Output:
    {"pass": true, "reasons": [], "checks": {...}}

Exit code: 0 if all pass, 2 if any fail (so shell pipelines fail loudly).

Wired-into philosophy: the trade skill should call this BEFORE submitting any
order. Fat-finger and rate-limit are enforced in Python (not in the LLM prompt)
because LLM hallucination is the dominant risk mode for an unattended agent.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path


RATE_LIMIT_PATH = Path(os.environ.get("BULL_RATE_LIMIT_PATH", "memory/.rate_limit.jsonl"))
KILLSWITCH_PATH = Path(os.environ.get("BULL_KILLSWITCH_PATH", "memory/killswitch.flag"))

DEFAULT_FAT_FINGER_PCT = 2.0
DEFAULT_MAX_ORDERS_PER_MINUTE = 6
DEFAULT_MAX_ORDERS_PER_HOUR = 30
DEFAULT_MAX_NOTIONAL_PCT = 10.0


def check_killswitch(side: str) -> tuple[bool, str | None]:
    if not KILLSWITCH_PATH.exists():
        return True, None
    if side.lower() == "sell":
        return True, None
    reason = KILLSWITCH_PATH.read_text(encoding="utf-8").strip() or "killswitch active"
    return False, f"killswitch: {reason}"


def check_fat_finger(price: float, ref_price: float, max_pct: float) -> tuple[bool, str | None]:
    if ref_price <= 0:
        return False, "ref_price invalid"
    deviation_pct = abs(price - ref_price) / ref_price * 100.0
    if deviation_pct > max_pct:
        return False, f"fat-finger: |{price}-{ref_price}|/{ref_price} = {deviation_pct:.2f}% > {max_pct}%"
    return True, None


def check_notional(qty: float, price: float, equity: float, max_pct: float) -> tuple[bool, str | None]:
    if equity <= 0:
        return False, "equity invalid"
    notional = qty * price
    pct = notional / equity * 100.0
    if pct > max_pct:
        return False, f"notional: {notional:.0f} = {pct:.2f}% NAV > {max_pct}% cap"
    return True, None


def _load_rate_log() -> list[dict]:
    if not RATE_LIMIT_PATH.exists():
        return []
    out = []
    for line in RATE_LIMIT_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _trim_rate_log(entries: list[dict], now_ts: float) -> list[dict]:
    cutoff = now_ts - 3600.0
    return [e for e in entries if e.get("ts", 0) >= cutoff]


def check_rate_limit(symbol: str, max_per_minute: int, max_per_hour: int) -> tuple[bool, str | None]:
    now_ts = time.time()
    entries = _trim_rate_log(_load_rate_log(), now_ts)
    last_minute = sum(1 for e in entries if e.get("ts", 0) >= now_ts - 60.0)
    last_hour = len(entries)
    if last_minute >= max_per_minute:
        return False, f"rate-limit: {last_minute} orders in last 60s >= {max_per_minute}"
    if last_hour >= max_per_hour:
        return False, f"rate-limit: {last_hour} orders in last hour >= {max_per_hour}"
    return True, None


def record_order(symbol: str, side: str, qty: float, price: float) -> None:
    RATE_LIMIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {"ts": time.time(), "symbol": symbol.upper(), "side": side.lower(), "qty": qty, "price": price}
    with RATE_LIMIT_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def run_checks(args: argparse.Namespace) -> dict:
    checks = {}
    reasons = []

    ok, reason = check_killswitch(args.side)
    checks["killswitch"] = ok
    if not ok:
        reasons.append(reason)

    ok, reason = check_fat_finger(args.price, args.ref_price, args.max_fat_finger_pct)
    checks["fat_finger"] = ok
    if not ok:
        reasons.append(reason)

    ok, reason = check_notional(args.qty, args.price, args.equity, args.max_position_pct)
    checks["notional"] = ok
    if not ok:
        reasons.append(reason)

    ok, reason = check_rate_limit(args.symbol, args.max_per_minute, args.max_per_hour)
    checks["rate_limit"] = ok
    if not ok:
        reasons.append(reason)

    return {
        "pass": all(checks.values()),
        "reasons": reasons,
        "checks": checks,
        "symbol": args.symbol.upper(),
        "side": args.side.lower(),
        "qty": args.qty,
        "price": args.price,
    }


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="pretrade_guards")
    sub = p.add_subparsers(dest="cmd", required=True)

    chk = sub.add_parser("check", help="Run all pre-trade checks (read-only)")
    chk.add_argument("--symbol", required=True)
    chk.add_argument("--side", required=True, choices=["buy", "sell"])
    chk.add_argument("--qty", required=True, type=float)
    chk.add_argument("--price", required=True, type=float)
    chk.add_argument("--ref-price", required=True, type=float, help="Mid or last price to compare against")
    chk.add_argument("--equity", required=True, type=float)
    chk.add_argument("--max-position-pct", type=float, default=DEFAULT_MAX_NOTIONAL_PCT)
    chk.add_argument("--max-fat-finger-pct", type=float, default=DEFAULT_FAT_FINGER_PCT)
    chk.add_argument("--max-per-minute", type=int, default=DEFAULT_MAX_ORDERS_PER_MINUTE)
    chk.add_argument("--max-per-hour", type=int, default=DEFAULT_MAX_ORDERS_PER_HOUR)

    rec = sub.add_parser("record", help="Record an order in the rate-limit log (call after fill)")
    rec.add_argument("--symbol", required=True)
    rec.add_argument("--side", required=True, choices=["buy", "sell"])
    rec.add_argument("--qty", required=True, type=float)
    rec.add_argument("--price", required=True, type=float)

    args = p.parse_args(argv[1:])

    if args.cmd == "check":
        result = run_checks(args)
        print(json.dumps(result, indent=2))
        return 0 if result["pass"] else 2

    if args.cmd == "record":
        record_order(args.symbol, args.side, args.qty, args.price)
        print(json.dumps({"recorded": True, "symbol": args.symbol.upper()}))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
