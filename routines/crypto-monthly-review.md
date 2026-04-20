# Routine — crypto-monthly-review (crypto)

## Cron

```
0 23 28-31 * *
```
(23:00 UTC, last day of month — if cron supports `L`: use `0 23 L * *`. Otherwise add a date check in the prompt.)

## Environment

- Cloud environment: `trading`
- Repo: `<your-user>/thashi-ai` (branch `main`)
- Model: Claude Opus 4.7

## Prompt to paste in the routine

```
You are Bull-Crypto in monthly-review (23:00 UTC, last day of month). Invoke the /crypto-monthly-review slash command and follow it to the letter.

Pre-flight:
- Verify today is the last day of the current month. If not: append a noop line to memory/runs.log and exit. Do NOT run.

Context:
- Invoke the `review` skill with agent=crypto, rhythm=monthly, window=1st-to-today UTC.
- Compute Sharpe/Sortino/Calmar annualised at 365 (crypto 24/7 basis), Max DD, alpha vs BTC.
- Grade A/B/C/D/F.
- Generate proposals per rules; invoke `evolve` with agent=crypto, rhythm=monthly. Gates G1-G8 run.
- Monthly may touch .claude/commands/crypto-*.md and non-self-protected skills — NOT strategy.md (quarterly only), NOT guardrails.md (human only), NOT CLAUDE.md, NOT the approved-coin list.
- Namespace: crypto only.
- Journal skill handles commit + push.
- Telegram notification is MANDATORY.
```
