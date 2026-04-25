#!/usr/bin/env python3
"""Structured event log (poor-man's OpenTelemetry).

Append-only JSONL. One line per event. Consumed by `metrics.py` (future) and
human review for tracing why a signal was produced.

Env:
    BULL_OTEL_PATH    default memory/runs.jsonl
    CLAUDE_ROUTINE    optional (set by routine wrapper)
    CLAUDE_SESSION_ID optional
    CLAUDE_PROMPT_ID  optional

Usage:
    python scripts/otel_log.py event trade.buy --symbol AAPL --qty 10 --price 175.20 --reason "CTQS 78"
    python scripts/otel_log.py event guard.reject --check fat_finger --symbol AAPL
    python scripts/otel_log.py tail --n 20
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path


OTEL_PATH = Path(os.environ.get("BULL_OTEL_PATH", "memory/runs.jsonl"))


def _now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def emit(event: str, payload: dict) -> dict:
    record = {
        "ts": _now_iso(),
        "event": event,
        "routine": os.environ.get("CLAUDE_ROUTINE"),
        "session_id": os.environ.get("CLAUDE_SESSION_ID"),
        "prompt_id": os.environ.get("CLAUDE_PROMPT_ID"),
        "payload": payload,
    }
    OTEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OTEL_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, default=str) + "\n")
    return record


def tail(n: int) -> list[dict]:
    if not OTEL_PATH.exists():
        return []
    lines = OTEL_PATH.read_text(encoding="utf-8").splitlines()[-n:]
    out = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="otel_log")
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("event", help="Append a structured event")
    e.add_argument("name", help="Event name, e.g. trade.buy / guard.reject / research.score")
    e.add_argument("--kv", action="append", default=[], help="key=value pairs")
    # Convenience flags (everything else flows through --kv)
    e.add_argument("--symbol")
    e.add_argument("--side")
    e.add_argument("--qty", type=float)
    e.add_argument("--price", type=float)
    e.add_argument("--reason")
    e.add_argument("--check")
    e.add_argument("--score", type=float)
    e.add_argument("--verdict")

    t = sub.add_parser("tail", help="Print last N events")
    t.add_argument("--n", type=int, default=20)

    args = p.parse_args(argv[1:])

    if args.cmd == "event":
        payload: dict = {}
        for k in ("symbol", "side", "qty", "price", "reason", "check", "score", "verdict"):
            v = getattr(args, k)
            if v is not None:
                payload[k] = v
        for kv in args.kv:
            if "=" not in kv:
                continue
            k, _, v = kv.partition("=")
            payload[k.strip()] = v.strip()
        rec = emit(args.name, payload)
        print(json.dumps(rec, indent=2))
        return 0

    if args.cmd == "tail":
        for r in tail(args.n):
            print(json.dumps(r))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
