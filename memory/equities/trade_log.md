# Trade log — Equities

Append-only. **Never rewrite** a past entry. Reverse chronological (most recent on top).

## Schema

```
### YYYY-MM-DDTHH:MM:SSZ — {BUY|SELL|TRIM|CUT|ADD|TIGHTEN|STOP-UPDATE} {SYMBOL} {qty}@{price}
- Order ID: {id}
- Value: ${value}
- % NAV at entry: {n}%
- Instrument: {equity | ETF | leveraged-ETF | option}
- Style: {day | short-swing | swing | positional}
- CTQS: C{xx}/T{xx}/Q{xx}/S{xx} = {total}/100 → Conviction {Probe|Standard|High}, confidence {xx}%
- Setup type: {setup}
- Catalyst: {event + date} OR "technical-only"
- Thesis: {1-3 lines}
- Stop: {type + level}
- Take-profit: {level or "trailing only"}
- Time stop: {date or "n/a"}
- Earnings hold: {yes/no}
- Routine: {routine name}
- Research note: {timestamp}
- Notes: {anything else}
```

## Stop-update schema (subsequent updates)

```
### YYYY-MM-DDTHH:MM:SSZ — STOP-UPDATE {SYMBOL}
- Previous stop: {type + level}
- New stop: {type + level}
- Reason: {trailing / locked profit / regime / thesis reinforcement}
- Routine: {routine name}
```

## Entries

### 2026-04-23T13:37:07Z — BUY GOOGL 7@$339.29
- Order ID: 1e58b2d7-9039-45bf-8b10-06e39c32f2d1 (stop: 45d94a3c-d7c9-44f6-bc8d-e6d38c6afef0)
- Value: $2,375.03
- % NAV at entry: 2.44%
- Instrument: equity
- Style: short-swing (3-4 trading days, pre-earnings exit mandatory)
- CTQS: C20/T19/Q18/S18 = 75/100 → Conviction Standard, downsized to Probe, confidence 55%
- Setup type: pre-earnings momentum + TPU/Anthropic catalyst reinforcement
- Catalyst: Earnings Q1 2026 on 2026-04-29 AMC (J-4 trading days). Secondary fuse: TPU 8t/8i launch + Anthropic multi-GW commitment announced 22/04.
- Thesis: Gemini 3 traction (750M MAU, +87% in 9 months), antitrust Mehta resolved Sep 2025, Cloud accelerating, TPU validated by Anthropic → convergence of signals pre-earnings. Scenario A activated (vs prior preference for post-earnings entry) due to 22/04 catalyst cluster.
- Stop: 8% trailing (Alpaca native, id 45d94a3c) @ $312.05 initial, hwm $339.185
- Take-profit: trailing only
- Time stop: 2026-04-28 close (mandatory pre-earnings exit)
- Earnings hold: NO (exit 28/04 close)
- Routine: market-open
- Research note: memory/equities/research_log.md — 2026-04-23 pre-market block, BUY 3
- Notes: Probe sizing $2,435 target; 7 shares × $339.29 = $2,375.03 (2.44% NAV — just under target but within Probe band 2-3%). GEV and VRT from the same BUY queue skipped at open due to wide spreads (GEV 4.66%, VRT 5.38% — early-open thin books) and FOMO guard on GEV (ask +14% vs plan $1,000).

### 2026-04-28T19:59:57Z — TRIM GOOGL 4@$349.85 (MOC partial fill)
- Order ID: 33e1dd7d-7c7f-4b2d-9d1f-2ecace102f20 (TIF=cls, qty=7 placed, qty=4 filled, qty=3 expired)
- Replaces native trailing stop 45d94a3c (canceled 2026-04-28T13:41:54Z when MOC was placed at market-open)
- Filled value: $1,399.40 (4 shares × $349.85 close auction)
- Realized P&L on the 4 shares: ($349.85 − $339.29) × 4 = +$42.24 (+3.11%)
- Reason: pre-earnings exit pre-staged at market-open per 04-27 daily-review carry-forward (post-04-24 INCIDENT remediation: exchange-bound exit not run-dependent). MOC partial-fill mechanics — 3/7 shares left unfilled at the close auction (Alpaca cls TIF expired at 20:02:20Z with filled_qty=4).
- Routine: market-open (placed) → market-close (audit + residual-cleanup follow-up)
- Notes: Partial fill is an unusual outcome on a $2T mcap name. Likely auction-imbalance routing chose to fill only 4/7 lots. Followup CUT for residual 3 shares queued same session — see 2026-04-28T20:10:26Z entry.

### 2026-04-29T13:31:25Z — CUT GOOGL 3@$345.71 (DAY market sell filled at the open)
- Order ID: c9a545bd-3caa-41ae-a9ef-a4d084c37255 (status=filled, filled_qty=3, filled_avg_price=$345.71)
- Submitted: 2026-04-28T20:10:26Z post-close · Filled: 2026-04-29T13:31:25Z (09:31 ET regular open, ~1 minute after the bell)
- Filled value: $1,037.13
- Realized P&L on the 3 shares: ($345.71 − $339.29) × 3 = +$19.26 (+1.89%)
- Total realized P&L on the GOOGL trade (4 shares MOC 04-28 + 3 shares DAY 04-29): +$42.24 + $19.26 = +$61.50 on $2,375.03 entry = +2.59% return on the position
- Reason: pre-earnings exit (no earnings hold). Earnings Q1 2026 = 2026-04-29 AMC (~20:00 UTC today). Exit at the regular open captured >6h margin before the print.
- Routine: market-open (verify-and-confirm — order placed at market-close 04-28; verified filled and tallied this run)
- Notes: GOOGL position fully closed. Net trade P&L +$61.50 / +2.59%; holding period 4 trading days (J+0 to J+4). Reinforces the 04-27 carry-forward and 04-24 INCIDENT remediation: queue-during-day market sell + DAY/GTD TIF + 14:30 last-call IOC fallback is the correct pre-earnings exit pattern (MOC TIF=cls alone can leave residual on partial fill). Book post-fill: 0 positions, 100% cash.

### 2026-04-28T20:10:26Z — CUT GOOGL 3 shares (DAY market sell, queued for 04-29 open)
- Order ID: c9a545bd-3caa-41ae-a9ef-a4d084c37255 (TIF=day, qty=3, market, status=accepted)
- Submitted post-close (20:10 UTC = 15:10 CT, 10 min after the bell)
- Expires: 2026-04-29T20:00:00Z (tomorrow's regular close) → will execute at tomorrow 13:30 UTC = 09:30 ET regular open
- Mark at queue: $349.62 (last trade) → notional ≈ $1,048.86
- Reason: cut pre-earnings — MOC partial-fill residual, no earnings hold. Earnings GOOGL Q1 2026 = 2026-04-29 AMC (~20:00 UTC tomorrow) → exit at tomorrow's regular open is well before the print and satisfies the no-earnings-hold guardrail.
- Routine: market-close (last-call)
- Notes: Considered extended-hours limit sell now (16:00-20:00 ET window) but Alpaca post-close quote was one-sided (bid $329.20 / ask $0) = no real liquidity at the moment of placement. DAY market sell is the safer mechanic — captures tomorrow's regular-session opening cross on a deep mcap. Reinforces the 04-24 INCIDENT remediation lesson: MOC TIF=cls is not deterministic on partial fills; for next pre-earnings exit, prefer queue-during-day market sell + GTD or use limit-IOC at the 14:30 last-call rather than rely on the close auction alone.
