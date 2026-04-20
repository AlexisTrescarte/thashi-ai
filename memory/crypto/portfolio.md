# Portfolio — Crypto

> Source of truth = Alpaca crypto API. This file is a **snapshot** written at every `crypto-daily-review`. Before any decision, refresh via `python scripts/alpaca_crypto_client.py positions`.

## Latest snapshot

- **Date (UTC)**: 2026-04-20T23:23:18Z
- **Equity total (USD)**: $97,382.43
- **Cash (USD)**: $97,382.43
- **Positions value**: $0.00
- **Cash %**: 100.00%
- **BTC benchmark price**: $75,822.83 (mid of $75,846.47 ask / $75,799.19 bid @ 23:23Z)
- **Performance vs BTC since baseline**: n/a (D0 — baseline set today)
- **Regime (crypto)**: undefined (first hourly run pending)
- **Auto-defense active**: no

## Baseline

- **Starting capital**: $97,382.43 (crypto-agent NAV — shared paper account with equities agent; sleeve split pending human declaration)
- **Baseline date (UTC)**: 2026-04-20
- **BTC baseline**: $75,822.83

## ATH tracking

- **ATH equity**: $97,382.43
- **ATH date**: 2026-04-20
- **Current drawdown from ATH**: 0.00%

## Open positions

_Regenerated from API at every `crypto-daily-review`. Format:_

| Symbol | Qty | Avg cost | Price | Value | P&L $ | P&L % | Entry (UTC) | Age (h) | CTQS | Style | Stop | TP | Catalyst |
|--------|-----|----------|-------|-------|-------|-------|-------------|---------|------|-------|------|----|----------|
| _none_ | — | — | — | — | — | — | — | — | — | — | — | — | — |

## Open risks

- **Sleeve-split ambiguity**: crypto agent and equities agent share one paper account ($97,382.43 total). Without a declared crypto NAV sleeve, per-position 10% / sector 25% caps cannot be computed against a stable denominator. Flag for human.
- **No regime read yet**: first `crypto-hourly` run must establish regime (BTC dominance, ETH/BTC, funding, DXY, key levels) before any BUY is considered.
- **Hourly cadence blackout**: 0 hourly runs in the last 24h → no CTQS scan, no regime log, no research entries. Cadence must start next cycle.
