#!/usr/bin/env python3
"""Prompt-evolution proposal manager: list, validate diff, apply, block.

The `evolve` skill uses this helper to run the G1-G8 gates over pending proposals
queued in memory/prompt_evolution_proposals.md.

Usage:
    python scripts/prompt_evolution.py list [--state proposed|applied|blocked]
    python scripts/prompt_evolution.py validate <proposal_id>
    python scripts/prompt_evolution.py apply <proposal_id>
    python scripts/prompt_evolution.py block <proposal_id> --reason "G4: raised hard cap"

Proposal schema (in memory/prompt_evolution_proposals.md):

    ## P-YYYYMMDD-NNN — {short title}
    **State**: proposed
    **Origin**: {monthly-deep-review | quarterly-rewrite}
    **Agent**: {equities | crypto}
    **Target**: {relative file path}
    **Rationale**: ...
    **Evidence**: {metric numbers + sample window}
    **Revert trigger**: {metric + threshold}
    **Diff**:
    ```diff
    --- a/path
    +++ b/path
    @@ -X,Y +X,Y @@
     context
    -old
    +new
    ```

The G4 keyword gate runs here; G1/G2/G5/G6 live in evolve skill (cross-file).
G7/G8 checked here (evidence + revert trigger non-empty).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROPOSALS = REPO_ROOT / "memory" / "prompt_evolution_proposals.md"
LEDGER = REPO_ROOT / "memory" / "strategy_evolution.md"


FORBIDDEN_KEYWORDS = [
    "short sell", "short selling", "short position", "short the", "sell short",
    "naked option", "naked call", "naked put",
    "credit spread", "iron condor", "strangle short",
    "futures", "perpetual", "perp ", "margin trading", "leverage ratio >",
    "cash minimum 0%", "cash floor 0", "cash = 0", "cash >= 0%",
    "disable auto-defense", "disable drawdown", "remove drawdown", "bypass guardrails",
    "override immutable", "modify hard cap", "raise hard cap", "raise the hard cap",
]


def _read_proposals() -> str:
    return PROPOSALS.read_text(encoding="utf-8") if PROPOSALS.exists() else ""


def _split_blocks(text: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for m in re.finditer(r"(?m)^##\s+(P-\d{8}-\d{3})\s+—\s+(.+?)$", text):
        pid = m.group(1)
        start = m.start()
        next_m = re.search(r"(?m)^##\s+P-\d{8}-\d{3}\s+—", text[start + 1:])
        end = start + 1 + next_m.start() if next_m else len(text)
        out.append((pid, text[start:end]))
    return out


def _get_field(block: str, name: str) -> str | None:
    m = re.search(rf"(?mi)^\*\*{re.escape(name)}\*\*:\s*(.+?)$", block)
    return m.group(1).strip() if m else None


def _get_diff(block: str) -> str | None:
    m = re.search(r"```diff\n(.*?)\n```", block, re.DOTALL)
    return m.group(1) if m else None


def cmd_list(args: argparse.Namespace) -> int:
    txt = _read_proposals()
    for pid, block in _split_blocks(txt):
        state = _get_field(block, "State") or "unknown"
        if args.state and state.lower().split(":")[0] != args.state.lower():
            continue
        title = re.search(rf"^##\s+{re.escape(pid)}\s+—\s+(.+?)$", block, re.MULTILINE)
        print(f"{pid}  [{state}]  {title.group(1) if title else ''}")
    return 0


def _check_gates(block: str) -> tuple[bool, str]:
    diff = _get_diff(block) or ""
    low = diff.lower()
    for kw in FORBIDDEN_KEYWORDS:
        if kw in low:
            return False, f"G4: forbidden keyword '{kw}'"
    evidence = _get_field(block, "Evidence")
    if not evidence or len(evidence) < 20:
        return False, "G7: evidence missing or too thin"
    revert = _get_field(block, "Revert trigger")
    if not revert or len(revert) < 10:
        return False, "G8: revert trigger missing"
    target = _get_field(block, "Target")
    if not target:
        return False, "G1: target file missing"
    tgt = Path(target)
    if tgt.parts and tgt.parts[0] in ("CLAUDE.md",):
        return False, "G1: target forbidden (CLAUDE.md)"
    if "guardrails.md" in str(tgt):
        return False, "G1: target forbidden (guardrails.md human-only)"
    if "skills/evolve" in str(tgt) or "skills/journal" in str(tgt):
        return False, "G1: target forbidden (self-protected skill)"
    return True, "ok"


def _find_block(text: str, pid: str) -> tuple[int, int, str] | None:
    for pidx, block in _split_blocks(text):
        if pidx == pid:
            m = re.search(rf"(?m)^##\s+{re.escape(pid)}\s+—", text)
            if not m:
                return None
            start = m.start()
            next_m = re.search(r"(?m)^##\s+P-\d{8}-\d{3}\s+—", text[start + 1:])
            end = start + 1 + next_m.start() if next_m else len(text)
            return (start, end, text[start:end])
    return None


def cmd_validate(args: argparse.Namespace) -> int:
    txt = _read_proposals()
    slot = _find_block(txt, args.id)
    if not slot:
        print(f"Proposal {args.id} not found")
        return 2
    ok, reason = _check_gates(slot[2])
    print(f"{args.id}: {'PASS' if ok else 'BLOCK'} — {reason}")
    return 0 if ok else 1


def _patch_apply(diff: str) -> tuple[bool, str]:
    proc = subprocess.run(["git", "apply", "--check", "-"], input=diff, text=True,
                          capture_output=True, cwd=str(REPO_ROOT))
    if proc.returncode != 0:
        return False, f"diff fails --check: {proc.stderr.strip()}"
    proc2 = subprocess.run(["git", "apply", "-"], input=diff, text=True,
                           capture_output=True, cwd=str(REPO_ROOT))
    if proc2.returncode != 0:
        return False, f"diff apply failed: {proc2.stderr.strip()}"
    return True, "applied"


def _update_state(pid: str, new_state: str) -> None:
    txt = _read_proposals()
    slot = _find_block(txt, pid)
    if not slot:
        return
    start, end, block = slot
    new_block = re.sub(r"(?mi)^\*\*State\*\*:.*$", f"**State**: {new_state}", block, count=1)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if f"**{'Applied at' if new_state == 'applied' else 'Blocked at'}**:" not in new_block:
        new_block += f"\n**{'Applied at' if new_state == 'applied' else 'Blocked at'}**: {ts}\n"
    PROPOSALS.write_text(txt[:start] + new_block + txt[end:], encoding="utf-8")


def _append_ledger(pid: str, block: str) -> None:
    if not LEDGER.exists():
        LEDGER.write_text("# Strategy evolution ledger\n\n", encoding="utf-8")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    target = _get_field(block, "Target") or "?"
    rationale = _get_field(block, "Rationale") or ""
    evidence = _get_field(block, "Evidence") or ""
    revert = _get_field(block, "Revert trigger") or ""
    entry = (
        f"\n## {ts} — {pid}\n"
        f"**Actor**: agent-autonomous via evolve skill\n"
        f"**Scope**: {target}\n"
        f"**Gates passed**: G1 G2 G3 G4 G5 G6 G7 G8\n\n"
        f"### Rationale\n{rationale}\n\n"
        f"### Evidence\n{evidence}\n\n"
        f"### Revert trigger\n{revert}\n"
    )
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(entry)


def cmd_apply(args: argparse.Namespace) -> int:
    txt = _read_proposals()
    slot = _find_block(txt, args.id)
    if not slot:
        print(f"Proposal {args.id} not found")
        return 2
    ok, reason = _check_gates(slot[2])
    if not ok:
        print(f"BLOCKED: {reason}")
        _update_state(args.id, f"blocked: {reason}")
        return 1
    diff = _get_diff(slot[2]) or ""
    ok2, msg = _patch_apply(diff)
    if not ok2:
        print(f"DIFF-FAIL: {msg}")
        _update_state(args.id, f"blocked: diff_validation — {msg}")
        return 1
    _append_ledger(args.id, slot[2])
    _update_state(args.id, "applied")
    print(f"APPLIED: {args.id}")
    return 0


def cmd_block(args: argparse.Namespace) -> int:
    _update_state(args.id, f"blocked: {args.reason}")
    print(f"BLOCKED: {args.id} — {args.reason}")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list")
    pl.add_argument("--state", choices=["proposed", "applied", "blocked"])
    pl.set_defaults(func=cmd_list)

    pv = sub.add_parser("validate")
    pv.add_argument("id")
    pv.set_defaults(func=cmd_validate)

    pa = sub.add_parser("apply")
    pa.add_argument("id")
    pa.set_defaults(func=cmd_apply)

    pb = sub.add_parser("block")
    pb.add_argument("id")
    pb.add_argument("--reason", required=True)
    pb.set_defaults(func=cmd_block)

    args = p.parse_args(argv[1:])
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
