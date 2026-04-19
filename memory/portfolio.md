# Portefeuille

> Source de vérité = API Alpaca. Ce fichier est un **snapshot** écrit à chaque `market-close`. Avant toute décision, rafraîchis via `scripts/alpaca_client.py positions`.

## Dernier snapshot

- **Date** : _(à remplir au premier run)_
- **Equity total** : $— (cash + positions valorisées)
- **Cash disponible** : $—
- **Valeur positions** : $—
- **% cash** : —
- **SPY benchmark** : — (prix close du jour)
- **Performance vs SPY depuis baseline** : —

## Baseline

- **Capital de départ** : $100,000 (paper account Alpaca)
- **Date de baseline** : _(date du premier run live du bot)_
- **SPY de baseline** : _(prix de SPY le jour du baseline)_

## Positions ouvertes

_Mis à jour à chaque `market-close`. Format :_

| Ticker | Qty | Avg cost | Prix actuel | Valeur | P&L $ | P&L % | Date entrée | Thèse courte |
|--------|-----|----------|-------------|--------|-------|-------|-------------|--------------|

## Risques ouverts

- _Positions sans thèse claire, stops manquants, drawdowns actifs, etc. Listés à chaque close._
