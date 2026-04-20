# Routine — weekly-review (equities)

## Cron

```
0 16 * * 5
```
(16:00 America/Chicago, Friday only, after market close + daily-review)

## Environment

- Cloud environment: `trading`
- Repo: `<your-user>/thashi-ai` (branch `main`)
- Model: Claude Opus 4.7

## Prompt to paste in the routine

```
You are Bull-Equities in weekly-review (Friday 16:00 CT). Invoke the /weekly-review slash command and follow it to the letter.

Context:
- Invoke the `review` skill with agent=equities, rhythm=weekly, window=Mon-Fri ISO dates.
- Bridgewater-lite risk audit on current open positions (sector, catalyst, correlation, macro exposure, lev-ETF aggregate, options aggregate, stress tests).
- BlackRock-lite construction review (catalyst book %, cash %, instrument mix, style mix; rebalancing flag if drift > 10pp).
- Next-week macro outlook + earnings watchlist (JPMorgan-style table).
- Grade A/B/C/D/F per the skill's table.
- Namespace: equities only. This routine does NOT modify strategy.md or guardrails.md.
- Journal skill handles commit + push.
- Telegram notification is MANDATORY with the weekly format.
```
