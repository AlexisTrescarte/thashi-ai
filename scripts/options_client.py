#!/usr/bin/env python3
"""Alpaca options client (stdlib only). Single-leg long calls/puts only.

Reads ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL from environment.

Usage:
    python scripts/options_client.py chain AAPL 2026-05-16     # list contracts for expiry
    python scripts/options_client.py quote AAPL260516C00200000 # single-contract latest quote
    python scripts/options_client.py buy AAPL260516C00200000 2 --limit 3.25
    python scripts/options_client.py sell AAPL260516C00200000 2
    python scripts/options_client.py close AAPL260516C00200000
    python scripts/options_client.py positions
    python scripts/options_client.py orders [--status open|closed|all]

Policy (enforced by trade skill, not here):
    - Long options only (single-leg call or put). No spreads, no naked shorts.
    - DTE 7-60 at entry.
    - Premium stop: cut at -50% of entry premium.
    - Time stop: cut at DTE-3 regardless of P&L.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


TRADING_BASE = os.environ.get("ALPACA_BASE_URL", "https://paper-api.alpaca.markets").rstrip("/")
DATA_BASE = "https://data.alpaca.markets"

OCC_RE = re.compile(r"^[A-Z]{1,6}\d{6}[CP]\d{8}$")


def _headers() -> dict[str, str]:
    key = os.environ.get("ALPACA_API_KEY")
    secret = os.environ.get("ALPACA_SECRET_KEY")
    if not key or not secret:
        raise SystemExit("ALPACA_API_KEY / ALPACA_SECRET_KEY missing in environment")
    return {
        "APCA-API-KEY-ID": key,
        "APCA-API-SECRET-KEY": secret,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _request(method: str, url: str, body: dict[str, Any] | None = None) -> Any:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=_headers())
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        payload = e.read().decode(errors="replace")
        raise SystemExit(f"Alpaca HTTP {e.code} on {method} {url}: {payload}") from e
    except urllib.error.URLError as e:
        raise SystemExit(f"Alpaca network: {e.reason}") from e


def _trading(path: str, method: str = "GET", body: dict[str, Any] | None = None, query: dict[str, Any] | None = None) -> Any:
    url = f"{TRADING_BASE}/v2/{path.lstrip('/')}"
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})
    return _request(method, url, body)


def _data(path: str, query: dict[str, Any] | None = None) -> Any:
    url = f"{DATA_BASE}/v1beta1/options/{path.lstrip('/')}"
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})
    return _request("GET", url)


def _enforce_occ(symbol: str) -> str:
    s = symbol.upper()
    if not OCC_RE.match(s):
        raise SystemExit(f"Refused: {s} not in OCC format (e.g. AAPL260516C00200000)")
    return s


def get_chain(underlying: str, expiration: str) -> Any:
    """expiration YYYY-MM-DD. Returns contract list."""
    return _trading("options/contracts", query={"underlying_symbols": underlying.upper(), "expiration_date": expiration, "status": "active", "limit": 1000})


def get_quote(symbol: str) -> Any:
    s = _enforce_occ(symbol)
    return _data("quotes/latest", query={"symbols": s})


def get_positions() -> list[dict[str, Any]]:
    allp = _trading("positions")
    return [p for p in allp if p.get("asset_class") == "us_option"]


def get_orders(status: str = "open", limit: int = 50) -> list[dict[str, Any]]:
    return _trading("orders", query={"status": status, "limit": limit, "direction": "desc"})


def place_order(symbol: str, qty: int, side: str, limit: float | None = None) -> dict[str, Any]:
    """Long options only: side in (buy, sell). 'sell' only to close or to open a protective? No — enforced at skill level."""
    s = _enforce_occ(symbol)
    if side not in ("buy", "sell"):
        raise SystemExit(f"Refused: side={side}")
    body: dict[str, Any] = {
        "symbol": s,
        "qty": str(int(qty)),
        "side": side,
        "time_in_force": "day",
    }
    if limit is not None:
        body["type"] = "limit"
        body["limit_price"] = str(limit)
    else:
        body["type"] = "market"
    return _trading("orders", method="POST", body=body)


def close_position(symbol: str) -> dict[str, Any]:
    s = _enforce_occ(symbol)
    return _trading(f"positions/{s}", method="DELETE")


def _pp(obj: Any) -> None:
    print(json.dumps(obj, indent=2, default=str))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    try:
        if cmd == "chain":
            _pp(get_chain(argv[2], argv[3]))
        elif cmd == "quote":
            _pp(get_quote(argv[2]))
        elif cmd == "positions":
            _pp(get_positions())
        elif cmd == "orders":
            status = "open"
            if "--status" in argv:
                status = argv[argv.index("--status") + 1]
            _pp(get_orders(status=status))
        elif cmd == "buy":
            limit = None
            if "--limit" in argv:
                limit = float(argv[argv.index("--limit") + 1])
            _pp(place_order(argv[2], int(argv[3]), "buy", limit=limit))
        elif cmd == "sell":
            limit = None
            if "--limit" in argv:
                limit = float(argv[argv.index("--limit") + 1])
            _pp(place_order(argv[2], int(argv[3]), "sell", limit=limit))
        elif cmd == "close":
            _pp(close_position(argv[2]))
        else:
            print(f"Unknown command: {cmd}")
            return 1
    except IndexError:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
