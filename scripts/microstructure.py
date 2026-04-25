#!/usr/bin/env python3
"""Microstructure confirmation layer for entry/exit decisions.

Computes from Alpaca quote endpoint:
  - spread (bps)
  - queue imbalance: (bid_size - ask_size) / (bid_size + ask_size), in [-1, +1]

Verdict (CONFIRM | NEUTRAL | BLOCK):
  BUY confirms when QI > qi_threshold and spread <= max_spread_bps.
  SELL confirms when QI < -qi_threshold and spread <= max_spread_bps.
  Otherwise NEUTRAL (no signal) or BLOCK (spread too wide).

This is a defensive arbiter, not a signal generator. Negative QI on a BUY does
not block (the LLM may still have a strong reason); it is reported as NEUTRAL
unless explicitly run with --strict, which converts NEUTRAL into BLOCK.

Usage:
    python scripts/microstructure.py confirm AAPL buy
    python scripts/microstructure.py confirm AAPL buy --strict --qi 0.20 --max-spread-bps 50
    python scripts/microstructure.py snapshot AAPL
"""

from __future__ import annotations

import argparse
import json
import sys

import alpaca_client


DEFAULT_QI_THRESHOLD = 0.10
DEFAULT_MAX_SPREAD_BPS = 30.0


def spread_bps(bid: float, ask: float) -> float | None:
    if bid <= 0 or ask <= 0 or ask < bid:
        return None
    mid = (bid + ask) / 2.0
    return (ask - bid) / mid * 10000.0


def queue_imbalance(bid_size: float, ask_size: float) -> float | None:
    total = bid_size + ask_size
    if total <= 0:
        return None
    return (bid_size - ask_size) / total


def fetch_snapshot(symbol: str) -> dict:
    raw = alpaca_client.get_quote(symbol)
    quote = raw.get("quote", raw) if isinstance(raw, dict) else {}
    bid = float(quote.get("bp") or quote.get("bid_price") or 0.0)
    ask = float(quote.get("ap") or quote.get("ask_price") or 0.0)
    bid_size = float(quote.get("bs") or quote.get("bid_size") or 0.0)
    ask_size = float(quote.get("as") or quote.get("ask_size") or 0.0)
    ts = quote.get("t") or quote.get("timestamp")

    sb = spread_bps(bid, ask)
    qi = queue_imbalance(bid_size, ask_size)
    mid = (bid + ask) / 2.0 if bid and ask else None

    return {
        "symbol": symbol.upper(),
        "ts": ts,
        "bid": bid,
        "ask": ask,
        "bid_size": bid_size,
        "ask_size": ask_size,
        "mid": mid,
        "spread_bps": sb,
        "queue_imbalance": qi,
    }


def confirm(symbol: str, side: str, qi_threshold: float, max_spread_bps: float, strict: bool) -> dict:
    snap = fetch_snapshot(symbol)
    side = side.lower()
    sb = snap["spread_bps"]
    qi = snap["queue_imbalance"]

    verdict = "NEUTRAL"
    reasons: list[str] = []

    if sb is None:
        verdict = "BLOCK"
        reasons.append("spread unavailable")
    elif sb > max_spread_bps:
        verdict = "BLOCK"
        reasons.append(f"spread {sb:.1f} bps > {max_spread_bps} bps")

    if verdict != "BLOCK":
        if qi is None:
            reasons.append("queue imbalance unavailable")
        else:
            if side == "buy":
                if qi > qi_threshold:
                    verdict = "CONFIRM"
                    reasons.append(f"QI +{qi:.3f} > +{qi_threshold} (bid pressure aligns with buy)")
                elif qi < -qi_threshold:
                    verdict = "BLOCK" if strict else "NEUTRAL"
                    reasons.append(f"QI {qi:.3f} < -{qi_threshold} (ask pressure against buy)")
                else:
                    reasons.append(f"QI {qi:.3f} within +/-{qi_threshold} (no edge)")
            elif side == "sell":
                if qi < -qi_threshold:
                    verdict = "CONFIRM"
                    reasons.append(f"QI {qi:.3f} < -{qi_threshold} (ask pressure aligns with sell)")
                elif qi > qi_threshold:
                    verdict = "BLOCK" if strict else "NEUTRAL"
                    reasons.append(f"QI +{qi:.3f} > +{qi_threshold} (bid pressure against sell)")
                else:
                    reasons.append(f"QI {qi:.3f} within +/-{qi_threshold} (no edge)")
            else:
                verdict = "BLOCK"
                reasons.append(f"unknown side: {side}")

    return {
        "verdict": verdict,
        "side": side,
        "snapshot": snap,
        "thresholds": {"qi": qi_threshold, "max_spread_bps": max_spread_bps, "strict": strict},
        "reasons": reasons,
    }


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="microstructure")
    sub = p.add_subparsers(dest="cmd", required=True)

    snap = sub.add_parser("snapshot", help="Print bid/ask/sizes/spread/QI for a symbol")
    snap.add_argument("symbol")

    conf = sub.add_parser("confirm", help="Verdict CONFIRM/NEUTRAL/BLOCK for a side")
    conf.add_argument("symbol")
    conf.add_argument("side", choices=["buy", "sell"])
    conf.add_argument("--qi", type=float, default=DEFAULT_QI_THRESHOLD)
    conf.add_argument("--max-spread-bps", type=float, default=DEFAULT_MAX_SPREAD_BPS)
    conf.add_argument("--strict", action="store_true", help="Treat opposing QI as BLOCK instead of NEUTRAL")

    args = p.parse_args(argv[1:])

    if args.cmd == "snapshot":
        print(json.dumps(fetch_snapshot(args.symbol), indent=2))
        return 0

    if args.cmd == "confirm":
        out = confirm(args.symbol, args.side, args.qi, args.max_spread_bps, args.strict)
        print(json.dumps(out, indent=2))
        return 0 if out["verdict"] != "BLOCK" else 2

    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
