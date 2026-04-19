# scripts/

Clients API Python **stdlib uniquement** (zéro dépendance, zéro `pip install` nécessaire).

## Utilisation (local)

```bash
# Charger les variables d'environnement depuis .env
set -a && source .env && set +a

# Alpaca
python scripts/alpaca_client.py account
python scripts/alpaca_client.py clock
python scripts/alpaca_client.py positions
python scripts/alpaca_client.py orders --status open
python scripts/alpaca_client.py quote SPY
python scripts/alpaca_client.py buy AAPL 10
python scripts/alpaca_client.py trailing-stop AAPL 10 10  # 10% trail
python scripts/alpaca_client.py close AAPL

# Telegram
python scripts/telegram_client.py ping
python scripts/telegram_client.py send "Hello *world*"
python scripts/telegram_client.py updates   # voir les messages reçus (pour trouver le chat_id)

# Snapshot portefeuille vs SPY
python scripts/portfolio_snapshot.py
```

## Utilisation depuis Bull (dans une routine)

Bull appelle ces scripts via l'outil `Bash`. Les clés API viennent des variables
d'environnement configurées dans l'environnement Cloud de la routine (Claude Desktop →
Routines → Cloud environments → `trading`), pas d'un `.env`.

## Ajout d'un endpoint

Si tu as besoin d'un endpoint Alpaca pas encore wrappé (ex: portfolio history, assets
listing), ajoute une fonction dans `alpaca_client.py` qui appelle `_trading()` ou
`_data()`, puis expose-la en CLI dans `main()`. Pas de dépendance tierce.
