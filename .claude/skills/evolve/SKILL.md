---
name: evolve
description: Gate-check and apply prompt-evolution proposals from memory/prompt_evolution_proposals.md. Enforces immutable guardrails (no hard-cap changes, no forbidden features, no disabling of auto-defense or evolution gates). Logs every applied change to memory/strategy_evolution.md. Invoke from monthly-deep-review and quarterly-rewrite only.
---

# Skill: evolve

Execute the controlled self-modification loop. Reads pending proposals, gate-checks each, applies the diff, logs to the evolution ledger, commits.

> This is the most sensitive skill. An unchecked evolve = runaway agent. Every gate must pass or the proposal is blocked. A blocked proposal stays in the queue for human review — never silently discarded.

## Invocation

Inputs:
- `agent`: `equities` or `crypto` (proposals can target agent-specific prompts or shared files)
- `rhythm`: `monthly` or `quarterly` (quarterly is the only rhythm allowed to touch `memory/strategy.md`)

## Pipeline

1. **Read** `memory/prompt_evolution_proposals.md` → all entries with state `proposed`
2. **For each proposal**:
   a. Run **all immutable gates** (below) — if any fails, mark `blocked: {reason}`, write decision, continue
   b. If all gates pass, run `diff validation` (below)
   c. If diff validates, **apply the patch**
   d. Run the post-apply check (target file still parses, guardrails still in place)
   e. Append entry to `memory/strategy_evolution.md`
   f. Update proposal state in `prompt_evolution_proposals.md` to `applied` with timestamp
3. **Commit** with message `[prompt-evolution] YYYY-MM-DD — {n} applied, {m} blocked`
4. **Notify Telegram** with summary

## Immutable gates (any failure = block)

### G1 — Target scope allowed
- **Monthly**: may target files in `.claude/commands/*.md` or `.claude/skills/*/SKILL.md`, except this `evolve` skill itself
- **Quarterly**: may additionally target `memory/strategy.md` (but never the immutable sections of `guardrails.md`)
- **Neither** may touch: `CLAUDE.md`, `memory/guardrails.md` (any section), `.claude/skills/evolve/SKILL.md` (self-protection), `.claude/skills/journal/SKILL.md` immutable parts, `scripts/*.py`

### G2 — Immutable content preserved
Parse the target file after the proposed diff. Verify these strings/sections remain intact (exact match required):
- In `guardrails.md`: the "Immutable hard caps", "Drawdown auto-defense", "Forbidden instruments", "Self-evolution gates" sections
- In any affected command: the Telegram notification policy section (can be tuned in content but the rule that notifications exist for mandatory routines cannot be removed)
- In `strategy.md`: the "What the agent is NEVER allowed to change" section

### G3 — Sample size
- Per-setup tweaks: sample ≥ 20 trades in window
- Framework-wide tweaks: sample ≥ 50 trades in window

### G4 — No forbidden-feature enablement
Diff must not introduce (case-insensitive match on known keywords):
- `short sell`, `short selling`, `short position`, `short the`, `sell short`
- `naked`, `credit spread`, `iron condor`, `strangle short`
- `futures`, `perpetual`, `margin trading`, `leverage ratio > 1` (for crypto)
- `cash minimum 0%`, `cash floor 0`, `cash = 0`, `cash >= 0%`
- `disable auto-defense`, `disable drawdown`, `remove drawdown`, `bypass guardrails`
- `override immutable`, `modify hard cap`, `raise hard cap`
- Crypto symbols outside the approved list (BTC/ETH/SOL/LINK/AVAX/DOT/MATIC) being added as tradeable

### G5 — Evolution gates not disabled
Diff must not remove or weaken any gate in this skill. A proposal targeting `evolve/SKILL.md` is automatically blocked (G1 would catch it; this is a second check).

### G6 — No active risk event
- No `[DRAWDOWN-AUTO-DEFENSE]` active in last 14 days
- No `[DAILY-LOSS-CAP]` today, no `[WEEKLY-LOSS-CAP]` in last 3 trading days
- No `[API-DEGRADED]` in last run

If any is active, defer all proposals to next review cycle — mark `blocked: active_risk_event`, keep in queue.

### G7 — Evidence requirement
Proposal must include:
- Concrete metric numbers (before/after)
- Sample window dates
- Statistical comparison (e.g. hit rate X% vs cohort Y%, delta Zpp)

Missing evidence → `blocked: insufficient_evidence`.

### G8 — Revert trigger defined
Proposal must define a revert trigger (e.g. "revert if next-month hit rate on this setup drops below baseline"). Without one → `blocked: no_revert_trigger`.

## Diff validation

- Unified-diff format, parseable
- Target file paths relative to repo root
- No hunk crosses two different files
- Diff applies cleanly (no rebase conflict) against current file
- Post-apply file size within ±50% of original (guard against mass deletion)

## Applying a patch

1. Read target file
2. Apply diff
3. Validate post-state: file parses, guardrails intact (regex check on immutable markers), no secrets introduced
4. Write file
5. Append to `memory/strategy_evolution.md`:

```markdown
## {ISO-UTC} — {routine} — {proposal title}

**Actor**: agent-autonomous via {monthly-deep-review | quarterly-rewrite}
**Scope**: {target file}
**Gates passed**: G1 ✓ G2 ✓ G3 ✓ G4 ✓ G5 ✓ G6 ✓ G7 ✓ G8 ✓

### Rationale
{from proposal}

### Evidence
{from proposal}

### Before → After (diff summary)
{3-line summary of the change}

### Revert trigger
{from proposal — metric + threshold}

### Follow-up
- Watch {metric} in next review
- If revert trigger fires, queue counter-proposal
```

6. Update proposal in `prompt_evolution_proposals.md` to `applied` with timestamp

## Blocking a proposal

Update proposal state to `blocked: {gate-id + reason}`. Do NOT delete it. It stays in queue for human review. Example:

```
**State**: blocked: G4 — proposed diff introduced "raise hard cap to 15%"
**Blocked at**: 2026-05-25T22:15:00Z
```

## Post-run

- Commit + push (journal skill handles)
- Telegram (French): `*🧬 Évolution prompts* — {rhythm}\n• {n} appliquées · {m} bloquées · {k} en attente`
- If any block triggered G2/G4/G5 (hard-cap, forbidden-feature, evolution-gate attack): add an `[INCIDENT]` entry to `learnings.md` so it's visible in future reviews

## Refusal conditions

- Multiple proposals targeting same file in same cycle → apply at most 1 (pick highest-evidence), defer others
- Two proposals with contradictory diffs → block both, request human arbitration
- Proposal older than 2 review cycles without being applied or blocked → auto-block with `stale: please review`
