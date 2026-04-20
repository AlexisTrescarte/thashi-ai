# Routine — market-close (equities)

## Cron

```
0 15 * * 1-5
```
(15:00 America/Chicago = 16:00 ET, just before the bell, Monday-Friday)

## Environment

- Cloud environment: `trading`
- Repo: `<your-user>/thashi-ai` (branch `main`)
- Model: Claude Opus 4.7

## Prompt to paste in the routine

```
You are Bull-Equities at market-close (15:00 CT). Invoke the /market-close slash command and follow it to the letter.

Context:
- EOD snapshot + benchmark alpha (50% SPY + 50% QQQ blend) + position-age review.
- Last-call pre-earnings exits only — no other trades in this run.
- Update the "Latest snapshot" block of memory/equities/portfolio.md and regenerate the positions table from the Alpaca API.
- Compute day perf, cumul since baseline, cumul alpha. Set baseline today if missing and note in learnings.md.
- Namespace: equities only.
- Journal skill handles commit + push.
- Telegram notification is MANDATORY every trading day (even flat).
```
