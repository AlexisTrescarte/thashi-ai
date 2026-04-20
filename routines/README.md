# routines/

This folder contains **the 5 routines to create manually in Claude Desktop**. Each file describes:
- the `cron` to paste
- the full `prompt` to paste
- the Cloud environment and the repo to select

## Procedure (one-time)

1. **Push this repo to GitHub** (private recommended).
   ```bash
   gh repo create thashi-ai --private --source=. --remote=origin --push
   ```
2. **Claude Desktop → Routines → Cloud environments → Add**
   - Name: `trading`
   - Network access: **Full** (or allowlist: `paper-api.alpaca.markets`, `data.alpaca.markets`, `api.telegram.org`, `github.com`, `api.github.com`)
   - Variables:
     - `ALPACA_API_KEY`
     - `ALPACA_SECRET_KEY`
     - `ALPACA_BASE_URL` = `https://paper-api.alpaca.markets`
     - `TELEGRAM_BOT_TOKEN`
     - `TELEGRAM_CHAT_ID`
     - `TRADING_MODE` = `paper`
3. **For each of the 5 routines** (pre-market, market-open, midday, market-close, weekly-review):
   - New Routine → **Remote**
   - Repo: `<your-user>/thashi-ai` (branch `main`)
   - Cloud environment: `trading`
   - Model: **Claude Opus 4.7** (or 4.6 if 4.7 isn't available in your plan)
   - Cron: copy from the matching `.md` file
   - Prompt: copy **the entire prompt block** from the matching `.md` file
   - Permissions → **Allow unrestricted branch pushes**: enable (required for Bull to commit `memory/` to `main`)
4. For each routine, **Run now** at least once to validate before letting the cron run.

## Timezone

Crons are expressed in `America/Chicago`. If Claude Desktop forces another timezone, adapt:
- 06:00 CT = 11:00 UTC (DST) / 12:00 UTC (standard)
- 08:30 CT = 13:30 UTC / 14:30 UTC
- 12:00 CT = 17:00 UTC / 18:00 UTC
- 15:00 CT = 20:00 UTC / 21:00 UTC
- 16:00 CT = 21:00 UTC / 22:00 UTC

## Recommended test order

1. **market-close** first (pure snapshot, no trade) → validates the Alpaca + Telegram + git push chain.
2. **weekly-review** → validates review logic and alpha calculations.
3. **pre-market** → validates research + research_log append.
4. **market-open** → validates real execution (will place a paper order! confirm you're on `paper-api`).
5. **midday** → validates cut/tighten (needs an open position to observe anything).
