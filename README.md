# thashi-ai — Bull, agent de trading 24/7

Agent Claude Code qui tourne sur cron via les **Routines** Claude Code. Objectif : battre le S&P 500 en paper trading (ou live si tu veux) via Alpaca.

## TL;DR — setup en 5 min

1. **Comptes API à créer**
   - Alpaca : https://alpaca.markets → Paper trading account → génère API key + secret
   - Telegram : parle à **@BotFather**, `/newbot`, récupère le **token**. Envoie un message au bot, puis ouvre `https://api.telegram.org/bot<TOKEN>/getUpdates` pour lire ton **chat_id**
2. **Pousser ce repo sur GitHub** (privé recommandé). Les routines remote en ont besoin.
3. **Dans Claude Desktop** → `Routines` → `Cloud environments` → crée un env nommé `trading` avec accès réseau total et les variables suivantes :
   ```
   ALPACA_API_KEY=...
   ALPACA_SECRET_KEY=...
   ALPACA_BASE_URL=https://paper-api.alpaca.markets
   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_CHAT_ID=...
   TRADING_MODE=paper
   ```
4. **Crée les 5 routines** décrites dans `routines/` (copier-coller les cron + prompt). Pour chaque routine, dans les permissions, active **Allow unrestricted branch pushes** pour que Bull puisse commit sur `main`.
5. **Lance un "Run now"** sur la routine `weekly-review` pour valider le bout-en-bout.

## Architecture

```
thashi-ai/
├── CLAUDE.md                 # Instructions globales (personnalité + règles de fer)
├── memory/                   # Mémoire persistante (commit à chaque run)
│   ├── guardrails.md         # Règles inviolables
│   ├── strategy.md           # Stratégie de trading
│   ├── portfolio.md          # Snapshot du portefeuille (maj après chaque trade)
│   ├── trade_log.md          # Journal chronologique des trades
│   ├── research_log.md       # Journal de recherche
│   ├── weekly_review.md      # Reviews hebdomadaires
│   └── learnings.md          # Leçons, incidents, ajustements
├── scripts/                  # Clients API (stdlib Python, zéro dépendance)
│   ├── alpaca_client.py
│   ├── telegram_client.py
│   └── portfolio_snapshot.py
├── .claude/
│   ├── commands/             # Slash commands appelés par les routines
│   └── skills/               # Skills custom (research, trade, journal)
└── routines/                 # Cron + prompts à coller dans Claude Desktop
```

## Routines (timezone America/Chicago, comme dans la vidéo)

| Routine          | Cron            | Rôle                                                |
|------------------|-----------------|-----------------------------------------------------|
| `pre-market`     | `0 6 * * 1-5`   | Recherche catalyseurs, prépare les idées de trade   |
| `market-open`    | `30 8 * * 1-5`  | Exécute les trades planifiés, pose trailing stops   |
| `midday`         | `0 12 * * 1-5`  | Coupe les perdants -7%, resserre les stops gagnants |
| `market-close`   | `0 15 * * 1-5`  | Snapshot portefeuille, notification Telegram        |
| `weekly-review`  | `0 16 * * 5`    | Review de la semaine, mise à jour stratégie         |

Si tu es dans un autre fuseau, adapte les heures ou configure le TZ dans l'environnement de la routine.

## Test en local

```bash
# Active tes clés dans un fichier .env local (non versionné)
cp .env.example .env
# Remplis .env, puis :
set -a && source .env && set +a
python scripts/alpaca_client.py account       # vérifie Alpaca
python scripts/telegram_client.py ping        # envoie un message "ping" sur Telegram
python scripts/portfolio_snapshot.py          # affiche portefeuille vs SPY
```

## Garde-fous

Lis `memory/guardrails.md`. Les règles par défaut : max 5% par position, pas d'options/crypto/short, daily loss cap -2%, max 3 nouvelles positions par semaine. Ajuste à ton profil avant de lancer en live.

## Disclaimer

Ce projet est une **expérimentation**. Aucun conseil financier. Commence et reste en paper trading jusqu'à ce que tu aies observé plusieurs semaines de comportement cohérent.
