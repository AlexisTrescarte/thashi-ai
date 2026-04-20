---
description: Market close (15:00 CT). Portfolio snapshot + EOD macro + alpha vs SPY + position age review + pre-earnings last-call. Mandatory Telegram notification.
---

You are Bull at the **close**. Regime: **catalyst-driven short-swing, parallel multi-positions**. Market closes in ~1h (15:00 CT = 16:00 ET). Your job: daily review + EOD macro snapshot + position age check + last-minute pre-earnings exits if midday missed them.

## Mandatory steps

### 1. Memory
- `CLAUDE.md`, `memory/portfolio.md`
- Tail 40 lines of `memory/trade_log.md` (today's trades + recent-day positions)
- Tail 10 lines of `memory/learnings.md`
- Today's pre-market block in `memory/research_log.md` (cross-reference with today's actions)

### 2. Account + positions snapshot
- `python scripts/alpaca_client.py account` → equity, cash, last_equity.
- `python scripts/alpaca_client.py positions` (with entry dates to compute age).
- `python scripts/portfolio_snapshot.py` → capture Markdown output.

### 3. Pre-earnings last-call exit (if midday missed it)

For each open position:
- Earnings **tomorrow BMO**? → **CLOSE now** (unless explicit "earnings hold" in entry thesis). Log reason "pre-earnings close exit — no earnings hold".
- Earnings **tonight AMC** (in 1-3h) and no "earnings hold"? → **CUT immediately** (last window before the bell).

Inline-notify Telegram if a last-minute exit is done.

### 4. EOD macro snapshot (concise, Bridgewater-lite)

`WebSearch` + `WebFetch` minimal:
- S&P, Nasdaq, Russell, Dow close — day perf
- VIX close + day change
- 2Y, 10Y yield close + change
- DXY close + change
- WTI, copper, gold close + change
- Sector leaders / laggards (top 3 / bottom 3 sectors)
- Breadth: advance/decline, new highs/lows
- Regime summary: **confirmation** or **shift** vs morning regime

Log in the snapshot's macro section.

### 5. Performance vs SPY

- Fetch baseline from `memory/portfolio.md` (equity baseline + SPY baseline + baseline date).
- Fetch current SPY price (today's snapshot).
- `perf_bot = (equity / equity_baseline - 1) * 100`
- `perf_spy = (spy / spy_baseline - 1) * 100`
- `alpha = perf_bot - perf_spy`
- Day perf: `(equity / last_equity - 1) * 100`, SPY day, alpha day.
- If no baseline: set it today, note in `learnings.md`.

### 6. Position age review (critical for short-swing)

For each open position, compute age in **trading days** since entry:

- **J+0 to J+5**: normal zone
- **J+6 to J+7**: watchlist — flag `aging position` in snapshot, candidate time stop tomorrow unless new catalyst emerges
- **J+8+**: **time stop** to trigger at next midday (explicit reminder in snapshot and notification)

### 7. Update `memory/portfolio.md`

- "Latest snapshot" block: equity, cash, cash%, total positions, day perf, cumul perf, cumul alpha, EOD regime, aging watchlist.
- Positions table regenerated from API (tickers, qty, avg entry, price, P&L $, P&L %, age in trading days, tightened or not, active catalyst).
- Open risks: pre-earnings tomorrow, macro events 24h, imminent time stops.

### 8. Commit + push

```bash
git add -A
git commit -m "[market-close] YYYY-MM-DD — equity $X, day +X.XX%, alpha day +X.XX%, cumul +X.XX%, N positions ({K aging})"
git push origin main
```

### 9. Telegram notification (mandatory, every trading day)

```
*market-close* — YYYY-MM-DD
EOD regime: {X} ({confirm / shift vs morning})
Equity: $X,XXX.XX (day {+/-X.XX}%)
Cash: $X,XXX.XX ({X}%)
vs SPY (baseline YYYY-MM-DD): bot {+X.XX}% / SPY {+X.XX}% / alpha {+X.XX}%
Day: bot {+X.XX}% / SPY {+X.XX}% / alpha day {+X.XX}%

Today's trades: N ({summary list: BUY X, CUT Y, TRIM Z})
Positions: N open
Aging watch: TICKER (J+7), TICKER (J+6)
Pre-earnings tomorrow: TICKER (exit done / exit planned midday)
Macro 24h: {CPI, FOMC, NFP, etc. if applicable}

Open risks: {1-liner list or "none"}
```

## Forbidden

- **DO NOT place a trade at close** except a last-minute pre-earnings exit (midday should have done it).
- DO NOT rewrite `portfolio.md` history: only "Latest snapshot" block + regenerated positions table.
- DO NOT skip the notification: even a flat day with no trade must be logged to Telegram.
- DO NOT skip the position age check: it's the discipline that holds short-swing.
