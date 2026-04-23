# Portfolio — Crypto

> Source of truth = Alpaca crypto API. This file is a **snapshot** written at every `crypto-daily-review` (and at the 00:00 UTC `crypto-hourly` for the daily P&L marker). Before any decision, refresh via `python scripts/alpaca_crypto_client.py positions`.

## Latest snapshot

- **Date (UTC)**: 2026-04-23T00:40:30Z
- **Equity total (USD, account-wide, shared with equities agent)**: $97,382.43
- **Cash (USD)**: $97,382.43
- **Crypto positions value**: $0.00
- **Crypto book exposure**: 0.00% of total NAV (cap 30%)
- **Cash %**: 100.00%
- **BTC benchmark price**: $78,924
- **Performance vs BTC since baseline**: 0.00% (baseline run)
- **Regime (crypto)**: neutral, leaning risk-on (DXY 4-yr low, BTC bouncing, ETH/BTC at 3-mo high, equities firmer on ceasefire)
- **Auto-defense active**: no
- **Daily loss cap active**: no
- **Weekly loss cap active**: no

## Baseline

- **Starting capital (account-wide)**: $97,382.43
- **Crypto-allocated NAV ceiling**: 30% of total = ~$29,214 (per guardrails aggregate-crypto cap)
- **Baseline date (UTC)**: 2026-04-23
- **BTC baseline**: $78,924

## ATH tracking

- **ATH equity (account-wide)**: $97,382.43
- **ATH date**: 2026-04-23 (baseline)
- **Current drawdown from ATH**: 0.00%

## Open positions

_Regenerated from API at every `crypto-daily-review`. Format:_

| Symbol | Qty | Avg cost | Price | Value | P&L $ | P&L % | Entry (UTC) | Age (h) | CTQS | Style | Stop | TP | Catalyst |
|--------|-----|----------|-------|-------|-------|-------|-------------|---------|------|-------|------|----|----------|
| _(none)_ | | | | | | | | | | | | | |

## Open risks

- _None — book empty. Universe and stops to be deployed only on CTQS ≥ 60 (or ≥ 70 technical-only Probe)._
