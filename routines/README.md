# routines/

Ce dossier contient **les 5 routines à créer manuellement dans Claude Desktop**. Chaque fichier décrit :
- le `cron` à coller
- le `prompt` complet à coller
- l'environnement Cloud et le repo à sélectionner

## Procédure (une seule fois)

1. **Pousser ce repo sur GitHub** (privé recommandé).
   ```bash
   gh repo create thashi-ai --private --source=. --remote=origin --push
   ```
2. **Claude Desktop → Routines → Cloud environments → Add**
   - Name : `trading`
   - Network access : **Full** (ou allowlist : `paper-api.alpaca.markets`, `data.alpaca.markets`, `api.telegram.org`, `github.com`, `api.github.com`)
   - Variables :
     - `ALPACA_API_KEY`
     - `ALPACA_SECRET_KEY`
     - `ALPACA_BASE_URL` = `https://paper-api.alpaca.markets`
     - `TELEGRAM_BOT_TOKEN`
     - `TELEGRAM_CHAT_ID`
     - `TRADING_MODE` = `paper`
3. **Pour chacune des 5 routines** (pre-market, market-open, midday, market-close, weekly-review) :
   - New Routine → **Remote**
   - Repo : `<ton-user>/thashi-ai` (branche `main`)
   - Cloud environment : `trading`
   - Model : **Claude Opus 4.7** (ou 4.6 si 4.7 pas dispo dans ton plan)
   - Cron : copier depuis le fichier `.md` correspondant
   - Prompt : copier **tout le bloc de prompt** depuis le fichier `.md` correspondant
   - Permissions → **Allow unrestricted branch pushes** : activer (nécessaire pour committer `memory/` sur `main`)
4. Pour chaque routine, **Run now** au moins une fois pour valider avant de laisser le cron tourner.

## Fuseau horaire

Les crons sont exprimés en `America/Chicago` (comme la vidéo). Si Claude Desktop t'oblige à un autre fuseau, adapte en conséquence :
- 06:00 CT = 11:00 UTC (heure d'été) / 12:00 UTC (heure d'hiver)
- 08:30 CT = 13:30 UTC / 14:30 UTC
- 12:00 CT = 17:00 UTC / 18:00 UTC
- 15:00 CT = 20:00 UTC / 21:00 UTC
- 16:00 CT = 21:00 UTC / 22:00 UTC

## Ordre de test recommandé

1. **market-close** d'abord (snapshot pur, pas de trade) → valide la chaîne Alpaca + Telegram + git push.
2. **weekly-review** → valide la logique de review et les calculs alpha.
3. **pre-market** → valide la recherche + append research_log.
4. **market-open** → valide l'exécution réelle (va passer un ordre paper ! vérifie que c'est bien en `paper-api`).
5. **midday** → valide les cut/tighten (nécessite une position ouverte pour voir quelque chose).
