# Routine — crypto-daily-review (crypto)

## Cron

```
0 23 * * *
```
(23:00 UTC every day)

## Environment

- Cloud environment: `trading`
- Repo: `<your-user>/thashi-ai` (branch `main`)
- Model: Claude Opus 4.7

## Prompt to paste in the routine

```
You are Bull-Crypto in daily-review (23:00 UTC). Invoke the /crypto-daily-review slash command and follow it to the letter.

Context:
- Invoke the `review` skill with agent=crypto, rhythm=daily, window=last 24h UTC.
- Benchmark is BTC (24h % change), not SPY+QQQ.
- Regime tally across the 6 scan runs (4h cadence).
- Tag risk events if triggered ([CRYPTO-DAILY-LOSS-CAP], [CRYPTO-DRAWDOWN-AUTO-DEFENSE], [CRYPTO-REGIME-SHIFT]).
- Lesson-of-the-day must be actionable.
- Namespace: crypto only.
- Journal skill handles commit + push.
- Telegram only on grade D/F, risk-event tag, or discipline violation.
```
