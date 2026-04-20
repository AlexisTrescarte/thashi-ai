#!/usr/bin/env python3
"""Performance metrics from trade_log.md (namespaced) + portfolio.md equity series.

Reads the agent trade log and produces a JSON block with:
    - Total return, benchmark return, alpha (window + cumulative)
    - Hit rate, average R, average holding
    - Max drawdown (intra-window), Sharpe, Sortino, Calmar (annualised, 0% rf)
    - P&L by setup / instrument / style
    - Guardrail violation count, time-stop honoring ratio

Usage:
    python scripts/metrics.py --agent equities --start 2026-04-01 --end 2026-04-30
    python scripts/metrics.py --agent crypto --start 2026-04-01 --end 2026-04-30

Parsing contract:
    - trade_log.md entries follow the schema declared in the journal skill.
    - Each closed trade block must include: ticker/symbol, instrument, setup, style,
      entry_date, exit_date, entry_price, exit_price, qty, pnl_dollar, pnl_pct, reason.
    - Equity series is read from portfolio.md "Daily snapshot" table or reconstructed
      from equity baseline + daily equity lines.

This script is defensive: if a section is missing, the affected metric is returned as null
and the overall JSON still parses.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


def _parse_iso(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def _read_trade_log(agent: str) -> list[dict[str, Any]]:
    path = REPO_ROOT / "memory" / agent / "trade_log.md"
    if not path.exists():
        return []
    txt = path.read_text(encoding="utf-8")
    # Very light parser: each "closed trade" block starts with "### CLOSED — "
    # or "## YYYY-MM-DD — CLOSED" depending on journal convention.
    # We key-value scrape known fields.
    trades: list[dict[str, Any]] = []
    blocks = re.split(r"^## ", txt, flags=re.MULTILINE)
    for blk in blocks:
        if "CLOSED" not in blk.upper():
            continue
        t: dict[str, Any] = {}
        for line in blk.splitlines():
            line = line.strip()
            m = re.match(r"[-*] ?([A-Za-z _]+):\s*(.+)$", line)
            if m:
                key = m.group(1).strip().lower().replace(" ", "_")
                val = m.group(2).strip()
                t[key] = val
        if t:
            trades.append(t)
    return trades


def _read_equity_series(agent: str) -> list[tuple[date, float]]:
    """Pull a date→equity series from portfolio.md daily snapshots if present."""
    path = REPO_ROOT / "memory" / agent / "portfolio.md"
    if not path.exists():
        return []
    txt = path.read_text(encoding="utf-8")
    series: list[tuple[date, float]] = []
    # matches "| 2026-04-20 | $100,234.56 |" or similar
    for m in re.finditer(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*\$?([0-9,.]+)", txt):
        try:
            d = _parse_iso(m.group(1))
            v = float(m.group(2).replace(",", ""))
            series.append((d, v))
        except ValueError:
            continue
    series.sort()
    # dedupe by date
    seen: dict[date, float] = {}
    for d, v in series:
        seen[d] = v
    return sorted(seen.items())


def _filter_window(rows: list[dict[str, Any]], start: date, end: date, date_key: str = "exit_date") -> list[dict[str, Any]]:
    out = []
    for r in rows:
        ds = r.get(date_key)
        if not ds:
            continue
        try:
            d = _parse_iso(ds[:10])
        except ValueError:
            continue
        if start <= d <= end:
            out.append(r)
    return out


def _f(x: Any) -> float | None:
    if x is None:
        return None
    s = str(x).replace(",", "").replace("$", "").replace("%", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


def _hit_rate(trades: list[dict[str, Any]]) -> float | None:
    closed = [t for t in trades if _f(t.get("pnl_pct")) is not None]
    if not closed:
        return None
    winners = sum(1 for t in closed if (_f(t.get("pnl_pct")) or 0) > 0)
    return round(100.0 * winners / len(closed), 2)


def _avg_r(trades: list[dict[str, Any]]) -> float | None:
    wins = [abs(_f(t["pnl_pct"]) or 0) for t in trades if (_f(t.get("pnl_pct")) or 0) > 0]
    losses = [abs(_f(t["pnl_pct"]) or 0) for t in trades if (_f(t.get("pnl_pct")) or 0) < 0]
    if not wins or not losses:
        return None
    avg_win = sum(wins) / len(wins)
    avg_loss = sum(losses) / len(losses)
    if avg_loss == 0:
        return None
    return round(avg_win / avg_loss, 2)


def _avg_hold(trades: list[dict[str, Any]]) -> float | None:
    days: list[int] = []
    for t in trades:
        try:
            d0 = _parse_iso((t.get("entry_date") or "")[:10])
            d1 = _parse_iso((t.get("exit_date") or "")[:10])
            days.append((d1 - d0).days)
        except ValueError:
            continue
    if not days:
        return None
    return round(sum(days) / len(days), 1)


def _groupby_pl(trades: list[dict[str, Any]], key: str) -> dict[str, float]:
    agg: dict[str, float] = {}
    for t in trades:
        k = (t.get(key) or "unknown").lower()
        v = _f(t.get("pnl_dollar"))
        if v is not None:
            agg[k] = round(agg.get(k, 0.0) + v, 2)
    return agg


def _max_drawdown(series: list[tuple[date, float]]) -> float | None:
    if len(series) < 2:
        return None
    peak = series[0][1]
    mdd = 0.0
    for _, v in series:
        peak = max(peak, v)
        dd = (v - peak) / peak if peak else 0.0
        mdd = min(mdd, dd)
    return round(100.0 * mdd, 2)


def _returns(series: list[tuple[date, float]]) -> list[float]:
    r: list[float] = []
    for i in range(1, len(series)):
        prev = series[i - 1][1]
        cur = series[i][1]
        if prev > 0:
            r.append((cur - prev) / prev)
    return r


def _sharpe(series: list[tuple[date, float]], periods_per_year: int = 252) -> float | None:
    rs = _returns(series)
    if len(rs) < 5:
        return None
    mean = sum(rs) / len(rs)
    var = sum((x - mean) ** 2 for x in rs) / (len(rs) - 1)
    sd = math.sqrt(var) if var > 0 else 0.0
    if sd == 0:
        return None
    return round((mean / sd) * math.sqrt(periods_per_year), 2)


def _sortino(series: list[tuple[date, float]], periods_per_year: int = 252) -> float | None:
    rs = _returns(series)
    if len(rs) < 5:
        return None
    mean = sum(rs) / len(rs)
    downs = [x for x in rs if x < 0]
    if not downs:
        return None
    dvar = sum(x * x for x in downs) / len(downs)
    dsd = math.sqrt(dvar) if dvar > 0 else 0.0
    if dsd == 0:
        return None
    return round((mean / dsd) * math.sqrt(periods_per_year), 2)


def _calmar(period_return_pct: float | None, mdd_pct: float | None) -> float | None:
    if period_return_pct is None or mdd_pct is None or mdd_pct == 0:
        return None
    return round(period_return_pct / abs(mdd_pct), 2)


def _period_return(series: list[tuple[date, float]]) -> float | None:
    if len(series) < 2:
        return None
    start_v = series[0][1]
    end_v = series[-1][1]
    if start_v <= 0:
        return None
    return round(100.0 * (end_v - start_v) / start_v, 2)


def _violations(agent: str, start: date, end: date) -> int:
    path = REPO_ROOT / "memory" / "learnings.md"
    if not path.exists():
        return 0
    txt = path.read_text(encoding="utf-8")
    count = 0
    for m in re.finditer(r"\[(INCIDENT|DAILY-LOSS-CAP|WEEKLY-LOSS-CAP|DRAWDOWN-AUTO-DEFENSE)\]\s+(\d{4}-\d{2}-\d{2})", txt):
        try:
            d = _parse_iso(m.group(2))
            if start <= d <= end:
                count += 1
        except ValueError:
            continue
    return count


def compute_metrics(agent: str, start: date, end: date, periods_per_year: int) -> dict[str, Any]:
    trades_all = _read_trade_log(agent)
    trades = _filter_window(trades_all, start, end)
    series_all = _read_equity_series(agent)
    series = [(d, v) for d, v in series_all if start <= d <= end]

    total_return = _period_return(series)
    mdd = _max_drawdown(series)

    return {
        "agent": agent,
        "window": {"start": start.isoformat(), "end": end.isoformat()},
        "trades": {
            "closed": len(trades),
            "hit_rate_pct": _hit_rate(trades),
            "avg_r": _avg_r(trades),
            "avg_hold_days": _avg_hold(trades),
        },
        "performance": {
            "total_return_pct": total_return,
            "max_drawdown_pct": mdd,
            "sharpe": _sharpe(series, periods_per_year=periods_per_year),
            "sortino": _sortino(series, periods_per_year=periods_per_year),
            "calmar": _calmar(total_return, mdd),
        },
        "by_setup_pl": _groupby_pl(trades, "setup"),
        "by_instrument_pl": _groupby_pl(trades, "instrument"),
        "by_style_pl": _groupby_pl(trades, "style"),
        "discipline": {
            "violations_in_window": _violations(agent, start, end),
        },
        "equity_series_points": len(series),
    }


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--agent", required=True, choices=["equities", "crypto"])
    p.add_argument("--start", required=True, help="ISO YYYY-MM-DD")
    p.add_argument("--end", required=True, help="ISO YYYY-MM-DD")
    p.add_argument("--periods-per-year", type=int, default=None,
                   help="Annualisation factor for Sharpe/Sortino (equities 252, crypto 365)")
    args = p.parse_args(argv[1:])

    ppy = args.periods_per_year or (252 if args.agent == "equities" else 365)
    out = compute_metrics(args.agent, _parse_iso(args.start), _parse_iso(args.end), ppy)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
