# Portfolio — Crypto

> Source of truth = Alpaca crypto API. This file is a **snapshot** written at every `crypto-daily-review`. Before any decision, refresh via `python scripts/alpaca_crypto_client.py positions`.

## Latest snapshot

- **Date (UTC)**: 2026-04-21T02:04:49Z
- **Source**: crypto-hourly (first Bull v2 run — baseline snapshot)
- **Total account equity (USD)**: $97,382.43 (shared Alpaca account across equities + crypto agents)
- **Total account cash (USD)**: $97,382.43
- **Crypto positions value**: $0.00
- **Crypto book % of NAV**: 0.0%
- **Cash %**: 100.0%
- **BTC benchmark price**: ~$75,628 (WebSearch cross-read, ~mid-April 2026)
- **Performance vs BTC since baseline**: baseline run — n/a
- **Regime (crypto)**: neutral
- **Auto-defense active**: no
- **Daily loss cap active**: no
- **Weekly loss cap active**: no

## Baseline

- **Starting capital (crypto allocation)**: $97,382.43 (account equity at first Bull v2 crypto-hourly run; pre-existing equities-side residual of $3.77 BTCUSD referenced in learnings is no longer in the Alpaca positions list as of this run)
- **Baseline date (UTC)**: 2026-04-21T02:04:49Z
- **BTC baseline**: ~$75,628

## ATH tracking

- **ATH equity**: $97,382.43
- **ATH date**: 2026-04-21
- **Current drawdown from ATH**: 0.0%

## Open positions

_Regenerated from API at every `crypto-daily-review`. Format:_

| Symbol | Qty | Avg cost | Price | Value | P&L $ | P&L % | Entry (UTC) | Age (h) | CTQS | Style | Stop | TP | Catalyst |
|--------|-----|----------|-------|-------|-------|-------|-------------|---------|------|-------|------|----|----------|

_(no open crypto positions at baseline)_

## Open risks

- **MATIC universe mismatch**: immutable universe still lists MATIC, but Polygon migrated to POL in late 2024 and legacy MATIC liquidity on aggregators is effectively nil. Treated SKIP at every run. Flagged for quarterly-rewrite human review — agent cannot modify the immutable universe line-item.
- **Regime fragility**: Fear & Greed retail at 23 (Extreme Fear) — if BTC loses consolidation floor, risk of a fear-driven flush. No position exposure yet so no defensive action required.
