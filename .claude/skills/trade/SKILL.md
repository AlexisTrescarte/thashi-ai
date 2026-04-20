---
name: trade
description: Execute BUY / TRIM / CUT / tighten-stop on Alpaca with conviction-based sizing and guardrail checks (catalyst-driven short-swing regime, 1-5 day horizon). Invoke from market-open and midday.
---

# Skill: trade

Place an order on Alpaca while respecting `memory/guardrails.md`. No strategic decision here — assumes a valid research note (BUY verdict) exists, or a midday rule triggers the action.

## Preconditions (check before order)

1. Market open (`alpaca_client.py clock`).
2. Keys present.
3. `TRADING_MODE` consistent with `ALPACA_BASE_URL`.
4. No daily loss cap hit yesterday, no weekly loss cap active, no drawdown cap.
5. No confirmed risk-off regime freezing opens (check `portfolio.md`).
6. **No ADD on short-swing**: top-up operation is forbidden by strategy — ignore any such request.

## BUY (new position)

1. Fetch `account` → `equity`, `cash`, `last_equity`.
2. Fetch `quote {TICKER}` → current ask, verify spread ≤ 0.5%.
3. Verify ask price ≤ pre-market plan price + 2% (else skip and log "FOMO guard").
4. **Conviction-based sizing** (from research note):
   - Probe → `target_pct = 0.02`
   - Standard → `target_pct = 0.04`
   - High conviction → `target_pct = 0.05`
   - If a major macro event (FOMC/CPI/NFP) is within 24h: cap at Standard (4%).
5. `qty = floor((target_pct * equity) / ask)`.
6. **Gates**:
   - cash post-trade ≥ 10% × equity
   - new positions today < 5, this week < 15
   - total positions < 20
   - target sector after buy ≤ 35% portfolio
   - no more than 5 positions exposed to same single event (catalyst concentration)
   - ticker in universe (volume > 2M, price ≥ $5, mcap ≥ $2B unless documented exception)
   - not a revenge trade (cut in last 5 days without "re-entry justified" in research)
   - ticker's earnings **outside** expected exit window (J+0 to J+8) unless explicit "earnings hold"
7. Execute: `python scripts/alpaca_client.py buy {TICKER} {QTY}` (market, day).
8. If `status=filled` or `accepted`: **immediately** place `trailing-stop {TICKER} {QTY} 6` (default 6% for short horizon).
9. **Log** in `trade_log.md`:
   ```
   ### 2026-04-20T13:30:00Z — BUY NVDA 15@$912.34
   - Order ID: xxx
   - Value: $13,685.10
   - % portfolio: 4.8%
   - Conviction: High (quality score 27/30)
   - Setup type: Pre-earnings momentum
   - Catalyst: earnings 2026-04-22 AMC (J+2) — exit planned eve-close unless clear runner
   - Thesis: (1 line from research_log)
   - Trailing stop: 6% (order ID yyy)
   - Time stop: 2026-04-30 (J+8)
   - Routine: market-open
   - Research: 2026-04-20T11:05:00Z
   ```

## CUT (loss ≤ -5% OR thesis broken OR time stop exceeded OR pre-earnings exit)

1. `close {TICKER}` — closes position at market.
2. Cancel active stops (`orders --status open` + cancel ticker's).
3. Log `trade_log.md` with reason (`cut -5%` / `thesis broken: reason` / `time stop J+8` / `pre-earnings exit eve`).
4. If thesis broken before stop: note in `learnings.md` (reason + what we could have seen earlier).

## TRIM (winner ≥ +15%)

1. `qty_trim = floor(current_qty * 0.5)` (default trim 50%).
2. If position > +25%, may trim 33% (let winners run) if clear runner.
3. `sell {TICKER} {qty_trim}` (market, day).
4. Cancel current trailing stop, place trailing 3% on `current_qty - qty_trim`.
5. Log reason `trim 50% +X%` or `trim 33% runner`.

## TIGHTEN (winner ≥ +10%)

1. List open stops for ticker, cancel them.
2. Place new trailing stop 3% on full qty.
3. Mark position `tightened` in `portfolio.md`.
4. Log reason `tighten +X%`.

## EARNINGS-EVE EXIT (position with earnings J+1)

1. If research note does not explicitly say "earnings hold": exit by default.
2. `close {TICKER}` on eve-close (triggered by midday if J+1 = earnings day, or market-close if time is short).
3. Log reason `pre-earnings exit — no earnings hold in thesis`.

## Failures

- Order rejected (insufficient buying power, PDT flag, asset halted, wash trade): log `learnings.md` with raw API response, notify Telegram `DEGRADED`.
- Quote fails: retry 1x after 5s; if still failing, skip trade, log, continue.
- Spread > 0.5%: skip, log in `learnings.md` (liquidity anomaly).
- Price > +2% vs morning plan: skip BUY (FOMO guard), log. Do not re-enter higher later in the day.

## Forbidden anti-patterns

- BUY without immediate trailing stop.
- Override conviction sizing "because the thesis is strong" — sizing comes from the note.
- CUT "out of caution" at -3%. Respect -5% unless thesis objectively broken.
- Hold through earnings without explicit "earnings hold" in research note.
- Re-enter a ticker cut in the last 5 days without explicit new thesis.
- ADD / top-up an existing position (forbidden on short-swing).
- Intraday scalping (no sell same day as buy unless stop hit or thesis abruptly broken).
