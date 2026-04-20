# routines/

This folder contains the **14 routines** (10 equities + 4 crypto) to create manually in Claude Desktop. Each file describes:
- the `cron` to paste
- the full `prompt` to paste
- the Cloud environment and repo to select

## Architecture

Bull is split into **two agents**:

| Agent | Timezone | Cadence | Instruments |
|---|---|---|---|
| **Bull-Equities** | America/Chicago | 8 routines, Mon-Fri | US equities, ETFs, leveraged ETFs, long options |
| **Bull-Crypto** | UTC | 4 routines, 24/7 + weekly + monthly | BTC, ETH, SOL, LINK, AVAX, DOT, MATIC (spot only) |

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
3. **For each of the 14 routines**:
   - New Routine → **Remote**
   - Repo: `<your-user>/thashi-ai` (branch `main`)
   - Cloud environment: `trading`
   - Model: **Claude Opus 4.7**
   - Cron: copy from the matching `.md` file
   - Prompt: copy **the entire prompt block** from the matching `.md` file
   - Permissions → **Allow unrestricted branch pushes**: enable (required to commit `memory/` to `main`)
4. For each routine, **Run now** once to validate before letting the cron run.

## The 14 routines

### Bull-Equities (America/Chicago, Mon-Fri unless noted)

| File | Cron (America/Chicago) | Purpose |
|---|---|---|
| `pre-market.md` | `0 6 * * 1-5` | 06:00 — macro + CTQS scan + daily plan |
| `market-open.md` | `30 8 * * 1-5` | 08:30 — dispatch BUY queue |
| `intraday-scan-1030.md` | `30 10 * * 1-5` | 10:30 — active mgmt + opportunistic BUY |
| `intraday-scan-1230.md` | `30 12 * * 1-5` | 12:30 — active mgmt + opportunistic BUY |
| `intraday-scan-1430.md` | `30 14 * * 1-5` | 14:30 — last-call exits (no new opens) |
| `market-close.md` | `0 15 * * 1-5` | 15:00 — EOD snapshot + alpha |
| `daily-review.md` | `30 15 * * 1-5` | 15:30 — grade the day |
| `weekly-review.md` | `0 16 * * 5` | Fri 16:00 — institutional week audit |
| `monthly-deep-review.md` | `0 17 L * *` | Last day of month 17:00 — Sharpe/Sortino + evolve |
| `quarterly-rewrite.md` | `0 18 L 3,6,9,12 *` | End-of-quarter 18:00 — strategy rewrite |

> Note: `L` (last day of month) cron syntax varies by scheduler. If `L` unsupported, use date-matching logic in the prompt to skip days that aren't month-end.

### Bull-Crypto (UTC, 24/7)

| File | Cron (UTC) | Purpose |
|---|---|---|
| `crypto-hourly.md` | `0 * * * *` | Every hour — regime + manage + opportunistic BUY |
| `crypto-daily-review.md` | `0 23 * * *` | 23:00 UTC — day vs BTC, stops discipline |
| `crypto-weekly-review.md` | `0 23 * * 0` | Sunday 23:00 UTC — 7d audit |
| `crypto-monthly-review.md` | `0 23 L * *` | Last day 23:00 UTC — Sharpe/Sortino vs BTC + evolve |

## Timezone reference (CT ↔ UTC)

- 06:00 CT = 11:00 UTC (DST) / 12:00 UTC (standard)
- 08:30 CT = 13:30 UTC / 14:30 UTC
- 10:30 CT = 15:30 UTC / 16:30 UTC
- 12:30 CT = 17:30 UTC / 18:30 UTC
- 14:30 CT = 19:30 UTC / 20:30 UTC
- 15:00 CT = 20:00 UTC / 21:00 UTC
- 15:30 CT = 20:30 UTC / 21:30 UTC
- 16:00 CT = 21:00 UTC / 22:00 UTC
- 17:00 CT = 22:00 UTC / 23:00 UTC
- 18:00 CT = 23:00 UTC / 00:00 UTC next day

If Claude Desktop forces UTC for cron, use the UTC column; the prompts themselves reference CT for human-readable logs.

## Recommended test order

1. **market-close** (pure snapshot, no trade) → validates the Alpaca + Telegram + git push chain
2. **daily-review** → validates the `review` skill + metrics.py + grading
3. **weekly-review** → validates alpha math + risk audit
4. **pre-market** → validates research + CTQS scan + journal
5. **market-open** → validates real execution (places a paper order — confirm `paper-api`)
6. **intraday-scan-1230** → validates dynamic stop mgmt with an open position
7. **crypto-hourly** → validates crypto endpoints + universe enforcement
8. **crypto-daily-review** → validates the crypto review path
9. **monthly-deep-review** → validates the `evolve` skill on a mock proposal (check `memory/prompt_evolution_proposals.md` seeding)
10. **quarterly-rewrite** → validates the full strategy-update flow (dry-run first)

## Operational notes

- **One agent per run**: an equities routine never writes to `memory/crypto/` and vice-versa (enforced by the `journal` skill).
- **Commit discipline**: every run pushes. If two runs overlap (e.g. crypto-hourly at the same clock slot as an equities routine), both will try to push; one may have to rebase. Accept that rebase at the start of the routine (`git pull --rebase origin main`) before any write.
- **Auto-defense state** is shared across agents via `memory/learnings.md`. If equities triggers drawdown auto-defense, the crypto agent reads the flag but only acts on its own per-agent drawdown.
- **Network errors**: routines log `[API-DEGRADED]` to `learnings.md` + notify Telegram, then terminate (no retry-storm).
