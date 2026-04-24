---
name: trade
description: Execute BUY / TRIM / CUT / TIGHTEN / STOP-UPDATE / ADD on Alpaca (equities, options, crypto majors) with confidence-based sizing, dynamic stop management, and guardrail gates. Invoke from market-open, intraday-scan, market-close (last-call only).
---

# Skill: trade

Execute an order on Alpaca or adjust a live position. Assumes a valid research note exists (for BUY) or a rule triggers (for CUT / TRIM / TIGHTEN / STOP-UPDATE / time-stop / earnings-eve / thesis-broken).

> No strategic decision here. Strategic decisions live in research notes + commands. This skill is the **execution layer** with guardrail enforcement.

## Preconditions (check before any action)

1. Market open for equities (`alpaca_client.py clock`). Crypto orders are placed inside the same US-hours window — we do not trade crypto outside equities session.
2. API keys present + `TRADING_MODE` consistent with `ALPACA_BASE_URL`
3. **Auto-defense not active** (no `[DRAWDOWN-AUTO-DEFENSE]` in last 14 days in `learnings.md`, or its conditions lifted)
4. **No active daily/weekly loss cap** blocking opens
5. **Confirmed risk-off regime** not freezing opens

## BUY (new position)

### Equities / ETFs

1. Fetch `account` → `equity`, `cash`, `buying_power`, `last_equity`
2. Fetch `quote {TICKER}` → ask, spread. Verify spread ≤ 0.5%
3. Verify ask ≤ plan price + 2% (else skip, log "FOMO guard")
4. **Confidence-based sizing** (from research note CTQS score + self-rated confidence):
   - High (≥85): target 7-10%, cap 10%
   - Standard (70-84): target 4-6%, cap 6%
   - Probe (55-69): target 2-3%, cap 3%
   - Technical-only: capped at Standard (max 6%)
   - If major macro event within 24h: one notch down
5. `qty = floor((target_pct × equity) / ask)`
6. **Gates** (all must pass):
   - Cash post-trade ≥ 10% × equity
   - New positions today < 10, this week < 30
   - Total positions < 30
   - Target sector after buy ≤ 25% portfolio
   - Position cap ≤ 10% NAV
   - Leveraged-ETF aggregate (if applicable) ≤ 15% post-trade
   - Not a revenge trade (not cut in last 5 days with P&L < 0 unless "re-entry justified" + CTQS ≥ 70)
   - If equity ticker: ticker's earnings outside horizon window unless explicit "earnings hold" in research
