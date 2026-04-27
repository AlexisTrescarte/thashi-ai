# Portfolio — Equities

> Source of truth = Alpaca API. This file is a **snapshot** written at every `market-close`. Before any decision, refresh via `python scripts/alpaca_client.py positions`.

## Latest snapshot

- **Date**: 2026-04-27T20:10:00Z (15:10 CT)
- **Equity total**: $97,461.39
- **Cash available**: $95,007.40
- **Positions value**: $2,453.99
- **Cash %**: 97.48%
- **Benchmark (50% SPY + 50% QQQ)**: SPY $714.89 / QQQ $663.82 → blend index $689.36
- **Day perf**: bot +0.044% · bench +0.041% · alpha day +0.003 pp
- **Performance vs benchmark since baseline**: bot +0.00% · bench +0.00% · alpha 0.00 pp (baseline set today — first market-close routine to fire after multiple missed market-close runs 04-20 / 04-24)
- **EOD regime**: neutral lean risk-on — VIX 18.71 (-3.11%), SPX +0.80% to 7,165 ATH, US10Y ~4.32%, no regime-shift trigger; mega-cap earnings cluster begins tomorrow (MSFT/META/GOOGL Wed 04-29 AMC, AAPL/AMZN Thu 04-30) + FOMC 04-28/29
- **Aging watchlist**: GOOGL J+2 (normal) — time-stop-next-session (04-28 close mandatory pre-earnings exit)
- **Auto-defense active**: no
- **Daily/weekly loss caps**: not active (day +0.04%, week tracking starts here)

## Baseline

- **Starting capital**: $100,000 (paper Alpaca)
- **Baseline date**: 2026-04-27 (set this run — first market-close routine to actually post a baseline)
- **Equity baseline**: $97,461.39
- **SPY baseline**: $714.89
- **QQQ baseline**: $663.82
- **Bench index baseline**: $689.36 (50/50 blend)

## ATH tracking (for drawdown auto-defense)

- **ATH equity**: $97,461.39
- **ATH date**: 2026-04-27 (initialized at baseline — paper account funded $100,000, current equity $97,461.39 reflects pre-baseline drift; ATH tracking begins fresh at baseline level per market-close routine spec)
- **Current drawdown from ATH**: 0.00%

## Open positions

_Regenerated from API at every `market-close`._

| Ticker | Type | Qty | Avg cost | Price | Value | P&L $ | P&L % | Entry | Age (td) | CTQS | Style | Stop | TP | Catalyst | Status |
|--------|------|-----|----------|-------|-------|-------|-------|-------|----------|------|-------|------|----|----------|--------|
| GOOGL | equity | 7 | $339.29 | $350.57 | $2,453.99 | +$78.96 | +3.33% | 2026-04-23 | J+2 | 75 (Probe) | short-swing | trail 8% native HWM $353.18 / stop $324.93 (GTC, ratchet active) | trailing only | Earnings Q1 2026 Wed 04-29 AMC + TPU 8t/8i + Anthropic deal | normal · time-stop-next-session (mandatory exit 04-28 close pre-earnings) |

## Open risks

- **Pre-earnings exit GOOGL Wed 04-29 AMC** — mandatory CUT tomorrow Tue 04-28 at 14:30 CT last-call slot or market-close routine (whichever fires first); no "earnings hold" in entry thesis. Native trail at $324.93 is the only backstop if both 04-28 routines miss (would expose position to earnings binary).
- **Mega-cap earnings cluster Wed–Thu** — MSFT, META, AMZN, AAPL all reporting; potential broad market vol Thu open. Watch for VIX spike.
- **FOMC Tue–Wed (04-28/29)** — hold consensus 94.8%, dot plot risk. Sizing one notch down per guardrails for any new BUY (n/a today, but relevant for tomorrow's pre-market).
- **Imminent time stops**: GOOGL 04-28 close (J+3 hard exit per entry plan).
- **Options DTE ≤ 4**: none (no options held).
- **Activity-floor gap**: 1 BUY / 5 trading days vs target ≥ 1/3 and ≥ 3/5 — GEV/VRT skipped 04-23 (spread + FOMO) never re-attempted (04-24 missed routines, 04-27 no fresh pre-market block); will re-score 04-28 pre-market.
