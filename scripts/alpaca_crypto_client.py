#!/usr/bin/env python3
"""Alpaca crypto client (stdlib only).

Reads ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL from environment.

Usage:
    python scripts/alpaca_crypto_client.py account
    python scripts/alpaca_crypto_client.py positions
    python scripts/alpaca_crypto_client.py orders [--status open|closed|all]
    python scripts/alpaca_crypto_client.py quote BTC/USD
    python scripts/alpaca_crypto_client.py buy BTC/USD 0.05      # market, gtc
    python scripts/alpaca_crypto_client.py sell BTC/USD 0.05
    python scripts/alpaca_crypto_client.py trailing-stop BTC/USD 0.05 5   # 5% trail
    python scripts/alpaca_crypto_client.py cancel <order_id>
    python scripts/alpaca_crypto_client.py close BTC/USD

Approved universe (immutable, enforced by crypto-hourly command):
    BTC/USD, ETH/USD, SOL/USD, LINK/USD, AVAX/USD, DOT/USD, MATIC/USD
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


APPROVED = {"BTC/USD", "ETH/USD", "SOL/USD", "LINK/USD", "AVAX/USD", "DOT/USD", "MATIC/USD"}

TRADING_BASE = os.environ.get("ALPACA_BASE_URL", "https://paper-api.alpaca.markets").rstrip("/")
DATA_BASE = "https://data.alpaca.markets"


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
    url = f"{DATA_BASE}/v1beta3/crypto/us/{path.lstrip('/')}"
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})
    return _request("GET", url)


def _enforce_universe(symbol: str) -> str:
    s = symbol.upper()
    if s not in APPROVED:
        raise SystemExit(f"Refused: {s} outside approved universe {sorted(APPROVED)}")
    return s


def get_account() -> dict[str, Any]:
    return _trading("account")


def get_positions() -> list[dict[str, Any]]:
    allp = _trading("positions")
    return [p for p in allp if p.get("asset_class") == "crypto"]


def get_orders(status: str = "open", limit: int = 50) -> list[dict[str, Any]]:
    return _trading("orders", query={"status": status, "limit": limit, "direction": "desc", "asset_class": "crypto"})


def get_quote(symbol: str) -> dict[str, Any]:
    s = _enforce_universe(symbol)
    return _data("latest/quotes", query={"symbols": s})


def place_market_order(symbol: str, qty: float, side: str) -> dict[str, Any]:
    s = _enforce_universe(symbol)
    if side not in ("buy", "sell"):
        raise SystemExit(f"Refused: side={side}. Spot only (buy/sell).")
    return _trading("orders", method="POST", body={
        "symbol": s,
        "qty": str(qty),
        "side": side,
        "type": "market",
        "time_in_force": "gtc",
    })


def place_trailing_stop(symbol: str, qty: float, trail_percent: float) -> dict[str, Any]:
    """Note: Alpaca crypto support for native trailing stops is limited.
    If this fails, the hourly routine must manage manual-trailing."""
    s = _enforce_universe(symbol)
    return _trading("orders", method="POST", body={
        "symbol": s,
        "qty": str(qty),
        "side": "sell",
        "type": "trailing_stop",
        "trail_percent": str(trail_percent),
        "time_in_force": "gtc",
    })


def cancel_order(order_id: str) -> dict[str, Any]:
    return _trading(f"orders/{order_id}", method="DELETE")


def close_position(symbol: str) -> dict[str, Any]:
    s = _enforce_universe(symbol)
    return _trading(f"positions/{urllib.parse.quote(s, safe='')}", method="DELETE")


def _pp(obj: Any) -> None:
    print(json.dumps(obj, indent=2, default=str))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    try:
        if cmd == "account":
            _pp(get_account())
        elif cmd == "positions":
            _pp(get_positions())
        elif cmd == "orders":
            status = "open"
            if "--status" in argv:
                status = argv[argv.index("--status") + 1]
            _pp(get_orders(status=status))
        elif cmd == "quote":
            _pp(get_quote(argv[2]))
        elif cmd == "buy":
            _pp(place_market_order(argv[2], float(argv[3]), "buy"))
        elif cmd == "sell":
            _pp(place_market_order(argv[2], float(argv[3]), "sell"))
        elif cmd == "trailing-stop":
            _pp(place_trailing_stop(argv[2], float(argv[3]), float(argv[4])))
        elif cmd == "cancel":
            _pp(cancel_order(argv[2]))
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
