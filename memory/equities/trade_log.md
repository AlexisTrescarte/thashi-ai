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

### 2026-04-28T13:41:58Z — STOP-UPDATE GOOGL
- Previous stop: trailing 8% (Alpaca native, id 45d94a3c-d7c9-44f6-bc8d-e6d38c6afef0), HWM $353.18, stop $324.93
- New stop: market-on-close sell qty=7, GTD today (id 33e1dd7d-7c7f-4b2d-9d1f-2ecace102f20, expires 2026-04-28T20:00:00Z)
- Reason: pre-staging mandatory pre-earnings exit on the exchange (earnings 2026-04-29 AMC, no earnings hold). Carry-forward from 04-27 daily-review + 04-24 INCIDENT remediation: convert the trail into a binding close-of-day exit so the routine doesn't depend on the 14:30 last-call waking up. Trade-off accepted: position is unprotected against intraday plunge between now and close (~6h), but the harness-gap pattern over the past week (5/9 missed routines on 04-27) made exchange-binding the dominant risk. Position currently +2.63% / +$67.52 mark $348.94, providing buffer.
- Routine: market-open
