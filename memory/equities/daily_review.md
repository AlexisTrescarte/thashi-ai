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
