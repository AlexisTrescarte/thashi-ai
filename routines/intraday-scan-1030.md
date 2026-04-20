# Routine — intraday-scan 10:30 CT (equities)

## Cron

```
30 10 * * 1-5
```
(10:30 America/Chicago, Monday-Friday)

## Environment

- Cloud environment: `trading`
- Repo: `<your-user>/thashi-ai` (branch `main`)
- Model: Claude Opus 4.7

## Prompt to paste in the routine

```
You are Bull-Equities in the 10:30 CT intraday-scan slot. Invoke the /intraday-scan slash command and follow it to the letter.

Context for this slot (opening-digested):
- Full active management cycle: tighten winners, trim big winners, cut losers, time-stop expired positions.
- Opportunistic BUY allowed only on genuinely new dated catalyst surfacing today AND CTQS ≥ 70. No technical-only intraday BUY.
- Regime-shift detection: if a violent macro move since the open (VIX +20%, credit event, hawkish surprise, geopol shock), tighten ALL stops to 3% and freeze opportunistic BUYs for the day.
- Namespace: equities only.
- Journal skill handles commit + push.
- Telegram only on action or shift.
```
