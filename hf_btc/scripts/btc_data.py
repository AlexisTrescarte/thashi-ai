#!/usr/bin/env python3
"""BTC/USD OHLCV + indicators (stdlib only).

Pulls bars from Alpaca crypto data API (free tier — IEX-equivalent crypto market data).
Computes RSI(14), MACD(12,26,9), Bollinger(20,2), ATR(14), EMA(20/50/200),
VWAP (session-anchored UTC midnight), Volume z-score(20).

Env: ALPACA_API_KEY, ALPACA_SECRET_KEY.

Usage:
    python btc_data.py snapshot                    # all 4 timeframes + indicators (JSON)
    python btc_data.py bars 5Min 200               # raw bars
    python btc_data.py indicators 5Min             # indicators on a single timeframe
"""

from __future__ import annotations

import json
import math
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any

DATA_BASE = "https://data.alpaca.markets"
SYMBOL = "BTC/USD"
TIMEFRAMES = ["1Min", "5Min", "15Min", "1Hour"]


def _headers() -> dict[str, str]:
    key = os.environ.get("ALPACA_API_KEY")
    secret = os.environ.get("ALPACA_SECRET_KEY")
    if not key or not secret:
        raise SystemExit("ALPACA_API_KEY / ALPACA_SECRET_KEY missing")
    return {
        "APCA-API-KEY-ID": key,
        "APCA-API-SECRET-KEY": secret,
        "Accept": "application/json",
    }


def _get(path: str, query: dict[str, Any]) -> Any:
    url = f"{DATA_BASE}/v1beta3/crypto/us/{path.lstrip('/')}?" + urllib.parse.urlencode(
        {k: v for k, v in query.items() if v is not None}
    )
    req = urllib.request.Request(url, method="GET", headers=_headers())
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Alpaca data HTTP {e.code}: {e.read().decode(errors='replace')}") from e


def get_bars(timeframe: str, limit: int = 200) -> list[dict[str, Any]]:
    """Return list of bars sorted oldest → newest, latest bar at the end.

    Paginates if needed (Alpaca caps a single page at ~1000 bars but may
    return fewer for older windows). Always pulls a recent window so the
    last bar is the current period.
    """
    minutes_per = {"1Min": 1, "5Min": 5, "15Min": 15, "1Hour": 60}.get(timeframe)
    if minutes_per is None:
        raise SystemExit(f"Unsupported timeframe: {timeframe}")

    end = datetime.now(timezone.utc)
    # Buffer 4× to be robust to thin trading windows and any API truncation.
    start = end - timedelta(minutes=minutes_per * limit * 4)

    bars: list[dict[str, Any]] = []
    page_token: str | None = None
    while True:
        payload = _get(
            "bars",
            query={
                "symbols": SYMBOL,
                "timeframe": timeframe,
                "limit": 1000,
                "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "sort": "asc",
                "page_token": page_token,
            },
        )
        page = payload.get("bars", {}).get(SYMBOL, [])
        bars.extend(page)
        page_token = payload.get("next_page_token")
        if not page_token or len(bars) >= limit * 5:
            break
    return bars[-limit:] if len(bars) > limit else bars


def get_latest_quote() -> dict[str, Any]:
    payload = _get("latest/quotes", query={"symbols": SYMBOL})
    return payload.get("quotes", {}).get(SYMBOL, {})


def get_latest_trade() -> dict[str, Any]:
    payload = _get("latest/trades", query={"symbols": SYMBOL})
    return payload.get("trades", {}).get(SYMBOL, {})


# ───────── indicators (stdlib math, no numpy) ─────────


def _ema(values: list[float], length: int) -> list[float]:
    if len(values) < length:
        return [float("nan")] * len(values)
    k = 2.0 / (length + 1)
    out: list[float] = [float("nan")] * (length - 1)
    seed = sum(values[:length]) / length
    out.append(seed)
    prev = seed
    for v in values[length:]:
        prev = v * k + prev * (1 - k)
        out.append(prev)
    return out


def _sma(values: list[float], length: int) -> list[float]:
    out: list[float] = []
    s = 0.0
    for i, v in enumerate(values):
        s += v
        if i >= length:
            s -= values[i - length]
        out.append(s / length if i >= length - 1 else float("nan"))
    return out


def _stddev(values: list[float], length: int) -> list[float]:
    out: list[float] = []
    for i in range(len(values)):
        if i < length - 1:
            out.append(float("nan"))
            continue
        window = values[i - length + 1 : i + 1]
        mean = sum(window) / length
        var = sum((x - mean) ** 2 for x in window) / length
        out.append(math.sqrt(var))
    return out


def rsi(closes: list[float], length: int = 14) -> float:
    if len(closes) < length + 1:
        return float("nan")
    gains, losses = [], []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    # Wilder smoothing
    avg_g = sum(gains[:length]) / length
    avg_l = sum(losses[:length]) / length
    for i in range(length, len(gains)):
        avg_g = (avg_g * (length - 1) + gains[i]) / length
        avg_l = (avg_l * (length - 1) + losses[i]) / length
    if avg_l == 0:
        return 100.0
    rs = avg_g / avg_l
    return 100.0 - (100.0 / (1.0 + rs))


