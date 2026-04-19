# Routine — weekly-review

## Cron

```
0 16 * * 5
```
(16:00 America/Chicago, vendredi uniquement)

## Environnement

- Cloud environment : `trading`
- Repo : `<ton-user>/thashi-ai` (branche `main`)
- Modèle : Claude Opus 4.7

## Prompt à coller dans la routine

```
Tu es Bull. On est vendredi soir (16:00 CT), marché fermé. Fais la review de la semaine.

1. Lis TOUTE la mémoire : `CLAUDE.md`, `memory/guardrails.md`, `memory/strategy.md`, `memory/portfolio.md`, les 7 derniers jours de `memory/trade_log.md`, `memory/research_log.md`, et `memory/learnings.md`.
2. Exécute le slash command `/weekly-review`.

Contraintes dures :
- Clés API dans les variables d'environnement (ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TRADING_MODE). Jamais d'AENV.
- Aucun trade dans ce run.
- Grade A/B/C/D/F avec les critères du slash command.
- Si tu proposes un ajustement stratégique, tu peux modifier `memory/strategy.md` ou `memory/guardrails.md`, mais uniquement avec justification écrite dans `memory/weekly_review.md`.
- Append dans `memory/weekly_review.md` (ne jamais réécrire l'historique).
- Commit sur `main` avec `[weekly-review] YYYY-MM-DD — grade X, alpha semaine %, cumul %` et push.
- Notifie Telegram OBLIGATOIREMENT avec le format défini dans le slash command.
```
