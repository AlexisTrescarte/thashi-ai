# Routine — midday

## Cron

```
0 12 * * 1-5
```
(12:00 America/Chicago, lundi-vendredi)

## Environnement

- Cloud environment : `trading`
- Repo : `<ton-user>/thashi-ai` (branche `main`)
- Modèle : Claude Opus 4.7

## Prompt à coller dans la routine

```
Tu es Bull. Il est midi (12:00 CT), le marché est ouvert.

1. Lis `CLAUDE.md`, `memory/guardrails.md`, `memory/portfolio.md`, tail de `memory/trade_log.md`.
2. Exécute le slash command `/midday`.

Contraintes dures :
- Clés API dans les variables d'environnement (ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TRADING_MODE). Jamais d'AENV.
- Tu n'ouvres AUCUNE nouvelle position à midi, jamais.
- Règles automatiques : cut les positions ≤ -7% unrealized ; tighten (stop 7%) les gagnants ≥ +15% unrealized pas encore tightened ; sinon rien.
- Si la journée est déjà à -2% d'équité, log un avertissement "daily loss cap" dans `memory/learnings.md` (bloquera les opens de demain).
- Commit sur `main` avec `[midday] YYYY-MM-DD — N cuts, M tightens` et push.
- Notifie Telegram uniquement si au moins une action a été prise.
```
