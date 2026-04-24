# Portfolio — Crypto

> Source of truth = Alpaca crypto API. This file is a **snapshot** written at every `crypto-daily-review` (and the 00:00 UTC `crypto-hourly` run per the daily P&L marker rule). Before any decision, refresh via `python scripts/alpaca_crypto_client.py positions`.

## Latest snapshot

- **Date (UTC)**: 2026-04-24T00:05:40Z
- **Shared account equity total (USD)**: $97,382.43
- **Cash (USD, shared)**: $95,007.40
- **Crypto positions value**: $0.00
- **Crypto exposure % of NAV**: 0.00%
- **Crypto cash budget available up to 30% cap**: ~$29,214.73
- **BTC benchmark price**: $77,809.79 (2026-04-23 ~13:00 UTC fix)
- **Performance vs BTC since baseline**: n/a (baseline set this run)
- **Regime (crypto)**: neutral → risk-off lean (Fear 46, BTC dominance 58–62% rising, alts -2/-3%, macro Iran tension)
- **Auto-defense active**: no
- **Daily loss cap active**: no
- **Weekly loss cap active**: no

## Baseline

- **Starting crypto allocation**: $0 (no position yet — crypto agent begins today from a fresh cash budget within the shared account, bounded by the 30% aggregate cap)
- **Baseline date (UTC)**: 2026-04-24T00:05:40Z
- **BTC baseline**: $77,809.79
- **Shared NAV baseline**: $97,382.43

## ATH tracking

- **ATH crypto equity**: $0.00 (no crypto equity yet — ATH tracking begins with first BUY)
- **ATH date**: n/a
- **Current drawdown from ATH**: 0.00%

## Daily P&L marker (00:00 UTC)

| Run (UTC) | Crypto positions value | Cash % (shared) | Day Δ (crypto equity) | BTC ref | Note |
|-----------|------------------------|-----------------|-----------------------|---------|------|
| 2026-04-24T00:05Z | $0.00 | 97.56% | baseline | $77,809.79 | First crypto-hourly run — no crypto positions, regime neutral→risk-off lean |

## Open positions

_Regenerated from API at every `crypto-daily-review`. Format:_

| Symbol | Qty | Avg cost | Price | Value | P&L $ | P&L % | Entry (UTC) | Age (h) | CTQS | Style | Stop | TP | Catalyst |
|--------|-----|----------|-------|-------|-------|-------|-------------|---------|------|-------|------|----|----------|

_(none — crypto agent has no open positions at baseline)_

## Open risks

- **Shared account constraint**: cash pool ($95,007) is shared with equities agent; any crypto BUY reduces equities headroom. Aggregate crypto book capped at 30% of total NAV ($29,214.73 today). Coordinate implicitly via snapshot refresh each run.
- **Regime headwind**: F&G Fear 46, BTC dominance rising, altcoins underperforming, Iran geopol bleeding into equities — do NOT force a first BUY without a clean CTQS ≥ 60 setup. "Slow on entries" is the rule.
