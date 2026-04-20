# Routine — quarterly-rewrite (equities, strategy rewrite)

## Cron

```
0 18 28-31 3,6,9,12 5
```
(18:00 America/Chicago, last Friday of Mar/Jun/Sep/Dec — approximated by last-week Friday of those months. If cron supports `L`: use `0 18 L 3,6,9,12 5`. Otherwise add a date check in the prompt.)

## Environment

- Cloud environment: `trading`
- Repo: `<your-user>/thashi-ai` (branch `main`)
- Model: Claude Opus 4.7

## Prompt to paste in the routine

```
You are Bull-Equities in quarterly-rewrite (18:00 CT, last Friday of Mar/Jun/Sep/Dec). Invoke the /quarterly-rewrite slash command and follow it to the letter.

Pre-flight:
- Verify today is the last Friday of Mar/Jun/Sep/Dec. If not: append a noop line to memory/runs.log and exit. Do NOT run.

Context:
- THIS IS THE ONLY ROUTINE AUTHORISED TO MODIFY memory/strategy.md (via the evolve skill's quarterly scope).
- Invoke the `review` skill with agent=equities, rhythm=quarterly, window=quarter-start-to-today.
- Audit strategy fitness on: macro-regime fit, setup fitness, instrument fitness, style fitness, stop-methodology fitness, activity + sizing, discipline ledger, correlation to benchmark.
- Draft ≤ 10 prompt-evolution proposals targeting memory/strategy.md. Each must include: diff, before/after metrics, sample window, revert trigger.
- Invoke the `evolve` skill with agent=equities, rhythm=quarterly. Gates G1-G8 run.
- After apply: bump strategy version (minor for tweaks, major for structural). Append version history entry.
- Optional baseline reset decision per the command's rules (never reset to hide drawdown).
- Namespace: equities only. This routine NEVER modifies guardrails.md or CLAUDE.md.
- Journal skill handles commit + push.
- Telegram notification is MANDATORY with the quarterly format.
```
