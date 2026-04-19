---
name: research
description: Recherche structurée sur un ticker ou un thème, avec sources primaires et verdict BUY/WATCH/SKIP. Invoquer à chaque pre-market ou sur demande.
---

# Skill : research

Produit une note de recherche conforme au schéma de `memory/research_log.md`.

## Étapes

1. **Définir le périmètre** : ticker unique (ex: NVDA) ou thème (ex: "défense US 2026").
2. **Collecter des sources primaires** avec `WebSearch` puis `WebFetch` :
   - Site investor relations (earnings releases, 10-Q/10-K, 8-K récents)
   - Communiqués officiels (FDA, DoD, SEC filings)
   - Transcript du dernier earnings call si disponible
3. **Compléter** avec 1-2 sources tierces de qualité (analyst estimates consensus, Bloomberg/Reuters pour contexte macro).
4. **Synthétiser** selon le schéma :
   - **Catalyseur** : 1 phrase, vérifiable dans une source primaire
   - **Sources** : URLs (minimum 2, au moins 1 primaire)
   - **Thèse** : 3-5 lignes, centrée sur les fondamentaux (revenue growth, margin, market position) pas sur le prix
   - **Risques** : 2-4 points concrets (guidance cut, competitor, regulatory, macro)
   - **Plan d'entrée** : prix max acceptable, taille cible en % portfolio (respecter 5% max), trailing stop standard 10%
   - **Temps de détention** : 2-10 semaines
   - **Verdict** : `BUY` (conviction haute, aligné stratégie), `WATCH` (bon mais pas prêt), `SKIP` (fail du screen)
5. **Filtrer contre la stratégie** (`memory/strategy.md`) : au moins 2 signaux d'entrée sur 4. Sinon → `SKIP` avec raison.
6. **Append** dans `memory/research_log.md` avec le timestamp ISO UTC.

## Check-list anti-biais

- La thèse tient sans regarder le prix ? (sinon = FOMO)
- Est-ce que je peux citer un chiffre précis depuis un 10-Q / earnings release ? (sinon = rumeur)
- Le secteur est-il dans `strategy.md` comme tailwind ou au moins neutre ? (sinon = hors mandat)
- Ai-je vérifié que le ticker n'est pas dans la liste de positions fermées récemment avec perte ? (éviter revenge trade — check `trade_log.md`)

## Sortie

Append dans `memory/research_log.md`. **Ne pas** produire de message Telegram — c'est le boulot du slash command parent (pre-market notifie uniquement si urgent).
