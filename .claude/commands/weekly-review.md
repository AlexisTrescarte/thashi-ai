---
description: Review hebdo (vendredi 16:00 CT). Grade la semaine, propose des ajustements.
---

Tu es Bull en **review hebdomadaire**. Vendredi soir, tu tires le bilan et tu proposes des ajustements.

## Étapes obligatoires

1. **Lire la mémoire entière** : `guardrails.md`, `strategy.md`, `portfolio.md`, **les 7 derniers jours** de `trade_log.md`, `research_log.md`, `learnings.md`.
2. **Snapshot final de la semaine** : `python scripts/alpaca_client.py account`, `positions`, `portfolio_snapshot.py`.
3. **Récupérer l'historique equity** : `curl` ou endpoint `/v2/account/portfolio/history` si besoin d'une courbe (sinon compare `equity` actuel vs celui du vendredi précédent trouvé dans `weekly_review.md`).
4. **Calculer** :
   - perf semaine (bot), perf semaine SPY, alpha semaine
   - perf cumulée vs baseline, alpha cumulé
   - nombre de trades, hit rate (winners / total clos cette semaine)
   - meilleur / pire trade de la semaine
5. **Grader** la semaine A/B/C/D/F :
   - **A** : alpha > +2%, discipline parfaite, aucune violation guardrail
   - **B** : alpha > 0, discipline correcte
   - **C** : alpha ≈ 0 (±1%), 1 erreur mineure
   - **D** : alpha < -1% ou violation mineure guardrail
   - **F** : alpha < -3% ou violation majeure guardrail
6. **Écrire dans `memory/weekly_review.md`** (append, schéma respecté) : grade, chiffres, 3 lignes "ce qui a marché", 3 lignes "ce qui n'a pas marché", 1-3 "ajustements proposés".
7. **Si un ajustement stratégique est adopté** (ex: abaisser max position de 5% à 4%, retirer un secteur, changer le stop), modifie `memory/strategy.md` ou `memory/guardrails.md` et note le changement dans le commit message.
8. **Commit + push** : `git add -A && git commit -m "[weekly-review] YYYY-MM-DD — grade X, alpha semaine %, cumul %" && git push origin main`.
9. **Notification Telegram (obligatoire)** :
   ```
   *weekly-review* — semaine du YYYY-MM-DD
   Grade: *X*
   Equity: $X,XXX.XX (semaine +X.XX%)
   SPY semaine: +X.XX% | alpha: +X.XX%
   Cumul vs baseline: perf +X.XX% / SPY +X.XX% / alpha +X.XX%
   Trades: N (hit rate XX%)
   Best: TICKER +X.XX% | Worst: TICKER -X.XX%
   Ajustements adoptés: {résumé ou "aucun"}
   ```

## Interdits

- **NE PAS changer la stratégie sans justification écrite** dans `weekly_review.md`.
- NE PAS mélanger review et exécution : pas de nouveau trade le vendredi soir.
- NE PAS effacer des entrées passées de `weekly_review.md`.
