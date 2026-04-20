# Prompt evolution proposals

Append-only queue. The `monthly-deep-review` and `quarterly-rewrite` routines write proposals here. The `evolve` skill reads, gate-checks, and applies (or blocks) them.

## States

- `proposed` — freshly written, awaiting gate check
- `applied` — gates passed, change executed, logged to `strategy_evolution.md`
- `blocked: {reason}` — gate failed, awaits human review

## Schema

```markdown
## {proposal-id: YYYY-MM-DDTHH:MM:SSZ-N} — {title}

**State**: proposed
**Scope**: {target file path}
**Proposed by**: {routine}
**Sample size**: N trades in window {YYYY-MM-DD → YYYY-MM-DD}

### Problem observed
{2-3 lines — metric drift, setup bleeding, etc., with numbers}

### Proposed change
```diff
- old line
+ new line
```

### Rationale
{2-3 lines}

### Gates
- [ ] min sample size met (N ≥ 20 per-setup / N ≥ 50 framework)
- [ ] no modification of immutable guardrails section
- [ ] no forbidden feature enabled
- [ ] no disabling of auto-defense
- [ ] no disabling of evolution gates
- [ ] no active drawdown auto-defense
- [ ] no active daily/weekly loss cap

### Decision
{applied | blocked: reason}
{timestamp of decision}
```

## Proposals

_(empty — first monthly review will write here)_
