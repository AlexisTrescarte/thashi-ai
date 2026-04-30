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

## 2026-04-30 — Daily review (grade: C)

### Performance
- Equity: $97,519.12 (day +0.077%, +$75.21 vs last_equity $97,443.91)
- Benchmark day (SPY+QQQ blend): +0.934% (SPY 711.59 → 718.41 = +0.958%; QQQ 661.59 → 667.61 = +0.910%; IEX feed)
- Alpha day: **-0.857%**
- Cumul since baseline 04-28: bot +0.065% · bench +1.195% (SPY 711.55 → 718.41 = +0.964%; QQQ 658.23 → 667.61 = +1.425%) · **alpha cumul -1.130%**

### Activity
- Trades opened today: 2 (GOOGL 7@$369.7114 BUY · LLY 5@$939.54 BUY) — both native 7% trailing stops attached within 11s of fill
- Trades closed today: 0 (the GOOGL 3@$345.71 CUT was filled 04-29, not today)
- Hit rate today: N/A | Avg R today: N/A
- Stops set within 5min on all new positions: **yes** (GOOGL +10s, LLY +11s)

### By setup (today)
- PEAD Pathway-B opportunistic: 2 BUYs opened, 0 closed → unrealized GOOGL +$101.25 (+3.91% from fill), LLY -$27.75 (-0.59% from fill); net intraday position-level +$73.50

### Open positions EOD (2)
- **GOOGL** 7 @ $369.7114 (entry 04-30 J+0, PEAD post-Q1-beat) · mark $384.18 · +$101.25 (+3.91% from fill, +9.78% vs 04-29 close) · native trail 7% (id 74ec67e0) HWM $385.84, stop $358.83 · time stop 05-07 close.
- **LLY** 5 @ $939.54 (entry 04-30 J+0, PEAD post-Q1-beat-and-raise) · mark $933.99 · -$27.75 (-0.59% from fill, +9.73% vs 04-29 close) · native trail 7% (id 8e54102c) HWM $945.50, stop $879.31 · time stop 05-07 close.

### What worked (2 lines)
- **Pathway-B PEAD execution textbook**: GOOGL fill at $369.71 (post-Q1-beat: revenue $109.9B / Cloud +63%) and LLY fill at $939.54 (post-Q1-beat-and-raise: revenue +56% YoY, FY guide raised) — both passed pretrade_guards + microstructure (LLY NEUTRAL 14.8 bps) and got their native trails attached within seconds; positions sized in their conviction tiers (GOOGL 2.65% Probe, LLY 4.82% Standard mid-band).
- **Spread-defer-then-fire mechanic on LLY**: 11:30 scan flagged spread 2.14% (over 0.5% cap → defer); 13:30 scan re-fetched, spread had normalized to 0.097% → fire. Same lesson family as 04-23 GEV/VRT spread-skip but applied in reverse — patience on liquidity captured the late-day continuation.

### What didn't (2 lines)
- **Cumul alpha now -1.13%** since 04-28 baseline (bench +1.20% on Mag-7 earnings beats and risk-on rally; bot +0.07% from cash-heavy posture). Today bot day +0.08% on a +0.93% blend session = -0.86% alpha day — the cash drag has been measurable now that we have a dated baseline; 99% cash through 04-29 missed the GOOGL/MSFT/META cluster gap.
- **3rd journal-commit failure in 5 trading days** ([HARNESS-GAP] 2026-04-30T16:35Z): pre-market 06:00 CT and market-open 08:30 CT both fired their slash commands but the journal step did not commit; GOOGL BUY only became visible to memory at 11:30 reconciliation. Pattern is recurring and the 04-30T16:35Z learnings entry already queues a journal-commit retry clause for the monthly evolution proposal.

### Discipline log
- Guardrail violations: 0 — none
- Time stops honored: N/A today (GOOGL J+0 / LLY J+0; both time-stop 05-07 close, well in horizon)
- Stop updates logged: 0 manual; 2 native auto-ratchets — GOOGL HWM $378.365 → $385.84 (stop $351.88 → $358.83), LLY HWM $938.34 → $945.4999 (stop $872.66 → $879.31)
- Sector mix EOD: tech 2.76% (GOOGL) + healthcare 4.79% (LLY) = 7.55% total — well within 25% sector cap
- Cash EOD: $90,158.23 (92.45%) — well above 10% floor

### Coherence adjustment
Raw metrics: alpha day -0.857% (within ±1%), 0 violations, hit/R undefined (no closes). Table strict reading → C (alpha within ±1% band; B requires alpha > 0; D starts at -1%). Settled **C**: today was a step up in execution vs the past week (2 clean BUYs with stops, microstructure-gated, sized properly) but the cumulative alpha drag (-1.13%) and the recurring HARNESS-GAP cap the grade. No upgrade to B because the day still printed negative alpha; no downgrade to D because every trade was disciplined.

### Carry-forward for tomorrow (Fri 2026-05-01)
- **GOOGL J+1**: PEAD continuation; native trail engaged. Action plan: hold while in-thesis; first TIGHTEN trigger at +10% trail-tightening per priority ladder (intraday-scan); time stop 05-07 close (J+5).
- **LLY J+1**: PEAD continuation; native trail engaged. Action plan: monitor for healthcare sector confirmation (XLV); TRIM trigger at +20% (Standard tier); time stop 05-07 close.
- **Aging J+6+**: none.
- **Pre-earnings tomorrow (05-01)**: AAPL AMC, AMZN AMC — Mag-7 cluster night. No exposure on book; pre-market must scan for Pathway-B PEAD candidates if any of the prints surprise materially.
- **Macro 24h**: NFP April release Fri 05-01 07:30 CT (typical first-Friday-of-May) → can swing pre-market; ISM Manufacturing 09:00 CT. Sizing one notch down on any new BUY before NFP per guardrails on dated event risk.
- **Regime note**: today **confirmed neutral-lean-risk-on** (SPY/QQQ near ATH on Mag-7 beats, AI capex undamaged, breadth holding ~53%); the 04-28 "risk-off twitch on OpenAI revenue concerns" reversed cleanly. Not tagging [REGIME-SHIFT] (single-session reversal is regime confirmation, not flip — needs 2+ sessions of structural change to tag).
- **Operational**: weekly-review fires Fri 16:00 CT after daily-review — must surface (a) 3 HARNESS-GAPs in 5 trading days, (b) cumul alpha -1.13% week-1 of formal baseline, (c) GOOGL+LLY PEAD stack into 05-07 horizon.
- **No risk-event tag today**: no DAILY-LOSS-CAP, no DRAWDOWN-AUTO-DEFENSE (DD from ATH -2.48%), no REGIME-SHIFT, no fresh INCIDENT (HARNESS-GAP already logged at 11:30Z).

### Lesson of the day (1 line)
- **Spread-defer-then-fire is a real Pathway-B tactic**: when a PEAD candidate gaps with a wide open book (LLY 11:30 spread 214 bps), defer to the next intraday-scan and re-fetch — today the 13:30 re-eval caught LLY at 14.8 bps and 70% confidence; codify into next pre-market: any spread-skipped name at market-open auto-queues for re-eval at 11:30 / 12:30 / 13:30 with the same plan price + 2% FOMO guard, no new research required.
