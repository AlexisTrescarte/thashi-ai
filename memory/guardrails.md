# Garde-fous — règles inviolables

Ces règles priment sur toute décision. Si une action violerait une règle, **tu n'agis pas** et tu consignes la situation dans `learnings.md`.

## Univers d'investissement

- **Actions US uniquement** (NYSE, NASDAQ). Pas d'ETF leveraged (TQQQ, SQQQ, SOXL, etc.). ETF classiques OK (SPY, QQQ, VTI...).
- **Interdit** : options, crypto, forex, futures, short selling.
- **Liquide uniquement** : volume journalier moyen > 1M actions. Pas de penny stocks (< $5 share price).

## Sizing & risk

- **Position max** : 5% de la valeur totale du portefeuille à l'entrée.
- **Top-up autorisé** si total position reste < 8% (conviction haute uniquement).
- **Cash minimum** : garder >= 10% de cash en permanence.
- **Nouvelles positions max** : 3 par semaine.
- **Total positions max** : 15 simultanées (concentration > diversification).

## Stops

- **Trailing stop 10%** posé à l'ouverture de toute nouvelle position.
- **Cut -7%** sur toute position en perte unrealized < -7% depuis l'entrée au check de midday.
- **Tighten** le trailing stop à 7% quand une position est > +15% unrealized.

## Daily / weekly caps

- **Daily loss cap** : si portefeuille perd > 2% sur la journée, stop toute nouvelle ouverture jusqu'au lendemain. Ne pas forcer de sell panique — laisser les stops travailler.
- **Weekly loss cap** : si la semaine est à -5%, passer en mode défensif (weekly-review doit le noter, pas de nouvelle position la semaine suivante).

## Mode

- **Paper par défaut** (`TRADING_MODE=paper` + `ALPACA_BASE_URL` en paper).
- **Passage live** : jamais sans une intervention humaine explicite documentée dans `learnings.md`.

## Hygiène

- **Jamais de secret dans un commit**, jamais de secret dans une notification ClickUp.
- **Jamais supprimer** d'entrée de `trade_log.md` ou `research_log.md`. On ajoute, on ne réécrit pas l'histoire.
- **Format dates ISO** partout : `2026-04-19T13:45:00Z`.
