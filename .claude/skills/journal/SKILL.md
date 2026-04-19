---
name: journal
description: Met à jour la mémoire (trade_log, portfolio, learnings, research_log, weekly_review) à la fin d'un run, commit et push. Invoquer à la fin de chaque routine.
---

# Skill : journal

Discipline de mémoire : append-only sur les logs, overwrite contrôlé sur les snapshots. Commit + push à chaque run sinon les prochaines routines repartent à zéro.

## Règles

- **Append-only** : `trade_log.md`, `research_log.md`, `weekly_review.md`, `learnings.md`. Ne jamais réécrire l'historique.
- **Overwrite contrôlé** : `portfolio.md` (bloc "Dernier snapshot" + table positions rafraîchie). `strategy.md` / `guardrails.md` uniquement via weekly-review.
- **Horodatage ISO UTC** partout : `2026-04-20T13:45:00Z`.
- **Ne jamais commiter `.env`, un secret, ou un transcript Telegram complet**.

## Étapes de fin de run

1. Écrire les appends dans les fichiers appropriés.
2. `git status` pour vérifier ce qui va être commit.
3. `git diff --stat` pour s'assurer qu'aucun fichier inattendu n'est modifié.
4. `git add -A`
5. `git commit -m "[{routine}] YYYY-MM-DD — {résumé 1 ligne}"`
6. `git push origin main`
7. Si le push échoue : append dans `learnings.md` un incident `[INCIDENT] push failed: ...`, notifier Telegram `DEGRADED`. Ne pas retry en boucle.

## Formats de commit

- `[pre-market] 2026-04-20 — 2 idées, 1 position à surveiller`
- `[market-open] 2026-04-20 — 1 trade (BUY NVDA 15)`
- `[midday] 2026-04-20 — 1 cut (META -7.4%), 0 tighten`
- `[market-close] 2026-04-20 — equity $97,432, day +0.32%, alpha +0.12%`
- `[weekly-review] 2026-04-24 — grade B, semaine +1.8%, alpha +0.4%`

## Anti-bruit

Si rien ne justifie un commit (ex: pre-market sans idée, midday sans action) :
- Commit quand même un snapshot minimal dans le fichier `memory/runs.log` (append d'une ligne `YYYY-MM-DDTHH:MM:SSZ [{routine}] noop: raison`).
- But : garder la trace que la routine a bien tourné.
