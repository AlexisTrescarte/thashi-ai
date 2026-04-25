#!/usr/bin/env python3
"""News / source normalization layer (defensive: trust + sanitize).

Two purposes:
  1. Trust: is the URL on the whitelist of primary/quality sources?
  2. Sanitize: detect text patterns that look like prompt injection so the LLM
     does not blindly act on adversarial content fetched via WebFetch.

Usage:
    python scripts/news_normalize.py trust https://www.sec.gov/...
    python scripts/news_normalize.py scan --file /tmp/article.txt
    echo "ignore previous instructions" | python scripts/news_normalize.py scan --stdin

Whitelist policy: research skill should treat non-whitelist sources as tertiary
only. The `evolve` and `trade` skills should refuse to act on signals whose
sole source is non-whitelist.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import urlparse


PRIMARY_DOMAINS = frozenset({
    # US regulators / data
    "sec.gov", "fda.gov", "federalreserve.gov", "treasury.gov",
    "fred.stlouisfed.org", "bls.gov", "bea.gov", "dol.gov",
    "cmegroup.com", "cftc.gov", "finra.org",
    # EU
    "esma.europa.eu", "ecb.europa.eu", "europa.eu",
    # Wires / official
    "businesswire.com", "prnewswire.com", "globenewswire.com",
    # Broker / exchange
    "alpaca.markets", "nasdaq.com", "nyse.com",
    # Crypto primary
    "binance.com", "coinbase.com", "etherscan.io", "glassnode.com",
})

QUALITY_DOMAINS = frozenset({
    "reuters.com", "bloomberg.com", "ft.com", "wsj.com", "barrons.com",
    "cnbc.com", "marketwatch.com", "seekingalpha.com",
    "theblock.co", "coindesk.com", "decrypt.co", "coingecko.com",
})


INJECTION_PATTERNS = [
    re.compile(r"\bignore\s+(?:all\s+)?(?:previous|prior|above)\s+(?:instructions?|prompts?|rules?)", re.I),
    re.compile(r"\bdisregard\s+(?:all\s+)?(?:previous|prior|above)", re.I),
    re.compile(r"\byou\s+are\s+now\s+(?:a|an)\s+", re.I),
    re.compile(r"\bnew\s+(?:system|role|persona)\s*[:=]", re.I),
    re.compile(r"<\s*system\s*>", re.I),
    re.compile(r"\bassistant\s*:\s*", re.I),
    re.compile(r"\b(?:execute|run|invoke)\s+(?:this|the\s+following)\s+(?:command|tool|prompt)", re.I),
    re.compile(r"\bclaude[,\s]+(?:please\s+)?(?:buy|sell|trade|execute)", re.I),
    re.compile(r"```(?:bash|sh|python)\s*\n[^`]*?(?:rm\s|curl\s|wget\s|alpaca|api[_-]?key)", re.I),
    re.compile(r"\bAPI[_-]?KEY|\bSECRET[_-]?KEY|\bBEARER\s+[A-Za-z0-9._-]{20,}", re.I),
    re.compile(r"</?\|im_(?:start|end)\|>", re.I),
]


def _domain(url: str) -> str:
    try:
        netloc = urlparse(url).netloc.lower()
    except ValueError:
        return ""
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc


def trust_level(url: str) -> dict:
    d = _domain(url)
    if not d:
        return {"url": url, "domain": "", "tier": "unknown", "trusted": False}
    parts = d.split(".")
    suffix2 = ".".join(parts[-2:]) if len(parts) >= 2 else d
    suffix3 = ".".join(parts[-3:]) if len(parts) >= 3 else d
    for candidate in (d, suffix3, suffix2):
        if candidate in PRIMARY_DOMAINS:
            return {"url": url, "domain": d, "tier": "primary", "trusted": True}
        if candidate in QUALITY_DOMAINS:
            return {"url": url, "domain": d, "tier": "quality", "trusted": True}
    return {"url": url, "domain": d, "tier": "tertiary", "trusted": False}


def scan_text(text: str) -> dict:
    hits: list[dict] = []
    for pat in INJECTION_PATTERNS:
        for m in pat.finditer(text):
            hits.append({"pattern": pat.pattern, "match": m.group(0)[:120], "pos": m.start()})
    return {
        "suspicious": bool(hits),
        "hits": hits,
        "char_count": len(text),
        "line_count": text.count("\n") + 1,
    }


def sanitize(text: str) -> str:
    out = text
    for pat in INJECTION_PATTERNS:
        out = pat.sub("[REDACTED-SUSPICIOUS]", out)
    return out


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="news_normalize")
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("trust", help="Classify a URL: primary | quality | tertiary | unknown")
    t.add_argument("url")

    s = sub.add_parser("scan", help="Scan text for prompt-injection patterns")
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--file")
    g.add_argument("--stdin", action="store_true")
    s.add_argument("--sanitize", action="store_true", help="Also emit sanitized text")

    args = p.parse_args(argv[1:])

    if args.cmd == "trust":
        result = trust_level(args.url)
        print(json.dumps(result, indent=2))
        return 0 if result["trusted"] else 2

    if args.cmd == "scan":
        text = sys.stdin.read() if args.stdin else open(args.file, encoding="utf-8").read()
        result = scan_text(text)
        if args.sanitize:
            result["sanitized"] = sanitize(text)
        print(json.dumps(result, indent=2))
        return 0 if not result["suspicious"] else 2

    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
