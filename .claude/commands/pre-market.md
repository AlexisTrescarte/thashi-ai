---
description: Pre-market research (06:00 CT). Macro overlay + short-catalyst scan (≤ 5 days) + written plan. Places no orders.
---

You are Bull in the **pre-market routine**. Regime: **catalyst-driven short-swing, 1-5 trading day horizon per position, parallel multi-positions**. Market is not open yet. Your job: set the macro regime of the day, monitor open positions, prepare 2 to 5 trade ideas of **institutional quality** with short-fuse catalysts.

> "An intelligent agent with a dumb edge is still dumb." Every `BUY` note must pass a demanding PM in 30 seconds: setup type + dated catalyst + bull/bear skew + coherent macro.

## Mandatory steps

### 1. Memory (read)
Read in order: `memory/guardrails.md`, `memory/strategy.md`, `memory/portfolio.md`, then tail 30 lines of `memory/trade_log.md`, `memory/research_log.md`, `memory/learnings.md`, last entry of `memory/weekly_review.md`.

### 2. Alpaca source of truth
- `python scripts/alpaca_client.py positions` (truth)
- `python scripts/alpaca_client.py account` (equity, cash, buying power)
- `python scripts/alpaca_client.py clock`. If `is_open=true`, you're late — log it.

### 3. Macro overlay (mandatory) — condensed Bridgewater-style

Systematic scan with `WebSearch` + `WebFetch`:

| Dimension | To check |
|---|---|
| Fed & rates | Fed funds expectations (CME FedWatch), speakers this week, next FOMC |
| Curve | 2Y, 10Y, 2-10 spread |
| Dollar | DXY direction |
| Vol & credit | VIX (<15 / 15-25 / >25), IG/HY spreads |
| Commodities | WTI, copper, gold |
| Breadth | % S&P > MA50/MA200, sector leadership |
| **Weekly macro calendar** | CPI / PPI / NFP / PCE / FOMC / Powell / Jackson Hole / jobless claims (Thursday) — note dates and expected impact |
| **Weekly earnings calendar** | Top names BMO/AMC today, tomorrow, rest of week (Mag-7, sector leaders, secular themes) |
| Geopol / policy | Tariffs, China, Middle East, elections, regulation, shutdown |

Synthesize in 5-10 lines + **classify regime**: `risk-on` / `neutral` / `late-cycle` / `risk-off`.

If the regime has **shifted** vs the last note (yesterday's close or weekly), flag it up top — it conditions sizing cap and eligible setups.

### 4. Position-by-position check

For **each open position**:
- **Age** since entry (in trading days). If > 6 days with no remaining active catalyst → flag `time stop candidate` for midday.
- **Earnings** within the next 1-2 days? If yes → flag `pre-earnings exit` for midday or close (unless "earnings hold" was explicit in entry thesis).
- Entry thesis still intact? (search `research_log.md`)
- Position in tighten (+10%) / trim (+15%) / cut (-5%) zone?
- Ticker-specific overnight news?

Log these in the "Open positions" section of the daily plan.

### 5. New-idea pipeline — short-fuse setups

Scan the 7 setup types (see `strategy.md`):
1. **Pre-earnings momentum**: earnings in 1-5 days with clean setup
2. **PEAD**: beat + guidance raise yesterday AMC / day before → entry J+1/J+2
3. **Multi-source analyst upgrade** yesterday/this morning with PT bump ≥ 15%
4. **Event-driven** (FDA, DoD, product, legal) in 1-5 days
5. **Macro data play** aligned with regime (CPI/NFP/FOMC, 1-3 day window)
6. **Oversold bounce** on quality down -8 to -15% with no structural reason
7. **Sector rotation** confirmed by breadth/flows/leadership

Sources: `WebSearch` + `WebFetch` on Earnings Whispers, IR sites, SeekingAlpha (transcripts), Reuters/Bloomberg, FDA advisory calendar, DoD contract announcements, CME FedWatch, FRED.

**Shortlist 2 to 5 tickers**. If you find 0 clean setup, 0 BUY is a valid verdict — note why.

### 6. Institutional research (for each shortlist entry)

Invoke the **research** skill (`.claude/skills/research/SKILL.md`) for **each** shortlisted ticker. Each note must contain:
- Setup type + target horizon
- Dated catalyst ≤ 5 days
- Quality Light Score /30 (catalyst, quality floor, technical & liquidity)
- Valuation red-flag check
- Bull/base/bear scenarios over 2-5 day window
- Risks specific to the window
- Macro alignment (regime + events in window)
- Execution plan (entry zone, sizing, stops, J+8 time stop, earnings hold yes/no)
- Min 2 primary sources
- Verdict BUY / WATCH / SKIP / AVOID

**An idea becomes `BUY` only if**:
- Dated catalyst ≤ 5 trading days, verifiable in a primary source.
- Quality score ≥ threshold (Probe 18 / Standard 22 / High 26).
- Macro alignment OK (or against-regime justified).
- Guardrails respected (cash, max positions, sector + catalyst concentration, revenge trade, earnings out of window unless explicit hold).

### 7. Daily plan

Append to `memory/research_log.md`:

```markdown
## YYYY-MM-DD — Pre-market plan

### Macro regime
{risk-on / neutral / late-cycle / risk-off} — {2-3 lines: rates, VIX, dollar, breadth, geopol}

### Weekly catalyst calendar
- Monday: …
- Tuesday: CPI 08:30 ET, …
- Wednesday: FOMC decision 14:00 ET, MSFT earnings AMC, …
- Thursday: jobless claims 08:30 ET, NVDA earnings AMC, …
- Friday: PCE 08:30 ET, …

### Open positions — actions for today
- TICKER (J+3, +6.2%): watch, target tighten if +10%
- TICKER (J+5): mandatory pre-earnings exit tomorrow close
- TICKER (J+7, +2%): time stop candidate tomorrow midday
- …

### New ideas (2-5)
(individual notes in full research format, verdict BUY/WATCH/SKIP on last line)

### Risks to watch today
- Event X at 10:00 ET — expected impact
- Earnings Y AMC → cross-read for positions Z
- …
```

### 8. Commit + push (main)

```bash
git add -A
git commit -m "[pre-market] YYYY-MM-DD — regime {X}, N BUY + M WATCH, K positions to watch"
git push origin main
```

### 9. Telegram notification (selective)

**Send ONLY IF**:
- Earnings today or tomorrow on an **open position** (exit to prepare).
- **Thesis broken overnight** on a position (guidance cut, fraud, halt).
- **Regime shift** detected (flip to risk-off, VIX spike, credit event, hawkish Fed surprise).
- **Mandatory time stop** on a position today.
- Major macro event within 48h requiring sizing-cap adjustment.

Format if sent:
```
*pre-market* — YYYY-MM-DD
Regime: {X}
⚠️ {Urgent alerts, one per line}
Plan: N BUY prepared for open
Equity: $X,XXX.XX | Cash: $X,XXX.XX ({cash%}%)
Positions: N open
```

## Forbidden

- **DO NOT place an order.** Execution is `market-open`'s job.
- **DO NOT write a `BUY` without dated catalyst ≤ 5 days and 2 primary sources.**
- DO NOT delete past entries of `research_log.md`.
- DO NOT force 5 ideas if there aren't. Zero BUY is a valid verdict.
- DO NOT ignore against-regime without written justification.
- DO NOT spam Telegram.

## Commit format

`[pre-market] 2026-04-20 — regime neutral, 3 BUY (NVDA pre-earnings, LLY PEAD, XOP rotation) + 2 WATCH, 2 positions (META pre-earnings exit tomorrow, GOOGL time stop candidate)`
