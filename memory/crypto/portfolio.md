# Portfolio — Crypto

> Source of truth = Alpaca crypto API. This file is a **snapshot** written at every `crypto-daily-review`. Before any decision, refresh via `python scripts/alpaca_crypto_client.py positions`.

## Latest snapshot

- **Date (UTC)**: 2026-04-22T23:00:00Z
- **Equity total (USD)**: $97,382.43
- **Cash (USD)**: $97,382.43
- **Positions value**: $0.00
- **Cash %**: 100.00%
- **BTC benchmark price**: $78,593.70 (mid bid/ask at 23:13 UTC)
- **Performance vs BTC since baseline**: 0.00% (baseline day)
- **Regime (crypto)**: unknown — 0 scan runs in window
- **Auto-defense active**: no

## Baseline

- **Starting capital**: $97,382.43 (crypto allocation = full paper account)
- **Baseline date (UTC)**: 2026-04-22T23:00:00Z
- **BTC baseline**: $78,593.70

## ATH tracking

- **ATH equity**: $97,382.43
- **ATH date**: 2026-04-22
- **Current drawdown from ATH**: 0.00%

## Open positions

_Regenerated from API at every `crypto-daily-review`. Format:_

| Symbol | Qty | Avg cost | Price | Value | P&L $ | P&L % | Entry (UTC) | Age (h) | CTQS | Style | Stop | TP | Catalyst |
|--------|-----|----------|-------|-------|-------|-------|-------------|---------|------|-------|------|----|----------|

_(no open positions)_

## Open risks

- **Scheduler gap**: 0/6 crypto-hourly runs executed in the last 24h. Remote trigger `crypto-hourly` appears not yet deployed or not firing on the `0 */4 * * *` UTC cron. Until this is resolved, no research, no BUYs, no dynamic stop management will occur. Flagged as INCIDENT in `memory/learnings.md`.
- Account shares paper equity with Bull-Equities ($97,382.43 total). Allocation policy between agents not yet defined — to revisit once both agents are live.
