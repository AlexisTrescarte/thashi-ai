# Portfolio — Crypto

> Source of truth = Alpaca crypto API. This file is a **snapshot** written at every `crypto-daily-review`. Before any decision, refresh via `python scripts/alpaca_crypto_client.py positions`.

## Latest snapshot

- **Date (UTC)**: 2026-04-23T23:00:00Z
- **Equity total (USD)**: $97,377.74 _(shared account; crypto-attributable = $0, all positions are equities)_
- **Cash (USD)**: $95,007.40
- **Positions value (crypto)**: $0.00
- **Cash %**: 97.56% (shared)
- **BTC benchmark price**: $78,176 mid (bid $78,141.94 / ask $78,210.04 at 23:29 UTC)
- **Performance vs BTC since baseline**: N/A _(no baseline — 0 crypto exposure since deployment)_
- **Regime (crypto)**: unknown _(0 scan runs in last 24h)_
- **Auto-defense active**: no

## Baseline

- **Starting capital**: $— (crypto allocation — not yet deployed)
- **Baseline date (UTC)**: _(to be set on first crypto live trade)_
- **BTC baseline**: _(to be set on first crypto live trade)_

## ATH tracking

- **ATH equity**: $— _(crypto book never held positions)_
- **ATH date**: —
- **Current drawdown from ATH**: —%

## Open positions

_Regenerated from API at every `crypto-daily-review`. Format:_

| Symbol | Qty | Avg cost | Price | Value | P&L $ | P&L % | Entry (UTC) | Age (h) | CTQS | Style | Stop | TP | Catalyst |
|--------|-----|----------|-------|-------|-------|-------|-------------|---------|------|-------|------|----|----------|

_(none — 0 crypto positions at 2026-04-23T23:00:00Z)_

## Open risks

- **Operational gap**: `crypto-hourly` routine has never logged a run in `memory/runs.log` since deployment. 6 expected scans today (00/04/08/12/16/20 UTC) vs 0 observed. Regime tally impossible. Verify RemoteTrigger is enabled, inspect `next_run_at`, and confirm the trigger targets the active branch. Until resolved, the crypto book will stay blind to opportunities and regime shifts.
