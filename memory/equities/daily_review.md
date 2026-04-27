# Daily reviews — Equities

Append-only. Every trading day at 15:30 CT the `daily-review` routine appends a section here.

Purpose: distilled lessons of the day, fast retrospective, feeds weekly/monthly aggregation.

## Schema

```markdown
## YYYY-MM-DD — Daily review (grade: A/B/C/D/F)

### Performance
- Equity: $X (day {+/-X.XX}%)
- Benchmark day (SPY+QQQ blend): {+/-X.XX}% | alpha day: {+/-X.XX}%
- Trades closed: N (W/L/BE)
- Trades opened: N

### By setup (today)
- Earnings momentum: W-L $P&L
- PEAD: ...
- ...

### What worked (2 lines)
- ...

### What didn't (2 lines)
- ...

### Discipline
- Guardrail violations: N ({details})
- Stops set within 5min: yes/no
- Time stops honored: yes/no

### Carry-forward for tomorrow
- Aging watchlist: ...
- Pre-earnings tomorrow: ...
- Regime note: ...
```

## Reviews

## 2026-04-24 — Daily review (grade: C)

### Performance
- Equity: $97,416.94 (day +0.04%, $37.31)
- Benchmark day (SPY+QQQ blend): N/A — baseline never posted (market-close 04-20 and 04-24 both missed); SPY 714.05 / QQQ 664.06 ref captured this run
- Cumul baseline: N/A (no baseline set)
- Trades closed: 0 (W:0 / L:0 / BE:0)
- Trades opened: 0

### By setup (today)
- None (no activity)

### Open positions (1)
- GOOGL 7 @ $339.29 (entry 04-23) · mark $344.12 · +1.42% ($+33.81) · native trail 8% ratcheted (HWM $339.185 → $345.23, stop $312.05 → $317.61) · time stop 04-28 close pre-earnings 04-29 AMC.

### What worked (2 lines)
- Native trailing stop on GOOGL ratcheted autonomously (HWM +$6.04, stop +$5.56) despite zero intraday-scan runs — the "prefer native trailing" rule (learnings 04-21 RULE-ADJUSTMENT) paid off by providing stop discipline without human-in-the-loop.
- GOOGL Probe sizing (2.44% NAV) behaved as designed: +1.54% intraday = $+36.61, held within Probe risk budget while TPU/Anthropic fuse remains intact pre-earnings.

### What didn't (2 lines)
- Operational failure — no routines executed on 04-24 (no pre-market / market-open / 3× intraday-scan / market-close in runs.log; no git commits since 04-23 market-open). Remote trigger / harness issue; the agent's discipline was not tested because the agent didn't wake up.
- GEV and VRT skip from 04-23 (spread + FOMO guard) was never re-attempted via intraday-scan 10:30/12:30/14:30 as planned — activity floor remains at 1 BUY / 5 TD (target ≥ 1/3 and ≥ 3/5); PEAD continuation window on GEV/VRT is slipping.

### Discipline log
- Guardrail violations: 0 (no trade activity)
- Time stops honored: N/A (GOOGL time stop is 04-28, not today)
- Stop updates logged: 0 manual; 1 native auto-ratchet on GOOGL (HWM $339.185 → $345.23 per Alpaca order state)

### Coherence adjustment
Raw metrics suggest B (day +0.04%, 0 violations, 0 closes → hit/R undefined). Grade downgraded to **C** because of [INCIDENT] on missed 04-24 routines — dynamic risk mgmt was absent; only Alpaca-native trailing saved the book from being flown blind.

