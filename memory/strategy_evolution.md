# Strategy evolution log

Append-only. **Never rewrite** a past entry. Every change to `memory/strategy.md` or to any command/skill prompt — whether agent-autonomous (via gated self-evolution) or human-edited — is logged here with rationale and evidence.

## Schema

```markdown
## YYYY-MM-DDTHH:MM:SSZ — {routine or "human"} — {title}

**Actor**: {agent-autonomous via monthly-deep-review | agent-autonomous via quarterly-rewrite | human}
**Scope**: {strategy.md | guardrails.md | .claude/commands/X.md | .claude/skills/X/SKILL.md}
**Gates passed** (if autonomous): {list of gate checks}

### Rationale
{2-4 lines — why this change}

### Evidence
{data points, metrics, sample size — concrete numbers}

### Before → After (diff summary)
{1-3 lines describing the delta}

### Follow-up
{metric to watch, revert criteria if it doesn't work}
```

## Log

_(empty — first evolution will append here)_
