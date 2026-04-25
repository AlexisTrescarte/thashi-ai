#!/usr/bin/env python3
"""Kill switch — file flag that blocks new BUY/ADD/TRIM until cleared.

The file `memory/killswitch.flag` (path overridable via BULL_KILLSWITCH_PATH)
contains a one-line reason. When present:
  - pretrade_guards.py rejects any BUY check
  - the trade skill should refuse to open new positions
  - CUT and STOP-UPDATE are still allowed (defensive exits must always work)

Usage:
    python scripts/killswitch.py status
    python scripts/killswitch.py activate "Earnings season — pause new opens"
    python scripts/killswitch.py deactivate

Activation is a deliberate human or routine action. Auto-defense at -20%
drawdown should activate this from the daily-review skill.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path


KILLSWITCH_PATH = Path(os.environ.get("BULL_KILLSWITCH_PATH", "memory/killswitch.flag"))


def status() -> dict:
    if not KILLSWITCH_PATH.exists():
        return {"active": False}
    text = KILLSWITCH_PATH.read_text(encoding="utf-8").strip()
    return {"active": True, "reason": text, "path": str(KILLSWITCH_PATH)}


def activate(reason: str) -> dict:
    if not reason or not reason.strip():
        raise SystemExit("activate requires a non-empty reason")
    KILLSWITCH_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    KILLSWITCH_PATH.write_text(f"{ts} {reason.strip()}\n", encoding="utf-8")
    return {"active": True, "reason": reason.strip(), "ts": ts}


def deactivate() -> dict:
    if KILLSWITCH_PATH.exists():
        KILLSWITCH_PATH.unlink()
    return {"active": False}


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="killswitch")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status")

    a = sub.add_parser("activate")
    a.add_argument("reason")

    sub.add_parser("deactivate")

    args = p.parse_args(argv[1:])

    if args.cmd == "status":
        print(json.dumps(status(), indent=2))
        return 0
    if args.cmd == "activate":
        print(json.dumps(activate(args.reason), indent=2))
        return 0
    if args.cmd == "deactivate":
        print(json.dumps(deactivate(), indent=2))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
