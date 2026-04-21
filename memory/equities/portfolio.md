# Portfolio — Equities

> Source of truth = Alpaca API. This file is a **snapshot** written at every `market-close`. Before any decision, refresh via `python scripts/alpaca_client.py positions`.

## Latest snapshot

- **Date**: 2026-04-21T20:00:00Z (15:00 CT market-close)
- **Equity total**: $97,382.43
- **Cash available**: $97,382.43
- **Positions value**: $0.00
- **Cash %**: 100.00%
- **Total positions**: 0 (0 equity · 0 ETF · 0 lev-ETF · 0 option)
- **Benchmark (50% SPY + 50% QQQ)**: blend 676.875 (SPY 706.96 · QQQ 646.79)
- **Day perf**: bot 0.00% · bench -0.48% (SPY -0.63% · QQQ -0.32%) · alpha day +0.48%
- **Cumul since baseline (2026-04-21)**: bot 0.00% · bench 0.00% · alpha +0.00%
- **EOD regime**: late-cycle, risk-off intraday — SPX -0.63% depuis l'ATH du 17/04, VIX 20.52 (+8.75%), WTI +4.5% sur tensions US-Iran, or -2.68%, 10Y à 4.30% (2Y 3.72%, 2s10s +58bp)
- **Aging watchlist**: aucune (0 positions)
- **Auto-defense active**: no (drawdown 0.00% from ATH $97,382.43)

## Baseline

- **Starting capital**: $100,000 (paper Alpaca) — portefeuille déjà à $97,382.43 au démarrage du tracking
- **Baseline date**: 2026-04-21
- **Equity baseline**: $97,382.43
- **SPY baseline**: 706.96 (close 2026-04-21)
- **QQQ baseline**: 646.79 (close 2026-04-21)
- **Blend baseline (50/50)**: 676.875

## ATH tracking (for drawdown auto-defense)

- **ATH equity**: $97,382.43
- **ATH date**: 2026-04-21
- **Current drawdown from ATH**: 0.00%

## Open positions

_Regenerated from API at every `market-close`. Format:_

| Ticker | Qty | Avg cost | Price | Value | P&L $ | P&L % | Entry | Age (td) | CTQS | Style | Stop | TP | Catalyst | Status |
|--------|-----|----------|-------|-------|-------|-------|-------|----------|------|-------|------|----|----------|--------|
| _(aucune position ouverte au market-close du 2026-04-21)_ |

## Open risks

- **Baseline posée aujourd'hui** : cumul perf/alpha démarre à 0% à partir du 2026-04-21 close. Toutes les métriques ultérieures seront référencées à ce point.
- **Cluster earnings mercredi 2026-04-22 pre-market** : GEV (watchlist — pas d'entrée avant rapport, voir research_log 2026-04-20). Surveiller réaction pour pre-market du 22/04.
- **FOMC 28-29 avril** : hold à 99% de probabilité (range 3.50-3.75%) mais wording de Powell à scruter ; earnings-week + FOMC + VIX qui remonte = event-risk cluster.
- **US-Iran** : ceasefire du 7 avril fragile, négociations en pause (suspension du trip Vance au Pakistan). WTI +4.5% aujourd'hui, VIX +8.75%. Régime à surveiller lors du pre-market.
- **GOOGL earnings 29/04 AMC** : pas d'entrée avant résultats (préférence scénario B).
- **Dry powder intact** : 100% cash, bien au-dessus du floor 10%. Pas d'exposition, pas de stop à gérer, pas de P&L exposé.