7. Execute: `python scripts/alpaca_client.py buy {TICKER} {QTY}` (market, day)
8. On fill, **immediately** place stop per the stop-type in the research plan:
   - % trailing: `trailing-stop {TICKER} {QTY} {pct}`
   - Stop-market: `scripts/alpaca_client.py stop {TICKER} {QTY} {level}` (extend client if needed)
   - Manual-trailing (if Alpaca doesn't support for this symbol): schedule update at next intraday-scan, log in trade note
9. **Log** trade to `memory/equities/trade_log.md` with full schema

### Long options

1. Fetch underlying quote, option chain via `options_client.py quote {UNDERLYING} {EXPIRY} {STRIKE} {C|P}`
2. Verify DTE 7-60, OI > 500, bid/ask spread ≤ 10% of mid
3. **Sizing** (premium cost, not notional):
   - `target_pct` per CTQS, but options aggregate ≤ 5% NAV hard cap
   - `contracts = floor((target_pct × equity) / (mid × 100))`
4. **Gates**: options aggregate ≤ 5% post-trade, underlying must be ADV > 5M shares
5. Execute via `options_client.py buy {SYMBOL} {CONTRACTS}` (market or limit based on spread)
6. **No stop** on options by default — use price-target AND time-stop at DTE-3:
   - Hard price stop: -50% of premium → cut
   - Hard time stop: DTE-3 → cut regardless

### Crypto (BTC / ETH / SOL only)

1. Verify symbol ∈ {BTC/USD, ETH/USD, SOL/USD}. Any other symbol → automatic skip with reason `crypto alt outside approved list`.
2. Fetch `alpaca_crypto_client.py quote {SYMBOL}` → bid/ask
3. Verify spread ≤ 1% (crypto liquidity)
4. **Sizing** confidence-based, capped:
   - Single-coin cap 10% NAV (same as equities per-position cap)
   - Aggregate crypto cap 15% NAV (sum across BTC + ETH + SOL)
5. `qty = (target_pct × equity) / ask` (fractional allowed)
6. **Native trailing stop required**: verify Alpaca supports trailing-stop for this crypto symbol before ordering. If not supported → skip (no manual-trailing fallback: the agent is asleep outside US hours and cannot cover overnight / weekend gaps).
7. Execute: `alpaca_crypto_client.py buy {SYMBOL} {QTY}`
8. Immediately: `alpaca_crypto_client.py trailing-stop {SYMBOL} {QTY} {pct}` — default 5% BTC, 7% ETH/SOL (override per research note)
9. Log to `memory/equities/trade_log.md` with `instrument=crypto`, `symbol={SYMBOL}`

## CUT (exit full position)

Triggers:
- Thesis broken (guidance cut, fraud, halt, FDA reject, contract loss, C-suite resign, crypto exploit / rug / SEC action / chain halt)
- Stop hit (if manual-trailing)
- Time stop exceeded
- Pre-earnings exit (no "earnings hold")
- Regime shift forcing defensive
- Take-profit target hit

Steps:
1. Cancel active stops for the symbol (`orders --status open` → cancel)
2. `close {SYMBOL}` (equities/crypto) or `options_client.py close {OPTION}` (options)
3. Log with explicit reason:
   - `cut thesis-broken: {reason}`
   - `cut stop-hit: {level}`
   - `cut time-stop: J+{N}`
   - `cut pre-earnings`
   - `cut regime-shift: {description}`
   - `cut take-profit: +{X}%`
4. If thesis broken before stop: also note in `learnings.md` (reason + what could've been seen earlier)

## TRIM (partial exit on a winner)

1. Per plan: 33%, 50%, or 66% of qty
2. Execute `sell {SYMBOL} {qty_trim}` (market, day)
3. Cancel current stop, place tighter stop on remaining qty (typically 3% trailing or structural tightened)
4. Log reason `trim X% at +Y%` (include the CTQS context if refreshed)

## TIGHTEN (stop adjustment, one-way ratchet)

1. List open stops for symbol, cancel
2. Place new tighter stop (%, ATR, or structural)
3. **One-way ratchet**: new stop must be tighter than previous (closer to current price on a long). Never loosen.
4. Log `STOP-UPDATE` entry with old and new level + reason

## STOP-UPDATE (dynamic TP/SL management — called at every intraday-scan)

For each open position:
- If price advanced ≥ X% since last stop update, consider tightening (per stop-update policy in research note)
- If macro event / earnings approaches, tighten ahead
- If a key technical level broken in our favor, move stop below new support
- If IV spike for options position: consider TRIM or CUT

Always log `STOP-UPDATE` entries (schema in `trade_log.md`).

## ADD (top-up on existing position — restricted)

Allowed only if ALL of:
- Original position < 50% of max cap for its conviction
- New distinct dated catalyst (different from original)
- Post-ADD position ≤ 10% NAV absolute hard cap
- Post-ADD position ≤ conviction tier cap

Steps:
1. Refresh CTQS in a new research note (mini, explicit "ADD justification")
2. Execute like a BUY but log as ADD with reference to original entry

## EARNINGS-EVE EXIT (equities, positions with earnings J+1)

1. If research note doesn't explicitly say "earnings hold": exit by default
2. `close {TICKER}` on eve-close (intraday-scan 14:30 or market-close 15:00)
3. Log reason `cut pre-earnings — no earnings hold`

## Failures

- Order rejected: log raw API response in `learnings.md`, notify Telegram `DEGRADED`
- Quote fails: retry 1× after 5s; if still failing, skip, log
- Spread > threshold: skip, log `liquidity anomaly`
- FOMO guard (ask > plan + 2%): skip BUY, do not re-enter higher same day

## Forbidden anti-patterns

- BUY without immediate stop (manual-trailing counts only if logged + update scheduled)
- Loosen a stop once placed (one-way ratchet violation)
- Override confidence sizing "because I feel strongly" — bounded by CTQS mapping
- CUT "out of caution" before a real trigger (let stops do their job)
- Hold through earnings without explicit "earnings hold"
- Re-enter a ticker cut < 5 days ago without explicit new thesis + CTQS ≥ 70
- ADD beyond per-position 10% hard cap
- Options: hold past DTE-3 or let decay beyond -50% premium
- Crypto: buy a symbol outside {BTC, ETH, SOL}
- Crypto: buy any symbol without native trailing stop support on Alpaca (overnight/weekend gap risk uncovered)
