#!/usr/bin/env python3
"""Snapshot portefeuille vs SPY.

Imprime en stdout un résumé Markdown destiné à être collé dans une notification
Telegram ou dans memory/portfolio.md.

Env: ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import alpaca_client as ac  # noqa: E402


def _pct(a: float, b: float) -> float:
    return (a - b) / b * 100.0 if b else 0.0


def build_snapshot() -> str:
    account = ac.get_account()
    positions = ac.get_positions()
    equity = float(account.get("equity", 0))
    cash = float(account.get("cash", 0))
    last_equity = float(account.get("last_equity", 0))
    day_pct = _pct(equity, last_equity)

    # SPY
    try:
        spy_q = ac.get_quote("SPY")
        spy_price = float(spy_q.get("quote", {}).get("ap") or spy_q.get("quote", {}).get("bp") or 0)
    except SystemExit:
        spy_price = 0.0

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    lines: list[str] = []
    lines.append(f"*Portfolio snapshot* — {now}")
    lines.append(f"Equity: `${equity:,.2f}` ({day_pct:+.2f}% aujourd'hui)")
    lines.append(f"Cash: `${cash:,.2f}` ({cash / equity * 100 if equity else 0:.1f}%)")
    lines.append(f"SPY ref: `${spy_price:,.2f}`")
    lines.append("")
    lines.append("*Positions* :")
    if not positions:
        lines.append("_aucune position ouverte_")
    else:
        for p in positions:
            sym = p.get("symbol", "?")
            qty = float(p.get("qty", 0))
            avg = float(p.get("avg_entry_price", 0))
            mv = float(p.get("market_value", 0))
            upl_pct = float(p.get("unrealized_plpc", 0)) * 100.0
            lines.append(f"- `{sym}` {qty:g} @ avg ${avg:,.2f} → ${mv:,.2f} ({upl_pct:+.2f}%)")
    return "\n".join(lines)


def main() -> int:
    print(build_snapshot())
    return 0


if __name__ == "__main__":
    sys.exit(main())
