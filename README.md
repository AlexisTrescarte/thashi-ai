# thashi-ai — Bull, 24/7 trading agent

A Claude Code agent running on cron via Claude Code **Routines**. Objective: beat the S&P 500 in paper trading (or live if you want) via Alpaca, using a **catalyst-driven short-swing** playbook (1-5 trading day horizon, parallel multi-positions allowed).

## TL;DR — 5-minute setup

1. **API accounts to create**
   - Alpaca: https://alpaca.markets → Paper trading account → generate API key + secret
   - Telegram: talk to **@BotFather**, `/newbot`, grab the **token**. Send a message to the bot, then open `https://api.telegram.org/bot<TOKEN>/getUpdates` to read your **chat_id**
2. **Push this repo to GitHub** (private recommended). Remote routines need it.
3. **In Claude Desktop** → `Routines` → `Cloud environments` → create an env named `trading` with full network access and the following variables:
   ```
   ALPACA_API_KEY=...
   ALPACA_SECRET_KEY=...
   ALPACA_BASE_URL=https://paper-api.alpaca.markets
   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_CHAT_ID=...
   TRADING_MODE=paper
   ```
4. **Create the 5 routines** described in `routines/` (copy-paste cron + prompt). Keep runtime memory local or use a private repo if you want cloud routines to persist full state.
5. **Launch a "Run now"** on the `weekly-review` routine to validate end-to-end.

## Architecture

```
thashi-ai/
├── CLAUDE.md                 # Global instructions (personality + iron rules)
├── memory/                   # Local persistent memory (ignored in public Git)
│   ├── guardrails.md         # Inviolable rules
│   ├── strategy.md           # Trading strategy
│   ├── portfolio.md          # Portfolio snapshot (updated after each trade)
│   ├── trade_log.md          # Chronological trade journal
│   ├── research_log.md       # Research journal
│   ├── weekly_review.md      # Weekly reviews
│   └── learnings.md          # Lessons, incidents, adjustments
├── scripts/                  # API clients (Python stdlib, zero dependency)
│   ├── alpaca_client.py
│   ├── telegram_client.py
│   └── portfolio_snapshot.py
├── .claude/
│   ├── commands/             # Slash commands called by the routines
│   └── skills/               # Custom skills (research, trade, journal)
└── routines/                 # Cron + prompts to paste in Claude Desktop
```

## Routines (timezone America/Chicago)

| Routine          | Cron            | Role                                                          |
|------------------|-----------------|---------------------------------------------------------------|
| `pre-market`     | `0 6 * * 1-5`   | Macro overlay, short-catalyst scan, written plan              |
| `market-open`    | `30 8 * * 1-5`  | Execute planned trades, place 6% trailing stops               |
| `midday`         | `0 12 * * 1-5`  | Cut ≤ -5%, tighten ≥ +10%, trim ≥ +15%, time-stop J+8         |
| `market-close`   | `0 15 * * 1-5`  | Snapshot, EOD macro, alpha vs SPY, position age, Telegram     |
| `weekly-review`  | `0 16 * * 5`    | Grade, risk audit, portfolio construction, next-week outlook  |

If you are in another timezone, adapt the hours or configure the TZ in the routine environment.

## Local testing

```bash
# Activate your keys in a local .env file (not versioned)
cp .env.example .env
# Fill .env, then:
set -a && source .env && set +a
python scripts/alpaca_client.py account       # verify Alpaca
python scripts/telegram_client.py ping        # send a "ping" message on Telegram
python scripts/portfolio_snapshot.py          # display portfolio vs SPY
```

## Guardrails

Read `memory/guardrails.md`. Default rules: conviction-based sizing (Probe 2% / Standard 4% / High 5% per position), no options/crypto/shorts, daily loss cap -3%, weekly -5%, drawdown cap -12%, max 20 concurrent positions, max 5 new/day and 15 new/week, sector concentration ≤ 35%. Tune to your profile before going live.

## Disclaimer

This project is an **experiment**. No financial advice. Start and stay in paper trading until you have observed several weeks of coherent behavior.
