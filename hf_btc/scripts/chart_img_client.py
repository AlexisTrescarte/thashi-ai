#!/usr/bin/env python3
"""chart-img.com client + daily quota guard.

Daily plan limits (subscription):
  - 50 calls / day
  - 1 / sec rate limit
  - 3 max parameters (studies)
  - 800x600 max resolution

Quota strategy (state/chart_img_quota.json):
  - 24 baseline slots/day (1 per UTC hour, on the hour)
  - 24 opportunistic slots/day (gated on numerical signal strength)
  - hard cap 48 — leaves 2 in plan reserve

Env: CHART_IMG_API_KEY.

Usage:
    python chart_img_client.py fetch BTCUSD 5m --reason baseline
    python chart_img_client.py fetch BTCUSD 15m --reason signal
    python chart_img_client.py quota
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

API_URL = "https://api.chart-img.com/v2/tradingview/advanced-chart/storage"
STATE_DIR = Path(__file__).resolve().parent.parent / "state"
QUOTA_FILE = STATE_DIR / "chart_img_quota.json"
CHARTS_DIR = STATE_DIR / "charts"

INTERVAL_MAP = {
    "1m": "1m", "3m": "3m", "5m": "5m", "15m": "15m", "30m": "30m",
    "1h": "1h", "2h": "2h", "4h": "4h", "1d": "1D", "1w": "1W",
}


def _key() -> str:
    k = os.environ.get("CHART_IMG_API_KEY")
    if not k:
        raise SystemExit("CHART_IMG_API_KEY missing")
    return k


def _load_quota() -> dict[str, Any]:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if not QUOTA_FILE.exists():
        return {
            "date_utc": today, "baseline_used": 0, "opportunistic_used": 0,
            "baseline_cap": 24, "opportunistic_cap": 24, "hard_cap": 48, "history": [],
        }
    q = json.loads(QUOTA_FILE.read_text())
    if q.get("date_utc") != today:
        q.update({"date_utc": today, "baseline_used": 0, "opportunistic_used": 0, "history": []})
    return q


def _save_quota(q: dict[str, Any]) -> None:
    QUOTA_FILE.write_text(json.dumps(q, indent=2))


def quota_status() -> dict[str, Any]:
    return _load_quota()


def _can_consume(reason: str, q: dict[str, Any]) -> tuple[bool, str]:
    total_used = q["baseline_used"] + q["opportunistic_used"]
    if total_used >= q["hard_cap"]:
        return False, f"hard_cap reached ({q['hard_cap']})"
    if reason == "baseline":
        if q["baseline_used"] >= q["baseline_cap"]:
            return False, f"baseline cap reached ({q['baseline_cap']})"
    elif reason == "signal":
        if q["opportunistic_used"] >= q["opportunistic_cap"]:
            return False, f"opportunistic cap reached ({q['opportunistic_cap']})"
    else:
        return False, f"unknown reason: {reason}"
    return True, "ok"


def fetch(
    symbol: str = "BINANCE:BTCUSDT",
    interval: str = "5m",
    reason: str = "signal",
    height: int = 600,
    width: int = 800,
) -> dict[str, Any]:
    """Fetch a chart, save PNG, update quota. Returns {ok, path, reason, quota_after}."""
    q = _load_quota()
    can, why = _can_consume(reason, q)
    if not can:
        return {"ok": False, "skipped": True, "why": why, "quota": q}

    tv_interval = INTERVAL_MAP.get(interval.lower())
    if not tv_interval:
        return {"ok": False, "skipped": True, "why": f"bad interval: {interval}"}

    body = {
        "symbol": symbol,
        "interval": tv_interval,
        "theme": "dark",
        "height": min(height, 600),
        "width": min(width, 800),
        "studies": [
            {"name": "Volume"},
            {"name": "Relative Strength Index", "input": {"length": 14}},
            {"name": "MACD"},
        ],
    }

    headers = {
        "x-api-key": _key(),
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    req = urllib.request.Request(
        API_URL, data=json.dumps(body).encode(), method="POST", headers=headers
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode(errors="replace")
        return {"ok": False, "error": f"HTTP {e.code}: {body_txt}"}
    except urllib.error.URLError as e:
        return {"ok": False, "error": f"network: {e.reason}"}

    img_url = data.get("url")
    if not img_url:
        return {"ok": False, "error": f"no url in response: {data}"}

    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fname = f"{ts}_{interval}_{reason}.png"
    fpath = CHARTS_DIR / fname

    try:
        with urllib.request.urlopen(img_url, timeout=20) as r:
            fpath.write_bytes(r.read())
    except urllib.error.URLError as e:
        return {"ok": False, "error": f"image download: {e.reason}"}

    if reason == "baseline":
        q["baseline_used"] += 1
    else:
        q["opportunistic_used"] += 1
    q["history"].append({"ts": ts, "interval": interval, "reason": reason, "file": fname})
    _save_quota(q)

    return {"ok": True, "path": str(fpath), "reason": reason, "quota": q}


def _pp(obj: Any) -> None:
    print(json.dumps(obj, indent=2, default=str))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "fetch":
        symbol_arg = argv[2] if len(argv) > 2 else "BTCUSD"
        symbol = "BINANCE:BTCUSDT" if symbol_arg.upper() in ("BTCUSD", "BTC/USD", "BTC") else symbol_arg
        interval = argv[3] if len(argv) > 3 else "5m"
        reason = "baseline"
        if "--reason" in argv:
            reason = argv[argv.index("--reason") + 1]
        time.sleep(1.1)
        _pp(fetch(symbol=symbol, interval=interval, reason=reason))
    elif cmd == "quota":
        _pp(quota_status())
    else:
        print(f"Unknown: {cmd}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
