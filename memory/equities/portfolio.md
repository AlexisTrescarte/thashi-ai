# Portfolio — Equities

> Source of truth = Alpaca API. This file is a **snapshot** written at every `market-close`. Before any decision, refresh via `python scripts/alpaca_client.py positions`.

## Latest snapshot

- **Date**: 2026-04-29 15:00 CT (post-close)
- **Equity total**: $97,443.92
- **Cash available**: $97,443.92
- **Positions value**: $0.00
- **Cash %**: 100.00%
- **Benchmark (50% SPY + 50% QQQ · base 04-28)**: SPY ~$710.13 · QQQ ~$655.53 → blend index ≈ 99.70
- **Day perf**: bot −0.01% · bench −0.31% (SPY −0.20% / QQQ −0.41%) → **alpha day +0.29%**
- **Cumul perf since baseline (04-28)**: bot −0.01% · bench −0.31% · **alpha +0.29%**
- **EOD regime**: neutral lean cautious — Fed 8-4 split hold (first 4-dissent vote since 1992, hawkish tilt vs dovish consensus), Powell's likely final press conf as chair (Warsh confirmation expected 05-15), Mag-7 AMC tonight (GOOGL/MSFT/META/AMZN), Iran/Hormuz tail keeping oil bid (+3%). No regime-shift trigger (VXX ~$29 flat, no credit event); breadth still deteriorating (Russell −1.15%).
- **Aging watchlist**: none — book empty post-GOOGL exit at the open
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
| _none_ | — | — | — | — | — | — | — | — | — | — | — | — | — | — | empty book |

## Open risks

- **Mag-7 AMC cluster tonight**: GOOGL · MSFT · META · AMZN report after the close. Book is 100% cash so no direct gap exposure; tomorrow's pre-market is the main redeployment event.
- **Powell press conf tail**: 8-4 dissent vote (first since 1992) introduced a hawkish micro-shift; Warsh confirmation 05-15 brings leadership-transition risk into May. Watch for follow-through tomorrow on rate-sensitives.
- **Iran/Strait of Hormuz**: Trump confirmed continued blockade, oil up >3% intraday. Energy ETFs (XLE/USO) remain a single-event tail; Brent path-dependent.
- **AMD earnings 05-05 AMC**: no current position; if BUY queued at next pre-market, must pre-stage GTD MOC at fill + 14:30 last-call IOC fallback (04-24 + 04-28 remediation).
- **Breadth deterioration persists**: Russell −1.15% today, S&P −0.20%, Nasdaq −0.41%. % SPX > MA50 likely sub-50 line — yellow flag for risk-on entries until breadth re-inflates.
- **Pre-market silence pattern**: 4 of last 6 weekday pre-market slots missed. Already on monthly-deep-review queue alongside the GTD-exit-at-fill remediation.
- **Activity floor below target**: rolling 5td BUY count = 1 (GOOGL 04-23, now closed). Floor target ≥3 in risk-on/neutral regime. Discipline holds: post-FOMC + post-Mag-7 setup tomorrow is the right place to close the gap, not a forced low-CTQS BUY.
