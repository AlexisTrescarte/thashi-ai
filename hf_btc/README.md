# Bull-HF-BTC — high-frequency BTC trading agent (sim-only)

Sister project of Bull-equities. Runs a 5-minute decision loop on **BTC/USD only**, **simulation-only** (`$3000` paper portfolio, no Alpaca order execution). Long + short virtual positions. Multiple trades per day expected.

> **Distinct from Bull-equities** — own CLAUDE.md, own state, own Telegram header (`*🐂 BullHF-BTC*`). Same chat ID, no API keys.

## What runs each tick (5 min)

1. **`harness.py prepare`** — pulls Alpaca crypto OHLCV (1m/5m/15m/1h × 200 bars), computes 8 indicators (RSI, MACD, Bollinger, ATR, EMA20/50/200, VWAP, Volume z-score), gates a chart-img fetch (50/day quota), builds `/tmp/hf_prompt.md` + `/tmp/hf_context.json`.
2. **`claude -p` non-interactive** — Claude Sonnet 4.6 receives the prompt, calls `WebSearch` once for BTC news, optionally `Read`s the chart, emits a strict JSON decision (`OPEN_LONG/OPEN_SHORT/CLOSE/HOLD/SKIP` + entry/TP/SL/sizing/confidence/reason_fr).
3. **`harness.py post`** — parses JSON, validates against guardrails, executes in `sim_portfolio` (with 0.05% slippage), checks any TP/SL hit on open trades since last tick, marks-to-market, sends Telegram (anti-spam: trade events always; heartbeat once/h; daily report at 23:55 UTC), commits + pushes if material change.
4. **`harness.py sleep_until_next`** — sleeps to next 5-min UTC boundary.

## Quick start (Mac)

```bash
# 1. Ensure .env is filled (parent repo .env is shared)
cat ../.env | grep -E '^(ALPACA|TELEGRAM|CHART_IMG)'

# 2. Smoke-test components in isolation
python scripts/btc_data.py snapshot
python scripts/chart_img_client.py quota
python scripts/sim_portfolio.py snapshot

# 3. Dry-run (no Claude, fake SKIP decision)
python scripts/harness.py tick_dry

# 4. Live loop (foreground)
./run_loop.sh

# 5. Live loop (background with log)
./run_loop.sh > /tmp/bull-hf-btc.log 2>&1 &
tail -f /tmp/bull-hf-btc.log
```

## VPS deployment (systemd)

```bash
sudo cp bull-hf-btc.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now bull-hf-btc
sudo journalctl -u bull-hf-btc -f
```

The service expects:
- `/opt/thashi-ai/hf_btc/` checkout
- `/opt/thashi-ai/.env` with secrets
- User `bull` + group `bull` with read access to the repo
- `claude` CLI on PATH (`/usr/local/bin/claude` by default)

## State files (`state/`)

| File | Purpose |
|---|---|
| `sim_portfolio.json` | $3000 sim equity, P&L, max DD, win/loss, equity curve |
| `open_trades.json` | Currently open trade(s) — max 1 |
| `trade_log.jsonl` | Append-only history of opens + closes |
| `chart_img_quota.json` | Daily quota tracker (resets 00:00 UTC) — 24 baseline + 24 opportunistic |
| `last_notif.json` | Anti-spam (last event ts, last heartbeat hour, last daily report date) |
| `runs.jsonl` | Per-tick log (prepare + post phases) |
| `charts/` | PNG chart images (gitignored) |

## Modes (`HF_TEST_MODE` env var)

| Gate | PROD (`0` or unset) | TEST (`1`) |
|---|---|---|
| Confidence floor (hard) | 50 | 40 |
| Cooldown same direction | 15 min | 5 min |
| Confluence target | ≥4/7 | ≥3/7 |
| Sizing 40-49 | SKIP | 2% probe-test |
| Sizing 50-59 | SKIP | 3% probe-test |
| Sizing 60-69 | 2-3% probe | 4% probe |

TEST = collect data (more trades, lower-conviction allowed). PROD = standard selectivity.

## Guardrails (NEVER softened, even in TEST)

- Sizing 2-12% per trade
- R/R ≥ 1.8
- Daily loss cap -3% sim → freeze new opens
- Max 1 open position
- Spread > 0.15% → SKIP forced

## Cost expectations

~288 ticks/day × ~10-15k token Sonnet 4.6 input + ~2k output ≈ **$7-12/day** API cost. WebSearch tool calls included.

Chart-img: 48/50 daily limit budget — 24 baseline (1/h) + 24 opportunistic (gated on signal_score ≥ 2).

## Notes

- **No Alpaca order execution.** Alpaca is data-only here. Sim portfolio is the only book.
- **Stateless between ticks** — full continuity flows through `state/` files.
- **Crash recovery** — `Restart=on-failure` on systemd; bash loop continues on partial failures (logs degraded ticks).
- **Time alignment** — every tick aligns to a 5-min UTC boundary. If a tick takes > 5 min (e.g. claude slow), the next one fires immediately to catch up.
