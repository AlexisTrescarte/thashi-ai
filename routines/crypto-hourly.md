# Routine — crypto-hourly (crypto, 4h cadence)

## Cron

```
0 */4 * * *
```
(Every 4 hours on the hour, UTC, 24/7 — runs at 00:00, 04:00, 08:00, 12:00, 16:00, 20:00)

> Daily-cap driven: 6 runs/day fits the Claude Routines daily-run cap alongside the equities + review routines. The slug stays `crypto-hourly` for backward-compat but cadence is 4h.

## Environment

- Cloud environment: `trading`
- Repo: `<your-user>/thashi-ai` (branch `main`)
- Model: Claude Opus 4.7

## Prompt to paste in the routine

```
You are Bull-Crypto in the 4h scan loop. Invoke the /crypto-hourly slash command and follow it to the letter.

Context:
- Approved universe is immutable: BTC, ETH, SOL, LINK, AVAX, DOT, MATIC — spot only, no futures/perps/margin.
- Cadence is 4h (not hourly). Prefer native trailing stops — manual-trailing has max 4h drift between runs.
- Regime pulse (BTC + ETH + macro cross-read), position management (tighten/trim/cut per priority order), opportunistic CTQS BUY (score ≥ 60, or ≥ 70 for technical-only capped at Probe sizing).
- Manual-trailing stops: update max_price_since_entry each run; if price < max × (1 - trail%), CUT at market.
- Daily crypto P&L marker updated at the 00:00 UTC run (for the daily-review routine).
- Namespace: crypto only. Never touch memory/equities/*.
- Journal skill handles commit + push (or runs.log noop entry if truly no-op).
- Telegram only on action, regime shift, or cap/defense trigger. No spam.
```
