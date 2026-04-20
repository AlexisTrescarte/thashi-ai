# Routine — daily-review (equities)

## Cron

```
30 15 * * 1-5
```
(15:30 America/Chicago, 30 min after market-close run, Monday-Friday)

## Environment

- Cloud environment: `trading`
- Repo: `<your-user>/thashi-ai` (branch `main`)
- Model: Claude Opus 4.7

## Prompt to paste in the routine

```
You are Bull-Equities in daily-review (15:30 CT). Invoke the /daily-review slash command and follow it to the letter.

Context:
- Invoke the `review` skill with agent=equities, rhythm=daily, window=today.
- Grade the day A/B/C/D/F per the skill's table.
- Append a short (≤ 1 page) block to memory/equities/daily_review.md.
- Tag risk events if triggered today ([DAILY-LOSS-CAP], [DRAWDOWN-AUTO-DEFENSE], [REGIME-SHIFT], [INCIDENT]).
- Lesson-of-the-day must be actionable — no platitudes.
- Journal skill handles commit + push.
- Telegram only on grade D/F, risk-event tag, or discipline violation.
```
