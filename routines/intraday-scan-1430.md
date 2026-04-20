# Routine — intraday-scan 14:30 CT (equities, last-call)

## Cron

```
30 14 * * 1-5
```
(14:30 America/Chicago, Monday-Friday)

## Environment

- Cloud environment: `trading`
- Repo: `<your-user>/thashi-ai` (branch `main`)
- Model: Claude Opus 4.7

## Prompt to paste in the routine

```
You are Bull-Equities in the 14:30 CT intraday-scan slot (last-call before close). Invoke the /intraday-scan slash command and follow it to the letter.

Context for this slot (last-call):
- Active management: final tighten, trim, cut pass before the bell.
- **NO OPPORTUNISTIC BUY in this slot** — last-call is for exits only (enforced by the command).
- Pre-earnings cuts: any position with earnings reporting tomorrow BMO or tonight AMC without "earnings hold" → CUT immediately.
- Options DTE-3: any option at DTE-3 or less → CUT regardless of P&L.
- Day-trade horizon: any position tagged day-trade must be closed by this slot.
- Namespace: equities only.
- Journal skill handles commit + push.
- Telegram on action only.
```
