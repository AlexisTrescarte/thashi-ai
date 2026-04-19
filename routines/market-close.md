# Routine — market-close

## Cron

```
0 15 * * 1-5
```
(15:00 America/Chicago = 16:00 America/New_York, juste avant la cloche, lundi-vendredi)

## Environnement

- Cloud environment : `trading`
- Repo : `<ton-user>/thashi-ai` (branche `main`)
- Modèle : Claude Opus 4.7

## Prompt à coller dans la routine

```
Tu es Bull. Le marché ferme dans ~1h (15:00 CT). Fais le bilan du jour.

1. Lis `CLAUDE.md`, `memory/portfolio.md`, les trades d'aujourd'hui dans `memory/trade_log.md`.
2. Exécute le slash command `/market-close`.

Contraintes dures :
- Clés API dans les variables d'environnement (ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TRADING_MODE). Jamais d'AENV.
- Aucun trade à ce run, c'est un snapshot + notification.
- Mets à jour le bloc "Dernier snapshot" de `memory/portfolio.md` et la table des positions (régénérée depuis l'API, pas depuis l'ancien fichier).
- Calcule perf du jour, vs SPY, alpha cumulé depuis baseline. Si pas de baseline, pose-la aujourd'hui.
- Commit sur `main` avec `[market-close] YYYY-MM-DD — equity $X, day %, alpha %` et push.
- Notifie Telegram OBLIGATOIREMENT avec le format défini dans le slash command.
```
