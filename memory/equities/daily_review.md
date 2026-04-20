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

## 2026-04-20 — Daily review (grade: C)

### Performance
- Equity: $97,382.47 (day ~0.00%, -$0.04 vs last_equity $97,382.51)
- Benchmark day (SPY+QQQ blend): n/a — baseline not yet captured (market-close snapshot missing, see incident)
- Alpha day: n/a (insufficient data)
- Trades closed: 0
- Trades opened: 0

### By setup (today)
- _no trades — setup breakdown n/a_

### What worked (2 lines)
- Conviction-over-activity respected: 4 routines ran (pre-market, market-open, midday, daily-review), 0 BUY forced despite ATH environment + CPI chaud + cluster earnings this week.
- GEV / GOOGL correctly held in WATCH pending 22/04 and 29/04 earnings — no FOMO entry on Monday gap-up attempts.

### What didn't (2 lines)
- BTCUSD residue ($3.82, hors-univers) carried over for a 3rd consecutive run — pre-market plan said close it, 3 runs later still open.
- Bull v2 `intraday-scan` did not run at 10:30/12:30/14:30 CT; legacy `midday` ran instead — routine wiring drift caught in learnings but uncorrected today.

### Discipline
- Guardrail violations: 0 (hard caps 10%/25%/10%/15%/5% all respected, cash 100%).
- Carry-over discipline gap: 1 (BTCUSD residue aged 3 runs without closure).
- Stops set within 5min: n/a (no new entries).
- Time stops honored: n/a.
- Stop updates logged: 0.

### Carry-forward for tomorrow (2026-04-21)
- **Aging positions**: none (only BTC residue, hors-univers — to be liquidated at next SELL-authorized run).
- **Pre-earnings tomorrow 21/04 (heavy cluster)**: INTC, LMT, HON, AXP, TFC, NEE, CMCSA, VRSN, PGR, DOW, KDP, BLK, BX. No Bull position exposed. Pre-market must rescan for post-print PEAD candidates Wed AM.
- **Macro 24h**: no Fed speaker high-impact; earnings season day 2. FOMC 28-29/04 still 99% hold. Watch 10Y yield if CPI revision hits.
- **Regime note**: confirm late-cycle ATH + hawkish Fed + hot CPI. No shift observed. Stay defensive on new entries, prefer cash until GEV (22/04) or GOOGL (29/04) catalysts resolve.
- **Priority action tomorrow**: (1) market-close MUST write baseline in portfolio.md (equity, SPY close, QQQ close, ATH init); (2) BTCUSD residue liquidation at first SELL-authorized routine.

### Lesson of the day (actionable)
**Market-close snapshot is a pre-requisite, not a nice-to-have.** If `portfolio.md` has no baseline when daily-review runs, daily-review must either trigger the snapshot itself or tag `[INCIDENT]` — never proceed blind. From tomorrow: first action of daily-review = verify `portfolio.md` last-updated date matches today; if not, write baseline from live Alpaca state before grading.

### Grade coherence
C reflects: disciplined no-op on trading (process-wise B+), offset by 2 unresolved discipline carry-overs (BTC residue + missing market-close snapshot + routine wiring drift). Process gaps > outcome, hence C.

