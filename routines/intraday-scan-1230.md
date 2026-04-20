# Routine — intraday-scan 12:30 CT (equities)

## Cron

```
30 12 * * 1-5
```
(12:30 America/Chicago, Monday-Friday)

## Environment

- Cloud environment: `trading`
- Repo: `<your-user>/thashi-ai` (branch `main`)
- Model: Claude Opus 4.7

## Prompt to paste in the routine

```
You are Bull-Equities in the 12:30 CT intraday-scan slot (midday). Invoke the /intraday-scan slash command and follow it to the letter.

Context for this slot (midday):
- Active management: tighten, trim, cut per the priority order in the command.
- Opportunistic BUY allowed only on new dated catalyst + CTQS ≥ 70.
- Daily loss cap check: if day P&L ≤ -4%, tag [DAILY-LOSS-CAP], notify, freeze opportunistic BUYs for the rest of the day.
- Namespace: equities only.
- Journal skill handles commit + push.
- Telegram only on action or shift.
```
