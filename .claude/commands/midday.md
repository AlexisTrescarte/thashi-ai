---
description: Gestion active midi (12:00 CT). Cut les -7%, tighten les gagnants > +15%.
---

Tu es Bull à **midi**. Le marché est en cours. Ton job : nettoyer le portefeuille.

## Étapes obligatoires

1. **Lire la mémoire** : `memory/guardrails.md`, `memory/portfolio.md`, tail de `memory/trade_log.md`.
2. **Vérifier le marché** : `python scripts/alpaca_client.py clock`. Si fermé, termine.
3. **Rafraîchir les positions** : `python scripts/alpaca_client.py positions`. Pour chacune, regarde `unrealized_plpc`.
4. **Décisions** :
   - `unrealized_plpc <= -0.07` (≤ -7%) → **CUT** : `python scripts/alpaca_client.py close {TICKER}`. Annuler aussi le trailing stop en cours (`cancel` si nécessaire).
   - `unrealized_plpc >= 0.15` (≥ +15%) **et pas encore tightened** : annuler le trailing stop actuel (10%) et le remplacer par un trailing stop 7%. Tag la position comme `tightened` dans `portfolio.md`.
   - Sinon : rien. Pas de scalping.
5. **Daily loss cap** : si l'équité est déjà à -2% vs `last_equity` du matin, note dans `learnings.md` un avertissement **"daily loss cap touché"** — ça bloquera toute nouvelle ouverture demain au pre-market.
6. **Log chaque action** dans `trade_log.md` avec le motif (`cut -7%`, `tighten +15%`). Mise à jour `portfolio.md`.
7. **Commit + push** : `git add -A && git commit -m "[midday] YYYY-MM-DD — N cuts, M tightens" && git push origin main`.
8. **Notification Telegram** : **uniquement** si au moins une action a été prise. Format bref :
   ```
   *midday* — YYYY-MM-DD
   Cuts: TICKER1 (-8.2%), TICKER2 (-7.4%)
   Tightened: TICKER3 (+18%)
   Equity: $X,XXX.XX (day %)
   ```

## Interdits

- **NE PAS ouvrir de nouvelle position.** Jamais à midi.
- NE PAS cut un perdant -5% "par prudence". Respecte la règle -7% strictement, sauf si la thèse est cassée (dans ce cas, log dans `learnings.md` et cut).
- NE PAS retoucher le trailing stop d'un gagnant < +15%.
