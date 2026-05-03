#!/usr/bin/env python3
"""Telegram client for Bull-HF-BTC. Supports text + photo attachment.

Header: *BTC-HF CLAUDE* — distinct from Bull-equities and the Codex HF loop.

Env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID.

Usage:
    python telegram_hf.py send "*Bull-HF-BTC* test"
    python telegram_hf.py send_photo /path/img.png "caption *bold*"
    python telegram_hf.py heartbeat            # uses last sim snapshot
"""

from __future__ import annotations

import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

API_BASE = "https://api.telegram.org"


def _token() -> str:
    t = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not t:
        raise SystemExit("TELEGRAM_BOT_TOKEN missing")
    return t


def _chat() -> str:
    c = os.environ.get("TELEGRAM_CHAT_ID")
    if not c:
        raise SystemExit("TELEGRAM_CHAT_ID missing")
    return c


def send_message(text: str, parse_mode: str = "Markdown") -> dict[str, Any]:
    url = f"{API_BASE}/bot{_token()}/sendMessage"
    body = json.dumps({
        "chat_id": _chat(), "text": text, "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }).encode()
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}: {e.read().decode(errors='replace')}"}
    except urllib.error.URLError as e:
        return {"ok": False, "error": f"network: {e.reason}"}


def send_photo(image_path: str, caption: str = "", parse_mode: str = "Markdown") -> dict[str, Any]:
    """Multipart upload — stdlib only."""
    url = f"{API_BASE}/bot{_token()}/sendPhoto"
    boundary = uuid.uuid4().hex
    sep = f"--{boundary}".encode()
    end = f"--{boundary}--".encode()
    nl = b"\r\n"

    p = Path(image_path)
    if not p.exists():
        return {"ok": False, "error": f"file not found: {image_path}"}
    img_bytes = p.read_bytes()
    mime = mimetypes.guess_type(p.name)[0] or "image/png"

    parts = bytearray()

    def add_field(name: str, value: str) -> None:
        parts.extend(sep + nl)
        parts.extend(f'Content-Disposition: form-data; name="{name}"'.encode() + nl + nl)
        parts.extend(value.encode() + nl)

    add_field("chat_id", _chat())
    if caption:
        add_field("caption", caption)
        add_field("parse_mode", parse_mode)

    parts.extend(sep + nl)
    parts.extend(f'Content-Disposition: form-data; name="photo"; filename="{p.name}"'.encode() + nl)
    parts.extend(f"Content-Type: {mime}".encode() + nl + nl)
    parts.extend(img_bytes + nl)
    parts.extend(end + nl)

    req = urllib.request.Request(
        url, data=bytes(parts), method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}: {e.read().decode(errors='replace')}"}
    except urllib.error.URLError as e:
        return {"ok": False, "error": f"network: {e.reason}"}


def escape_md(s: str) -> str:
    """Escape Telegram Markdown reserved chars in a value (not the whole message)."""
    for ch in ("_", "*", "`", "["):
        s = s.replace(ch, f"\\{ch}")
    return s


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "send":
        text = argv[2] if len(argv) > 2 else sys.stdin.read()
        print(json.dumps(send_message(text), indent=2))
    elif cmd == "send_photo":
        path = argv[2]
        caption = argv[3] if len(argv) > 3 else ""
        print(json.dumps(send_photo(path, caption), indent=2))
    else:
        print(f"Unknown: {cmd}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
