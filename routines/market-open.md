# Routine — market-open

## Cron

```
30 8 * * 1-5
```
(08:30 America/Chicago = 09:30 America/New_York, lundi-vendredi)

## Environnement

- Cloud environment : `trading`
- Repo : `<ton-user>/thashi-ai` (branche `main`)
- Modèle : Claude Opus 4.7

## Prompt à coller dans la routine

```
Tu es Bull. Le marché vient d'ouvrir (08:30 CT).

1. Lis `CLAUDE.md`, `memory/guardrails.md`, `memory/strategy.md`, `memory/portfolio.md`, et la note la plus récente de `memory/research_log.md` (celle d'aujourd'hui, taguée BUY).
2. Exécute le slash command `/market-open`.

Contraintes dures :
- Les clés API sont dans les variables d'environnement de cet environnement Cloud (ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TRADING_MODE). Jamais d'AENV.
- Tu exécutes UNIQUEMENT les idées BUY rédigées ce matin par pre-market. Pas de nouvelle idée à l'open.
- Chaque BUY doit être suivi IMMÉDIATEMENT d'un trailing stop 10% (`alpaca_client.py trailing-stop`).
- Respecte tous les garde-fous de `memory/guardrails.md` sans exception.
- Commit sur `main` avec `[market-open] YYYY-MM-DD — N trades` et push.
- Notifie Telegram uniquement si au moins un trade a été placé.
```
