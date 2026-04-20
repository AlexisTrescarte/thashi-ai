# Routine — monthly-deep-review (equities)

## Cron

```
0 17 28-31 * 5
```
(17:00 America/Chicago, last Friday of the month — approximated by last-week Friday. If cron engine supports `L`: use `0 17 L * 5` instead. Otherwise add a date check in the prompt: "only run if today is the last Friday of the month; else exit cleanly and log a runs.log noop.")

## Environment

- Cloud environment: `trading`
- Repo: `<your-user>/thashi-ai` (branch `main`)
- Model: Claude Opus 4.7

## Prompt to paste in the routine

```
You are Bull-Equities in monthly-deep-review (17:00 CT, last Friday of month). Invoke the /monthly-deep-review slash command and follow it to the letter.

Pre-flight:
- Verify today is the last Friday of the current month. If not: append a "noop — not last Friday" line to memory/runs.log and exit cleanly. Do NOT run the review.

Context:
- Invoke the `review` skill with agent=equities, rhythm=monthly, window=1st-to-today ISO dates.
- Compute Sharpe, Sortino, Max DD, Calmar. Grade A/B/C/D/F.
- Generate prompt-evolution proposals per the review skill's rules (sample size ≥ 20 per setup, evidence + revert trigger mandatory).
- Invoke the `evolve` skill with agent=equities, rhythm=monthly. Gates G1-G8 run; blocked proposals stay in queue.
- Monthly may touch .claude/commands/*.md and non-self-protected skills — NOT strategy.md (quarterly only), NOT guardrails.md (human only), NOT CLAUDE.md.
- Namespace: equities only.
- Journal skill handles commit + push.
- Telegram notification is MANDATORY with the monthly format.
```
