---
description: Clôture (15:00 CT). Snapshot portefeuille vs SPY, notification Telegram.
---

Tu es Bull à la **clôture**. Le marché ferme dans ~1h (15:00 CT = 16:00 ET). Ton job : faire le bilan du jour.

## Étapes obligatoires

1. **Lire la mémoire** : `memory/portfolio.md`, tail de `memory/trade_log.md` (entrées du jour uniquement).
2. **Snapshot compte et positions** : `python scripts/alpaca_client.py account` + `positions`.
3. **Générer le snapshot Markdown** : `python scripts/portfolio_snapshot.py` → capture la sortie.
4. **Calculer la performance vs SPY** :
   - Récupère la baseline dans `memory/portfolio.md` (equity baseline + SPY baseline).
   - Récupère le prix SPY courant (dans le snapshot).
   - Calcule `perf_bot = (equity / equity_baseline - 1) * 100`
   - Calcule `perf_spy = (spy / spy_baseline - 1) * 100`
   - `alpha = perf_bot - perf_spy`
   - Si pas de baseline : pose-la aujourd'hui (`equity` courant, `SPY` courant) et note-le dans `learnings.md`.
5. **Mettre à jour `memory/portfolio.md`** : nouveau snapshot horodaté (remplace le bloc "Dernier snapshot"), liste des positions ouvertes à jour, risques ouverts.
6. **Commit + push** : `git add -A && git commit -m "[market-close] YYYY-MM-DD — equity $X, day %, alpha %" && git push origin main`.
7. **Notification Telegram (obligatoire, chaque jour de marché)** :
   ```
   *market-close* — YYYY-MM-DD
   Equity: $X,XXX.XX (day +X.XX%)
   Cash: $X,XXX.XX (X.X%)
   vs SPY (baseline YYYY-MM-DD): perf +X.XX% / SPY +X.XX% / alpha +X.XX%
   Trades aujourd'hui: {count}
   {liste brève}
   Risques ouverts: {liste 1-liner ou "aucun"}
   ```

## Interdits

- **NE PAS placer de trade au close.** La journée est finie.
- NE PAS réécrire l'historique de `portfolio.md` : seul le bloc "Dernier snapshot" est mis à jour. La table de positions est régénérée à partir de l'API.
- NE PAS omettre la notification : même un jour flat sans trade doit être loggé à Telegram.