### Carry-forward for tomorrow (next trading day = Mon 2026-04-27)
- **GOOGL** (J+2 Monday) — **mandatory pre-earnings exit 04-28 close** (earnings 04-29 AMC). Monday pre-market must re-confirm exit plan; Monday intraday-scan = last chance to TRIM if setup deteriorates.
- **Aging watchlist**: GOOGL only (J+2 Monday → J+3 Tuesday = exit day).
- **Macro 24h (Monday)**: FOMC window 28-29 avril opens; last pre-FOMC trading day. PCE core was due Fri 04-25 07:30 CT — confirm print at next pre-market (missed today's run means we need to ingest on Monday open).
- **Pre-earnings this week**: GOOGL 04-29 AMC (exit 04-28 close); MSFT/META/AMZN 04-29 or 04-30 (watchlist only, no position).
- **Re-queue from 04-23 skips**: GEV (FOMO guard kept at $1,020 cap for residual bias — only if price pulled back), VRT (re-check spread at open — beat+raise intact). Both must be re-scored Monday pre-market; PEAD window narrows after 3 sessions.
- **Regime note**: neutral lean risk-on on last-known reading (04-23 close); Monday pre-market must re-confirm post 04-24 + 04-25 closes (SPY 714.05, QQQ 664.06 captured as ref).
- **Incident remediation**: investigate why 04-24 routines didn't fire (cron/trigger scheduling). If repro risk exists for 04-27, flag to user.

### Lesson of the day (1 line)
- When a routine misses fire, Alpaca-native trailing stops are the *only* line of defense → every new BUY must carry a native trail (not manual-tracked), and time-stops inside the horizon must be enforced via GTD limit-sell orders placed at fill, not reliance on future intraday-scan runs.

## 2026-04-27 — Daily review (grade: C)

### Performance
- Equity: $97,461.46 (day +0.044%, +$43.26 vs last_equity $97,418.20)
- Benchmark day (SPY+QQQ blend): ~+0.04% (SPY ~$714.90 vs Fri 714.05 = +0.12%; QQQ ~$663.80 vs Fri 664.06 = -0.04%) — intraday quotes captured 15:32 CT
- Alpha day: ≈ +0.00% (flat to bench within rounding)
- Cumul baseline: N/A (baseline never posted; 04-20 and 04-24 market-close both missed — this gap not closeable retroactively)

### Activity
- Trades opened today: 0
- Trades closed today: 0 (W:0 / L:0 / BE:0)
- Hit rate today: N/A | Avg R today: N/A
- Stops set within 5min on all new positions: N/A (no new positions)

### By setup (today)
- None — no activity

### Open positions (1)
- GOOGL 7 @ $339.29 (entry 04-23, J+2 trading days) · mark $350.58 · +3.33% (+$79.03) · native trail 8% ratcheted (HWM $339.185 → $353.18 today, stop $312.05 → $324.93) · time stop 04-28 close pre-earnings 04-29 AMC.

### What worked (2 lines)
- Native trailing on GOOGL kept ratcheting autonomously through the 5 missed routines (HWM $345.23 Fri → $353.18 today, stop $317.61 → $324.93) — exchange-side discipline filled the gap left by the silent harness, exactly as the 04-21 RULE-ADJUSTMENT predicted.
- Priority ladder held cleanly across the 3 scans that did fire (11:30/13:30/14:30): no premature TIGHTEN/TRIM/CUT on a +3.3% Probe — discipline of "P10 hold until P1-P9 trigger" prevented over-management of an in-thesis position.

### What didn't (2 lines)
- Pre-market 06:00 CT did not fire (3rd straight missing pre-market for equities — no 04-24, no 04-25 weekend, no 04-27) → BUY Pathway A blocked all day; with no fresh CTQS scan and no qualifying B/C catalyst, the agent ran cash 97.5% on a market that printed near ATH on QQQ — opportunity cost is unmeasured but real.
- Market-open 08:30 CT, intraday-scan 10:30/12:30 CT and market-close 15:00 CT also absent from runs.log/git — 4 daytime routines plus pre-market = 5 missed of 9 expected, recurrence of the 04-24 harness-gap pattern (different routines missing this time but same root cause).

### Discipline log
- Guardrail violations: 0 — none (no trades placed)
- Time stops honored: N/A today (GOOGL time-stop is 04-28 close, not 04-27)
- Stop updates logged: 0 manual; 1 native auto-ratchet on GOOGL (HWM +$7.95, stop +$7.32 vs Fri ratchet)

### Coherence adjustment
Raw metrics: alpha ~0%, 0 violations, 0 closes (hit/R undefined). Strict reading of the table → B (alpha > 0 marginally, 0 violations) or C (alpha ±1%, hit/R undefined). Settled on **C** because: (a) hit/R cannot validate B-grade discipline, (b) recurring harness gap (3rd missing pre-market in a row) is an operational degradation worth flagging in the cumulative trend, (c) cash 97.5% on a near-ATH risk-on day is a missed deployment under strategy.md "conviction over activity" only when there's a fresh CTQS scan — without one, no valid B-grade case can be made.

### Carry-forward for tomorrow (Tue 2026-04-28)
- **GOOGL — CRITICAL**: mandatory pre-earnings exit **04-28 close** (earnings 04-29 AMC). Tomorrow 14:30 CT last-call slot is the binding window. **Pre-place the exit at 04-28 market-open as belt-and-suspenders**: convert the 8% trailing to either (a) a GTD market-on-close sell or (b) a tight stop-limit at $349 (≈ -0.4% from current mark) to bind the exit to the exchange — DO NOT rely solely on the 14:30 routine waking up. This addresses the 04-24 INCIDENT remediation that was queued.
- **Aging watchlist**: GOOGL J+3 = exit day; no other names.
- **Pre-earnings tomorrow (04-28)**: GOOGL only on book. AMC tomorrow includes various names (V, etc. — confirm pre-market) but no exposure on book.
- **Macro 24h**: FOMC starts 04-28 (Tue) → decision 04-29 (Wed) AMC, hold ~94.8% probability. Sizing one notch down for any new BUY per guardrails. PCE core (Fri 04-25 print) — confirm reading at 04-28 pre-market.
- **Re-queue from 04-23 skips**: GEV (FOMO bias > $1,020 still a guard) and VRT (re-check spread + price) — must be re-scored at 04-28 pre-market if it fires; PEAD window now J+4 since 04-22 print, narrowing fast.
- **Regime note**: neutral lean risk-on confirmed today (VIX 18-19, SPY/QQQ near ATH). FOMC week → expect compression; tighten any new stop methodology from default trail by 1-2pp.
- **Operational**: 04-28 pre-market 06:00 CT MUST fire for GOOGL exit pre-staging; if it doesn't, the agent at next-fire-routine must execute the pre-place action before any other work.

### Lesson of the day (1 line)
- **Pre-stage the GOOGL exit at 04-28 market-open** with a GTD market-on-close (or stop-limit at $349) — do not let the 14:30 last-call routine be the single point of failure for a mandatory pre-earnings exit, because today proved 50%+ of routines can miss in a single session and the exchange is the only reliable executor when the harness is silent.
