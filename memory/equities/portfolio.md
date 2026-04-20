# Portfolio — Equities

> Source of truth = Alpaca API. This file is a **snapshot** written at every `market-close`. Before any decision, refresh via `python scripts/alpaca_client.py positions`.

## Latest snapshot

- **Date**: 2026-04-20T20:00:00Z (market-close, 15:00 CT)
- **Equity total**: $97,382.46
- **Cash available**: $97,378.65
- **Positions value**: $3.81 (BTCUSD residue — out-of-universe, reserved for Bull-Crypto)
- **Cash %**: 99.996%
- **Benchmark close**: SPY $707.80 (-0.33%) / QQQ $646.19 (-0.41%) / blend 676.995 (-0.37%)
- **Day perf**: bot ~0.00% / bench -0.37% → **alpha day +0.37%**
- **Cumul since baseline**: bot 0.00% / bench 0.00% / alpha 0.00% (baseline set today)
- **EOD regime**: late-cycle + geopolitical pullback (US-Iran peace talks at risk, WTI +5% to ~$88.80, VIX 17.48). Confirms morning note — no violent shift.
- **Aging watchlist**: none (0 equity positions)
- **Auto-defense active**: no

## Baseline

- **Starting capital**: $100,000 (paper Alpaca)
- **Baseline date**: 2026-04-20
- **Baseline equity**: $97,382.46
- **SPY baseline**: 707.80
- **QQQ baseline**: 646.19
- **Blend baseline (50/50)**: 676.995

## ATH tracking (for drawdown auto-defense)

- **ATH equity**: $97,382.46
- **ATH date**: 2026-04-20
- **Current drawdown from ATH**: 0.00%

## Open positions

_Regenerated from API at every `market-close`. Format:_

| Ticker | Qty | Avg cost | Price | Value | P&L $ | P&L % | Entry | Age (td) | CTQS | Style | Stop | TP | Catalyst | Status |
|--------|-----|----------|-------|-------|-------|-------|-------|----------|------|-------|------|----|----------|--------|
| BTCUSD (out-of-universe) | 0.000049999 | 73094.17 | 76190.70 | 3.81 | +0.15 | +4.24% | legacy | n/a | n/a | n/a | none | n/a | n/a | to be liquidated by Bull-Crypto or SELL-enabled equities run |

_No equity / ETF / option positions._

## Open risks

- **BTCUSD residue** (out of equities universe): $3.81, carried from legacy. Must be closed by next run authorized to SELL (intraday-scan or Bull-Crypto). Zero exposure risk (0.004% NAV).
- **Earnings cluster Tue 2026-04-21**: INTC, LMT, HON, AXP, TFC, NEE, CMCSA, VRSN, PGR, DOW, KDP, BLK, BX. Bot has no exposure → no pre-earnings exit needed tonight.
- **GEV Q1 earnings Wed 2026-04-22 pre-market** — WATCH only, no position.
- **GOOGL Q1 earnings Tue 2026-04-29 AMC** — WATCH only, no position.
- **Macro 24h**: no top-tier print Tue (FOMC 28–29 avril, PCE later). Continued geopolitical headline risk on Iran / Strait of Hormuz.
