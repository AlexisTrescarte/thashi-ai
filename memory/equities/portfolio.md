# Portfolio — Equities

> Source of truth = Alpaca API. This file is a **snapshot** written at every `market-close`. Before any decision, refresh via `python scripts/alpaca_client.py positions`.

## Latest snapshot

- **Date**: 2026-04-30 15:00 CT (post-close)
- **Equity total**: $97,529.08
- **Cash available**: $90,158.23
- **Positions value**: $7,370.85
- **Cash %**: 92.44%
- **Benchmark (50% SPY + 50% QQQ · base 04-28)**: SPY $715.67 · QQQ $662.23 → blend index 100.59
- **Day perf**: bot +0.09% · bench +0.05% (SPY +0.11% / QQQ −0.02% est. from 04-29 inferred close) → **alpha day +0.04%**
- **Cumul perf since baseline (04-28)**: bot +0.08% · bench +0.59% · **alpha −0.52%**
- **EOD regime**: neutral lean risk-on — Mag-7 dispersion continued (LLY +9.7%, GOOGL +10.4% PEAD pops vs MSFT/META weakness), VIX ~18, 10Y ~4.39%, broad indices closed positive. FOMC cleared 04-29 (hold + 8-4 dissent). No regime shift; alpha drag is structural (cash-heavy book entered 04-28 baseline at 99% cash, only 7.6% deployed by today's close).
- **Aging watchlist**: none — both positions J+0 (entered 04-30), normal short-swing band
- **Auto-defense active**: no

## Baseline

- **Starting capital**: $100,000 (paper Alpaca, opened 2024-04-07)
- **Baseline date**: 2026-04-28 (formal baseline set this session — first explicit baseline since portfolio.md template)
- **Equity baseline**: $97,455.66
- **SPY baseline**: $711.55 (mid Alpaca quote 20:00 UTC)
- **QQQ baseline**: $658.23 (mid Alpaca quote 20:00 UTC)
- **Note**: implicit pre-baseline drawdown from paper start −2.54% ($100k → $97.46k); formal alpha tracking begins 2026-04-28.

## ATH tracking (for drawdown auto-defense)

- **ATH equity**: $100,000 (implicit from paper start; will reset on first equity > $100k)
- **ATH date**: 2024-04-07 (paper account open)
- **Current drawdown from ATH**: −2.54%

## Open positions

_Regenerated from API at every `market-close`._

| Ticker | Type | Qty | Avg cost | Last | Value | P&L $ | P&L % | Entry | Age (td) | CTQS | Style | Stop | TP | Catalyst | Status |
|--------|------|-----|----------|------|-------|-------|-------|-------|----------|------|-------|------|----|----------|--------|
| GOOGL | equity | 7 | $369.71 | $386.26 | $2,703.83 | +$115.85 | +4.48% | 2026-04-30 | J+0 | 75 (Probe) | short-swing PEAD | 7% trailing GTC (74ec67e0) HWM $385.84 stop $358.83 | trailing-only | PEAD on Q1 2026 beat (rev $109.9B, Cloud +63%) — next earnings ~late July 2026 | normal |
| LLY | equity | 5 | $939.54 | $933.63 | $4,668.15 | −$29.55 | −0.63% | 2026-04-30 | J+0 | 80 (Standard) | short-swing PEAD | 7% trailing GTC (8e54102c) HWM $945.50 stop $879.31 | trailing-only | PEAD on Q1 2026 beat+raise (rev $19.8B +56% YoY, FY raised) — next earnings ~late July 2026 | normal |

## Open risks

- **LLY day-1 PEAD fade (J+0)**: late-day entry into +9.7% pop closed −0.63% from fill — moderate fade-risk overnight. Trail stop $879.31 = 5.8% room from current $933.63. Time stop 2026-05-07 close (J+5 short-swing). No earnings hold needed (next report late July).
- **GOOGL D+1 PEAD continuation (J+0)**: +4.48% from fill, trail engaged with HWM $385.84 / stop $358.83. Native one-way ratchet. Time stop 2026-05-07 close.
- **AMD earnings 05-05 AMC**: queued for next pre-market; if BUY surfaces, must pre-stage GTD MOC at fill (per 04-24 INCIDENT remediation).
- **Sector concentration check**: GOOGL 2.77% NAV (tech) + LLY 4.79% NAV (healthcare) = 7.56% deployed. Tech sector cap 25% headroom intact; healthcare cap 25% headroom intact.
- **Cash floor check**: 92.44% cash — well above 10% mandatory floor.
- **Journal-commit health**: 3 commit failures in past 5 trading days flagged in learnings (04-25 / 04-27 / 04-30 pre-market+market-open). Monthly-review proposal queued.
