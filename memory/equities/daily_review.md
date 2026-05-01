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

## 2026-05-01 — Daily review (grade: C)

### Performance
- Equity: $97,614.06 (day +0.0915%, +$89.23 vs last_equity $97,524.83)
- Benchmark day (SPY+QQQ blend): +0.6308% (SPY $718.41→$720.49 = +0.290%; QQQ $667.61→$674.10 = +0.972%)
- Alpha day: **−0.539%** (cash-heavy book lagged a risk-on tape)
- Cumul since baseline (04-28): bot +0.163% · bench +1.834% · **alpha cumul −1.671%** (deployment lag from 100% cash through 04-29 still drags the book)

### Activity
- Trades opened today: 1 (AAPL Pathway A PEAD, reconciled at 11:30 — see [HARNESS-GAP] tag)
- Trades closed today: 0 (W:0 / L:0 / BE:0)
- Hit rate today: N/A | Avg R today: N/A
- Stops set within 5min on all new positions: yes — AAPL trail 6% native placed 13 sec after fill (order 43ed6c8b, GTC, HWM $287.22 / stop $269.99)

### By setup (today)
- PEAD (Pathway A): 1 BUY · AAPL 16@$282.83 · CTQS 84 Standard · 4.64% NAV · J+0 mark $279.78 (−1.08%)
- Holds: GOOGL J+1 (+4.12% cumul, day +0.04%), LLY J+1 (+2.39% cumul, day +2.93%), AAPL J+0 (−1.08%)
- Skipped: CAT (spread 6.85%→1.823% never normalized), AMZN (technical borderline), RDDT (FOMO +16%), EL/RBLX/WDC (FOMO/broken/bad-tape)

### Open positions (3)
- AAPL 16 @ $282.83 (J+0) · mark $279.78 · −1.08% (−$48.87) · trail 6% stop $269.99 · time stop 05-08 close
- GOOGL 7 @ $369.71 (J+1) · mark $384.95 · +4.12% (+$106.67) · trail 7% stop $359.66 · time stop 05-07 close
- LLY 5 @ $939.54 (J+1) · mark $962.01 · +2.39% (+$112.35) · trail 7% stop $915.54 (ratcheted on +2.93% day) · time stop 05-07 close

### What worked (2 lines)
- LLY day-2 PEAD continuation paid: +2.93% on the day, +$137.05 unrealized — vindicates the 04-30 13:30 Pathway-B late-day entry on the spread-normalization re-check (LLY 11:30 spread 2.14% → 13:37 0.097% → fill). Native 7% trail ratcheted autonomously through the run-day, exchange-bound discipline.
- AAPL Pathway-A executed mechanically per pre-market plan (CTQS 84 / China+iPhone+GM trifecta / Standard 4.64% NAV / 6% trail placed 13 sec after fill) — reconciled cleanly at 11:30 after market-open journal-fail. The pattern "trades execute on Alpaca despite journal-commit fail" is now the *expected* HARNESS-GAP recovery shape and intraday-scan Step 2 (verify-via-API) caught it on the first pass.

### What didn't (2 lines)
- Cash-heavy book (87.7% post-trade) lagged the QQQ rally: bot +0.09% vs bench +0.63% = **−0.54% alpha day**, accumulating to −1.67% alpha cumul over the 4-day baseline window. The drag is structural, not single-trade — slow deployment from 100% cash on 04-29 through 04-30/05-01 missed the meat of the post-FOMC + Mag-7-PEAD impulse.
- CAT Pathway-B (CTQS 76 beat-and-raise + record backlog) spread-skipped all of D+0 (6.85% at 11:30 → 1.823% at 13:30 — never under the 0.5% cap). 3rd same-pattern leader miss in 9 td (GEV/VRT 04-23, CAT 05-01) — the new "Pathway-B J+1 fallback" lesson exists exactly to absorb this; Monday pre-market must execute it on CAT.

