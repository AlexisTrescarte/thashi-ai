# Portfolio — Crypto

> Source of truth = Alpaca crypto API. This file is a **snapshot** written at every `crypto-daily-review`. Before any decision, refresh via `python scripts/alpaca_crypto_client.py positions`.

## Latest snapshot

- **Date (UTC)**: 2026-04-20T20:06Z
- **Equity total (USD)**: $97,382.46
- **Cash (USD)**: $97,378.65
- **Positions value**: $3.81
- **Cash %**: 99.996%
- **BTC benchmark price**: $76,230 (mid, BTC/USD)
- **Performance vs BTC since baseline**: baseline-setting run
- **Regime (crypto)**: neutral / mildly risk-on (BTC holding $75K, ETF inflows positive, total cap -1.3% → alt weakness)
- **Auto-defense active**: no

## Baseline

- **Starting capital**: $97,382.46 (shared Alpaca account, crypto allocation floats freely up to 30% NAV cap)
- **Baseline date (UTC)**: 2026-04-20T20:06Z (first Bull-Crypto v2 run)
- **BTC baseline**: $76,230

## ATH tracking

- **ATH equity**: $97,382.46
- **ATH date**: 2026-04-20T20:06Z
- **Current drawdown from ATH**: 0.00%

## Open positions

_Regenerated from API at every `crypto-daily-review`. Format:_

| Symbol | Qty | Avg cost | Price | Value | P&L $ | P&L % | Entry (UTC) | Age (h) | CTQS | Style | Stop | TP | Catalyst |
|--------|-----|----------|-------|-------|-------|-------|-------------|---------|------|-------|------|----|----------|
| BTCUSD (legacy-orphan-dust) | 0.000049999 | $73,094.17 | $76,229.80 | $3.81 | +$0.16 | +4.29% | pre-v2 (unknown) | >168 | none | none | none (qty below exchange min, untradeable) | n/a | n/a |

## Open risks

- **BTCUSD legacy-orphan-dust**: inherited from pre-Bull-v2 equities routines. Qty 0.000049999 BTC is below Alpaca min order size (0.0001 BTC) → unsellable as standalone order. Value $3.81 = 0.004% NAV = immaterial. Held passively until the position can be bundled with a future BTC BUY and exited together, or the Alpaca min-notional allows close-position. No stop placed (operationally impossible at this size). Not treated as a Bull-Crypto conviction position.
