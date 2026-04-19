---
name: trade
description: Exécute un BUY / SELL / TRIM / ADD / CUT / tighten-stop sur Alpaca avec vérifs guardrails. Invoquer depuis market-open et midday.
---

# Skill : trade

Place un ordre sur Alpaca en respectant `memory/guardrails.md`. Pas de décision stratégique ici — on suppose qu'une note de recherche valide existe ou qu'une règle midday déclenche l'action.

## Préconditions (vérifier avant l'ordre)

1. Le marché est ouvert (`alpaca_client.py clock`).
2. Les clés sont présentes (sinon le script crashera de toute façon).
3. `TRADING_MODE` est cohérent avec `ALPACA_BASE_URL` (paper / live).

## BUY

1. Récupérer `account` → `equity`, `cash`.
2. Récupérer `quote {TICKER}` → prix ask courant.
3. Calculer `qty = floor((target_pct * equity) / ask)`. `target_pct` ≤ 5%.
4. **Gates** :
   - cash post-trade ≥ 10% × equity
   - nouvelles positions de la semaine < 3 (compter dans `trade_log.md`)
   - ticker conforme à l'univers (pas penny < $5, volume OK) — skip si unknown
5. Exécuter : `python scripts/alpaca_client.py buy {TICKER} {QTY}`.
6. Si `status=filled` ou `accepted` : poser **immédiatement** `trailing-stop {TICKER} {QTY} 10`.
7. **Log** dans `trade_log.md` :
   ```
   ### 2026-04-20T13:30:00Z — BUY NVDA 15@$912.34
   - Order ID: xxx
   - Valeur: $13,685.10
   - % portfolio: 4.8%
   - Thèse: (copier depuis research_log.md, 1 ligne)
   - Trailing stop: 10% (order ID yyy)
   - Routine: market-open
   - Research: 2026-04-20T11:05:00Z
   ```

## CUT (perte -7% ou thèse cassée)

1. `close {TICKER}` — ferme la position au marché.
2. Annuler les stops en cours pour ce ticker : lister `orders --status open`, cancel ceux du ticker.
3. Log dans `trade_log.md` avec motif (`cut -7%` ou `thèse cassée: raison`).

## TRIM (gagnant > +30% sur signal)

1. Calculer `qty_trim = floor(current_qty * 0.5)`.
2. `sell {TICKER} {qty_trim}`.
3. Annuler le trailing stop actuel (couvrait la qty totale) et en poser un nouveau sur `current_qty - qty_trim` à 7%.
4. Log.

## TIGHTEN (gagnant > +15%)

1. Lister les stops ouverts pour le ticker, les `cancel`.
2. Poser un nouveau trailing stop 7% sur la qty pleine.
3. Marquer la position `tightened` dans `portfolio.md`.

## Échecs

- Ordre rejeté (insufficient buying power, pattern day trader, asset halted) : log `learnings.md` avec la réponse API brute, notifier Telegram `DEGRADED`.
- Quote KO : retry 1x après 5s ; si toujours KO, skip ce trade, log, continuer.
