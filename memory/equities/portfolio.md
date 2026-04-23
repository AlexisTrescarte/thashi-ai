# Portfolio — Equities

> Source of truth = Alpaca API. This file is a **snapshot** written at every `market-close`. Before any decision, refresh via `python scripts/alpaca_client.py positions`.

## Latest snapshot

- **Date**: 2026-04-23T20:05:00Z (15:05 CT, market close)
- **Equity total**: $97,379.63
- **Cash available**: $95,007.40
- **Positions value**: $2,372.23
- **Cash %**: 97.56%
- **Benchmark (50% SPY + 50% QQQ)**: baseline set today — bench_index = 100.00
- **Day perf**: bot -0.003% · bench ≈ -0.65% (SPY -0.40% / QQQ -0.90%) · alpha day +0.65pp
- **Cumul since baseline**: bot 0.00% · bench 0.00% · alpha 0.00% (J0)
- **EOD regime**: neutral, lean risk-off intraday (oil +4% shock on Iran/Hormuz uncertainty, software -massive: NOW -17%, IBM -8%). Morning "lean risk-on" broke by midday. No full regime shift per guardrails (VIX move < 15%), flagged as micro rotation.
- **Aging watchlist**: GOOGL (J+0, mandatory time stop 2026-04-28 close pre-earnings 04/29 AMC)
- **Auto-defense active**: no

## Baseline

- **Starting capital**: $100,000 (paper Alpaca)
- **Baseline date**: 2026-04-23
- **Equity baseline**: $97,379.63
- **SPY baseline**: $688.15 (Alpaca close quote 20:00:02Z)
- **QQQ baseline**: $652.88 (Alpaca mid 652.85/652.92 at 20:05:35Z)
- **Bench index baseline**: 100.00 (normalized 50/50 blend)

> Rationale: portfolio.md previously had no explicit baseline date. Setting today (first clean close snapshot) as J0. Equity $97,379.63 is below the nominal $100,000 starting capital because prior runs (20-22/04) included a residual BTCUSD line (since reattributed to the crypto agent) and no equities positions were held on those dates. Log in `memory/learnings.md`.

## ATH tracking (for drawdown auto-defense)

- **ATH equity**: $97,382.43 (date 2026-04-22, last_equity at today's close)
- **ATH date**: 2026-04-22
- **Current drawdown from ATH**: -0.003%

## Open positions

_Regenerated from API at every `market-close`._

| Ticker | Instr | Qty | Avg cost | Price | Value | P&L $ | P&L % | Entry | Age (td) | CTQS | Style | Stop | TP | Catalyst | Status |
|--------|-------|-----|----------|-------|-------|-------|-------|-------|----------|------|-------|------|----|----------|--------|
| GOOGL | equity | 7 | $339.29 | $338.89 | $2,372.23 | -$2.80 | -0.12% | 2026-04-23 | J+0 | 75 | short-swing | trail 8% @ $314.60 (HWM $341.96) | trailing | Earnings 2026-04-29 AMC (J-4); TPU 8t/8i + Anthropic multi-GW fuse | normal |

## Open risks

- **GOOGL earnings 2026-04-29 AMC** → mandatory pre-earnings exit 2026-04-28 close (no "earnings hold" in entry thesis). 3 trading days to time stop.
- **PCE core 2026-04-25 BMO** → macro catalyst end of week; stops already disciplined, no change.
- **FOMC 2026-04-28 → 04-29** → hold quasi-certain (94.8%) but dot plot risk; per guardrails sizing one notch down from 2026-04-27 onwards + options max premium halved for event window (no options in book → non-binding).
- **INTC AMC tonight 2026-04-23** → not in book; SMH/AVGO/NVDA re-rating risk tomorrow open (may bleed into GEV/VRT if AI capex narrative breaks).
- **Iran war / Strait of Hormuz** → WTI +4% today, if re-escalation continues expect further rotation energy-up / tech-down; flag for tomorrow pre-market.
- **No position without stop**: GOOGL trailing 8% Alpaca native (id 45d94a3c) active, HWM ratcheting — guardrail respected.
- **No option position**: DTE concerns N/A.
- **Aging time stops imminent**: GOOGL J+0 today → J+3 at 04/28 close (in-plan exit).