def macd(closes: list[float], fast: int = 12, slow: int = 26, signal: int = 9) -> dict[str, float]:
    if len(closes) < slow + signal:
        return {"macd": float("nan"), "signal": float("nan"), "hist": float("nan")}
    ema_fast = _ema(closes, fast)
    ema_slow = _ema(closes, slow)
    macd_line = [
        (ema_fast[i] - ema_slow[i]) if not (math.isnan(ema_fast[i]) or math.isnan(ema_slow[i])) else float("nan")
        for i in range(len(closes))
    ]
    valid = [v for v in macd_line if not math.isnan(v)]
    sig = _ema(valid, signal)
    return {
        "macd": macd_line[-1],
        "signal": sig[-1] if sig and not math.isnan(sig[-1]) else float("nan"),
        "hist": macd_line[-1] - sig[-1] if sig and not math.isnan(sig[-1]) else float("nan"),
    }


def bollinger(closes: list[float], length: int = 20, k: float = 2.0) -> dict[str, float]:
    if len(closes) < length:
        return {"upper": float("nan"), "middle": float("nan"), "lower": float("nan"), "bandwidth_pct": float("nan"), "pct_b": float("nan")}
    sma = _sma(closes, length)
    sd = _stddev(closes, length)
    upper = sma[-1] + k * sd[-1]
    lower = sma[-1] - k * sd[-1]
    middle = sma[-1]
    bandwidth_pct = (upper - lower) / middle * 100 if middle else float("nan")
    pct_b = (closes[-1] - lower) / (upper - lower) if upper != lower else float("nan")
    return {"upper": upper, "middle": middle, "lower": lower, "bandwidth_pct": bandwidth_pct, "pct_b": pct_b}


def atr(highs: list[float], lows: list[float], closes: list[float], length: int = 14) -> float:
    if len(closes) < length + 1:
        return float("nan")
    trs = []
    for i in range(1, len(closes)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        trs.append(tr)
    avg = sum(trs[:length]) / length
    for v in trs[length:]:
        avg = (avg * (length - 1) + v) / length
    return avg


def vwap_session(bars: list[dict[str, Any]]) -> float:
    """Session-anchored VWAP — resets at UTC midnight."""
    if not bars:
        return float("nan")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    pv = 0.0
    vol = 0.0
    for b in bars:
        ts = b["t"][:10]
        if ts != today:
            continue
        typ = (b["h"] + b["l"] + b["c"]) / 3
        pv += typ * b["v"]
        vol += b["v"]
    return pv / vol if vol else float("nan")


def volume_zscore(volumes: list[float], length: int = 20) -> float:
    if len(volumes) < length:
        return float("nan")
    window = volumes[-length:]
    mean = sum(window) / length
    var = sum((v - mean) ** 2 for v in window) / length
    sd = math.sqrt(var)
    return (volumes[-1] - mean) / sd if sd else 0.0


def compute_indicators(bars: list[dict[str, Any]]) -> dict[str, Any]:
    if len(bars) < 30:
        return {"error": f"insufficient bars: {len(bars)}"}
    closes = [b["c"] for b in bars]
    highs = [b["h"] for b in bars]
    lows = [b["l"] for b in bars]
    vols = [b["v"] for b in bars]
    ema20 = _ema(closes, 20)[-1]
    ema50 = _ema(closes, 50)[-1] if len(closes) >= 50 else float("nan")
    ema200 = _ema(closes, 200)[-1] if len(closes) >= 200 else float("nan")
    last = closes[-1]

    def _rel(level: float) -> float:
        return ((last / level) - 1.0) * 100 if level and not math.isnan(level) else float("nan")

    return {
        "last_close": last,
        "rsi_14": rsi(closes, 14),
        "macd": macd(closes),
        "bollinger": bollinger(closes, 20, 2.0),
        "atr_14": atr(highs, lows, closes, 14),
        "atr_pct": atr(highs, lows, closes, 14) / last * 100 if last else float("nan"),
        "ema_20": ema20,
        "ema_50": ema50,
        "ema_200": ema200,
        "dist_ema20_pct": _rel(ema20),
        "dist_ema50_pct": _rel(ema50),
        "dist_ema200_pct": _rel(ema200),
        "vwap_session": vwap_session(bars),
        "dist_vwap_pct": _rel(vwap_session(bars)),
        "volume_z20": volume_zscore(vols, 20),
        "n_bars": len(bars),
        "first_ts": bars[0]["t"],
        "last_ts": bars[-1]["t"],
    }


def snapshot() -> dict[str, Any]:
    """Pull all 4 timeframes + indicators + latest quote/trade."""
    out: dict[str, Any] = {"symbol": SYMBOL, "snapshot_utc": datetime.now(timezone.utc).isoformat()}
    for tf in TIMEFRAMES:
        bars = get_bars(tf, limit=200)
        out[tf] = compute_indicators(bars)
    out["latest_quote"] = get_latest_quote()
    out["latest_trade"] = get_latest_trade()
    return out


def _pp(obj: Any) -> None:
    print(json.dumps(obj, indent=2, default=str))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "snapshot":
        _pp(snapshot())
    elif cmd == "bars":
        tf = argv[2] if len(argv) > 2 else "5Min"
        n = int(argv[3]) if len(argv) > 3 else 50
        _pp(get_bars(tf, n))
    elif cmd == "indicators":
        tf = argv[2] if len(argv) > 2 else "5Min"
        _pp(compute_indicators(get_bars(tf, 200)))
    else:
        print(f"Unknown: {cmd}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
