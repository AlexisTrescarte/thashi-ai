# Stratégie — Bull

## Objectif

Battre le **SPY** (total return) sur le long terme. Benchmark recalculé à chaque `market-close` et consolidé chaque `weekly-review`.

## Philosophie

- **Fundamentals-driven swing**. Horizon moyen par position : 2 à 10 semaines. Pas de day-trading.
- **Conviction over activity**. Mieux vaut 0 trade qu'un trade médiocre. Le cash est une position.
- **Asymétrie** recherchée : thèse qui peut faire +30% si juste, -10% si faux (grâce au trailing stop).

## Signaux d'entrée (au moins 2 parmi)

1. **Catalyseur fondamental clair** : earnings beat + guidance raise, produit lancé, contrat majeur, changement management, rerating analyste multi-sources.
2. **Secular tailwind** : secteur en croissance structurelle (AI infra, GLP-1, defense spending, reshoring, power/grid, cybersecurity).
3. **Valuation raisonnable** : P/E ou EV/EBITDA sous médiane secteur OU croissance revenus > multiple (PEG < 2).
4. **Technique** : le ticker tient sa moyenne mobile 50j, n'est pas > 30% au-dessus de sa MA200 (anti-FOMO).

## Signaux de sortie

- **Trailing stop 10%** atteint.
- **Thèse cassée** : earnings miss matériel, guidance cut, changement narratif secteur. Sortir même en profit.
- **Objectif atteint** : position > +30% ET signal technique de consolidation → trim 50%, tighten stop sur le reste.
- **Rotation** : meilleure opportunité identifiée ET portefeuille full → fermer la position la plus faible (conviction la plus basse) pour financer.

## Allocation cible

- **Core** (50-60%) : positions grande cap, qualité (MSFT, GOOGL, META, NVDA, AMZN, BRK.B, JPM, etc.) selon thèses actives.
- **Thèmes** (20-30%) : plays sur les secular tailwinds (liste à maintenir dans `research_log.md`).
- **Opportuniste** (10-15%) : situations spéciales, rebonds post-earnings, turnarounds.
- **Cash** (>= 10%) : dry powder pour corrections.

## Cadence

- **Pré-marché (06:00 CT)** : scan news, earnings overnight, pré-marché movers. Écrire un plan de trade dans `research_log.md` (pas d'exécution).
- **Open (08:30 CT = 09:30 ET)** : exécuter le plan validé ce matin uniquement. Pas d'improvisation à l'open.
- **Midday (12:00 CT)** : revue des positions, cut les -7%, tighten les gagnants > +15%.
- **Close (15:00 CT = 16:00 ET, juste avant cloche)** : snapshot valeur portefeuille vs SPY, notification ClickUp.
- **Weekly (vendredi 16:00 CT)** : review complète, grade A-F, ajustements stratégie proposés.

## Itération

La stratégie évolue. Chaque `weekly-review` peut proposer des ajustements à ce fichier. Tout changement doit :
1. Être justifié par des observations de `learnings.md` ou `trade_log.md`.
2. Être committé avec un message `[strategy] {résumé}` pour garder l'historique dans git.
