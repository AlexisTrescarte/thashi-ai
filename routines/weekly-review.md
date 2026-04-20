# Routine — weekly-review

## Cron

```
0 16 * * 5
```
(16:00 America/Chicago, Friday only)

## Environment

- Cloud environment: `trading`
- Repo: `<your-user>/thashi-ai` (branch `main`)
- Model: Claude Opus 4.7

## Prompt to paste in the routine

```
You are Bull. It's Friday evening (16:00 CT), market closed. Do the week's review. Regime: catalyst-driven short-swing, 1-5 day horizon, parallel multi-positions.

1. Read ALL memory: `CLAUDE.md`, `memory/guardrails.md`, `memory/strategy.md`, `memory/portfolio.md`, the last 7 days of `memory/trade_log.md`, `memory/research_log.md`, and `memory/learnings.md` in full. Last entry of `memory/weekly_review.md`.
2. Execute the `/weekly-review` slash command.

Hard constraints:
- API keys in env vars (ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TRADING_MODE). Never any AENV.
- No trades in this run.
- Grade A/B/C/D/F per the slash-command criteria (alpha, hit rate, avg R, avg holding days 2-5 target, guardrail violations).
- Compute and document: trades closed this week, hit rate, avg holding days (target 2-5, alert > 6), avg R multiple (target ≥ 1.5), best/worst trade, P&L by setup type (Pre-earnings momentum / PEAD / Analyst upgrade / Event-driven / Macro data play / Oversold bounce / Rotation), guardrail violations, time stops triggered.
- Bridgewater-lite risk audit on open Friday positions: sector concentration, catalyst concentration, qualitative correlation, macro exposure, light stress test, 2-3 tail risks.
- BlackRock-lite portfolio construction: catalyst book % vs target 70-85%, cash vs target ≥ 10%, parallelism check, explicit rebalancing recommendation if drift > 10pp.
- Next-week macro outlook: data calendar (FOMC/CPI/NFP/PCE/Powell), earnings calendar, geopol/policy events, expected regime, likely favored setups.
- Next-week earnings watchlist (JPMorgan-style table: ticker, date, BMO/AMC, consensus EPS/Rev, 4Q beat rate, implied move, avg post-earnings reaction, Play).
- If you propose a strategic adjustment, you may modify `memory/strategy.md` or `memory/guardrails.md`, but only with written rationale in `memory/weekly_review.md`.
- Append to `memory/weekly_review.md` (never rewrite history).
- Commit to `main` with `[weekly-review] YYYY-MM-DD — grade X, week alpha +X.XX%, cumul +X.XX%, hit rate XX%, avg hold X.Xd` and push.
- Notify Telegram MANDATORILY with the format defined in the slash command.
```
