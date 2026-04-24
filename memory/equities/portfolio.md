# Portfolio — Equities

> Source of truth = Alpaca API. This file is a **snapshot** written at every `market-close`. Before any decision, refresh via `python scripts/alpaca_client.py positions`.

## Latest snapshot

- **Date**: 2026-04-24 15:00 CT (market-close)
- **Equity total**: $97,415.40
- **Cash available**: $95,007.40
- **Positions value**: $2,408.00
- **Cash %**: 97.53%
- **Positions count**: 1 (1 equity · 0 ETF · 0 lev-ETF · 0 option)
- **Benchmark (50% SPY + 50% QQQ)**: SPY $713.33 · QQQ $655.95 (baseline set today, see below)
- **Day perf**: bot +0.04% · bench +1.21% · alpha_day **-1.18%**
- **Cumul perf since baseline**: bot 0.00% · bench 0.00% · alpha 0.00% (baseline = today)
- **EOD regime**: risk-on tech-led rally — S&P +0.80%, Nasdaq +1.63%, Dow -0.16%; NVDA back above $5T; VIX 18.69 (-3.21%); 10Y 4.32% flat; DXY 98.57 (-0.21%). Tech/semis lead, Energy lags. Confirms morning "neutral lean risk-on" read, with a clear tech-megacap bid into next week's mega-earnings.
- **Aging watchlist**: none (only position GOOGL at J+1, normal)
- **Auto-defense active**: no

## Baseline

- **Starting capital**: $100,000 (paper Alpaca)
- **Baseline date**: 2026-04-24 (set at first market-close with populated snapshot — see `memory/learnings.md` 2026-04-24T20:00:00Z note)
- **Equity baseline**: $97,415.40
- **SPY baseline**: $713.33 (close 2026-04-24)
- **QQQ baseline**: $655.95 (close 2026-04-24)
- **Bench blend baseline**: 50/50 SPY+QQQ, tracked going forward as `0.5 × SPY_today/SPY_baseline + 0.5 × QQQ_today/QQQ_baseline − 1`

## ATH tracking (for drawdown auto-defense)

- **ATH equity**: $97,415.40 (baseline = ATH at start)
- **ATH date**: 2026-04-24
- **Current drawdown from ATH**: 0.00%

## Open positions

_Regenerated from API at every `market-close`. Format:_

| Ticker | Type   | Qty | Avg cost | Price   | Value    | P&L $  | P&L % | Entry       | Age (td) | CTQS | Style       | Stop                         | TP        | Catalyst                          | Status |
|--------|--------|-----|----------|---------|----------|--------|-------|-------------|----------|------|-------------|------------------------------|-----------|-----------------------------------|--------|
| GOOGL  | equity | 7   | $339.29  | $344.00 | $2,408.00| +$32.97| +1.39%| 2026-04-23  | J+1      | 75   | short-swing | 8% trailing · stop $317.61 (hwm $345.23) | trailing only | Earnings Q1 2026-04-29 AMC · TPU/Anthropic | normal — time-stop 2026-04-28 close (no earnings hold) |

## Open risks

- **Pre-earnings exit due 2026-04-28 close (GOOGL)** — mandatory, no earnings hold; will be enforced at Tuesday market-close or earlier if stop trips. Next pre-market/intraday-scan must track.
- **Mega-cap earnings cluster week of 04/28** — MSFT & META 4/28 AMC, GOOGL & AMZN 4/29 AMC, AAPL 4/30 AMC. Implied tape volatility high; tighten discipline on any new entry.
- **FOMC 4/28-29** (statement 4/29 14:00 ET, Powell presser 14:30 ET). Market prices 85% hold at 3.50-3.75%, non-SEP meeting → full weight on statement wording. Any entry Monday-Tuesday must respect the event-risk guardrail.
- **Concentration risk = none** (single 2.47% equity position, 97.53% cash). Risk-OFF is opportunity-cost risk: bot lagged the +1.21% bench blend today; keep BUY queue primed for Monday.
- **Options at DTE ≤ 4**: none (no option exposure).
