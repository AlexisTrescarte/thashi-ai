#!/usr/bin/env python3
"""Client Telegram minimal (stdlib uniquement).

Env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID.

Usage:
    python scripts/telegram_client.py ping
    python scripts/telegram_client.py send "Message ici"
    echo "Message" | python scripts/telegram_client.py send -

Markdown activé par défaut (parse_mode=Markdown). Les underscores/asterisks/backticks
doivent être échappés avec un backslash pour ne pas être interprétés en italique/gras/code.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request


API_BASE = "https://api.telegram.org"


def _token() -> str:
    t = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not t:
        raise SystemExit("TELEGRAM_BOT_TOKEN manquant")
    return t


def _chat() -> str:
    c = os.environ.get("TELEGRAM_CHAT_ID")
    if not c:
        raise SystemExit("TELEGRAM_CHAT_ID manquant")
    return c


def send_message(text: str, parse_mode: str = "Markdown", disable_preview: bool = True) -> dict:
    url = f"{API_BASE}/bot{_token()}/sendMessage"
    body = json.dumps({
        "chat_id": _chat(),
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": disable_preview,
    }).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Telegram HTTP {e.code}: {e.read().decode(errors='replace')}") from e


def get_updates() -> dict:
    url = f"{API_BASE}/bot{_token()}/getUpdates"
    with urllib.request.urlopen(url, timeout=15) as resp:
        return json.loads(resp.read())


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "ping":
        print(json.dumps(send_message("*Bull* : ping ✅"), indent=2))
    elif cmd == "send":
        if len(argv) < 3:
            print("Usage: send '<text>' | send -")
            return 1
        text = sys.stdin.read() if argv[2] == "-" else argv[2]
        print(json.dumps(send_message(text), indent=2))
    elif cmd == "updates":
        print(json.dumps(get_updates(), indent=2))
    else:
        print(f"Inconnu: {cmd}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