### Discipline log
- Guardrail violations: 0 — none placed, none attempted
- Time stops honored: N/A today (AAPL J+0, GOOGL J+1, LLY J+1 — all far from time stops)
- Stop updates logged: 1 placed (AAPL initial trail 6% / stop $269.99, 13 sec after fill); 0 manual updates; 2 native ratchets on GOOGL/LLY (LLY HWM $938.34→$962.01, stop $872.66→$894.67 ≈ -7%; GOOGL trail tracked through book)
- HARNESS-GAP tags appended today: 2 ([market-open journal-fail @ 13:47 UTC for AAPL], [12:30 intraday-scan no-fire]) — operational, not discipline. 5–6th and 7th in a 9-td rolling count. No risk-event tag warranted.

### Coherence adjustment
Raw metrics: alpha day −0.54% (within ±1% C-band), 0 violations, 0 closes (hit/R undefined). Strict reading → **C**. Not B (alpha negative + cumul lag worsening), not D (alpha < -1% threshold not breached, no discipline violation). Cumulative alpha drag (-1.67% in 4 td) is concerning and feeds the next weekly-review, but isolated to today the grade stands at **C**.

### Carry-forward for Monday (2026-05-04)
- **AAPL J+1**: native trail 6% / stop $269.99 (-3.7% buffer from $279.78). Pathway-A in-thesis on China+iPhone+GM trifecta. Watch reclaim of $283 = entry break-even; breakdown < $278 = early concern. Pre-market re-CTQS not needed (single-day trade).
- **GOOGL J+2**: native trail 7% / stop ratcheted ~$359.66 area. Time stop 05-07 close (J+5). Up +4.12% cumul on Q1 PEAD. Hold per priority ladder; let trail run.
- **LLY J+2**: native trail 7% / stop ratcheted to ~$894 area on today's +2.93% day. Time stop 05-07 close (J+5). Up +2.39% cumul. Hold; multi-day GLP-1 PEAD intact (target $30-50 of drift).
- **Pathway-B J+1 fallbacks** (per today's LESSON 2026-05-01T18:36:00Z): re-CTQS at Monday pre-market for **CAT** (J+1 spread normalization expected, FOMO guard at the new mark, T-grade may improve on a J+1 base-build) and **AMZN** (J+1 technical confirmation if $270 reclaimed). Both have intact post-print theses; missed D+0 on mechanical guards.
- **Macro 24h (Mon 05-04)**: ISM Mfg PMI 09:00 CT, Factory Orders 09:00 CT. No FOMC speakers scheduled. NFP confirmed rescheduled to **2026-05-08** (Friday next week) — pre-market 05-08 must apply confidence notch-down. NFP calendar source = BLS (https://www.bls.gov/schedule/news_release/empsit.htm).
- **Pre-earnings this week**: AMD 05-05 AMC (no current position; if BUY queued at Monday pre-market, mandatory GTD-exit-at-fill per 04-24 INCIDENT remediation). PLTR 05-05 AMC. Several other tech names tail.
- **Regime note**: neutral lean risk-on confirmed by today's tape (VIX < 17 print, broad +0.3/+0.6/+1.0 SPY/QQQ/RTY, 53% SPX > MA50 holds the breadth-yellow line). Watch for breadth crack < 50% as regime-shift trigger. NFP defer relieves immediate macro-fog through Thursday.
- **Operational**: 4 of 6 trading days now show ≥ 1 journal-commit failure. Monthly-review proposal queue (promote-now): journal-commit retry + [JOURNAL-COMMIT-FAIL] direct-write fallback + slot-firing reliability diagnostic. **Today's 2 HARNESS-GAPs cost 0 P&L** (AAPL was reconciled cleanly at 11:30; the 12:30 no-action slot was zero blast-radius). The pattern remains structurally critical regardless of zero-cost individual events.

### Lesson of the day (1 line)
- **Calibration fix on macro-event days**: pre-market must validate the calendar source (BLS / Fed) BEFORE applying confidence notch-downs — today's NFP was already public-rescheduled to 05-08 at 06:00 CT, and the over-conservative −7pp notch (75% → 68%) cost AAPL ~36 bp of NAV by sizing 4.64% instead of upper-Standard 5.0% on a CTQS 84 idea. Add `WebFetch BLS schedule` to pre-market step 0 on any NFP/CPI/PCE day.
