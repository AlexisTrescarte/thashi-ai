# Portfolio — Equities

> Source of truth = Alpaca API. This file is a **snapshot** written at every `market-close`. Before any decision, refresh via `python scripts/alpaca_client.py positions`.

## Latest snapshot

- **Date**: 2026-04-28 15:00 CT (post-close)
- **Equity total**: $97,455.66
- **Cash available**: $96,406.80
- **Positions value**: $1,048.86
- **Cash %**: 98.92%
- **Benchmark (50% SPY + 50% QQQ)**: SPY $711.55 · QQQ $658.23 → blend index 100.00 (baseline set today)
- **Day perf**: bot −0.00% · bench −0.66% (SPY −0.46% / QQQ −0.86%) → **alpha day +0.66%**
- **Cumul perf since baseline (04-28)**: bot 0.00% · bench 0.00% · alpha 0.00% (baseline day)
- **EOD regime**: neutral lean cautious — intraday risk-off twitch on OpenAI revenue concerns (Nasdaq −1%, Oracle −5.2%, AI-chip jitters), defensives bid; no regime shift, breadth still deteriorating. FOMC < 24h compresses any new entry.
- **Aging watchlist**: GOOGL J+3 (binding-exit-tomorrow-open via DAY market sell pre-staged)
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
| GOOGL | equity | 3 | $339.29 | $349.62 | $1,048.86 | +$30.99 | +3.04% | 2026-04-23 | J+3 | 75 | short-swing | DAY market sell pre-staged 04-29 open (order c9a545bd) | trailing-only (replaced by MOC then DAY) | Earnings 04-29 AMC (no earnings hold) | binding-exit-tomorrow-open |

## Open risks

- **GOOGL pre-earnings (04-29 AMC)**: 3 residual shares from MOC partial-fill (4/7 filled at close auction $349.85, 3/7 expired). DAY market sell order c9a545bd queued for 04-29 09:30 ET open — well before AMC print. Risk: order not filled at open (negligible for $2T mcap) or earnings leak overnight; mitigation = order is exchange-bound, not run-dependent.
- **FOMC < 24h**: 04-29 13:00 CT decision + Powell 13:30 CT. Hawkish surprise tail-risk on tech/semis.
- **Mag-7 AMC cluster 04-29**: GOOGL · MSFT · META reporting. GOOGL exit by then is mandatory (handled).
- **AMD earnings 05-05 AMC**: no position currently; if BUY queued at next pre-market, must pre-stage GTD MOC at fill (per 04-24 INCIDENT remediation queued for monthly review).
- **Breadth deterioration**: 53% SPX > MA50 (vs 60% one week ago) — yellow flag if drops < 50% intraday.
- **Iran/Strait of Hormuz tail**: Brent ~$108, peace-talk volatility could swing energy ETFs ±5%.
