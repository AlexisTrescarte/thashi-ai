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

## 2026-04-23 — Daily review (grade: B)

### Performance
- Equity: $97,379.14 (day **-0.00%** — flat vs last_equity $97,382.43)
- Benchmark day (SPY +QQQ 50/50): SPY -0.39% · QQQ -0.56% → **-0.48%** | alpha day: **+0.48%**
- Cumul since baseline: baseline not yet posted (market-close of 2026-04-20 was retro-pending); vs last_equity 22/04 → flat. SPY 23/04 close 708.41, QQQ 651.40 captured for retro-baseline.
- Trades closed: 0
- Trades opened: 1 (GOOGL Probe 2.44% NAV)

### By setup (today)
- Pre-earnings momentum + catalyst-reinforcement (GOOGL): 1 open, MTM -$3.29 (-0.29%) EOD — no close, no realized P&L yet.
- PEAD beat+raise (GEV, VRT): **0 opened** — both rejected at open on spread > 0.5% (GEV 4.66% + FOMO guard ask +14% vs plan; VRT 5.38%). No technical breakout setup this session.

### What worked (2 lines)
- Discipline mechanic: two forced skips (GEV, VRT) on spread/FOMO guard prevented 7-8% slippage on thin gap-day open books — single largest protection of the session.
- Cash posture protected the book on a broad red tape (-0.48% bench) via 97.56% cash residual; alpha day +0.48% is pure beta-avoidance, not stock selection.

### What didn't (2 lines)
- Activity floor still light: 1 BUY filled vs 3 queued pre-market (0.20 filled-ratio) → 1 BUY / 5 TD rolling, floor (≥ 3/5 TD risk-on) still missed.
- Market-open timing cost: entering GEV/VRT in the first 10 minutes of a post-gap tape = mechanical rejection. The plan should have routed those names to intraday-scan 10:30 from the outset.

### Discipline log
- Guardrail violations: **0** — zero override attempted on spread cap or FOMO guard; both GEV/VRT skips logged in trade_log context.
- Time stops honored: N/A (GOOGL time stop = 28/04 close, 3 TD away).
- Stop updates logged: **0 manual** — Alpaca native trailing ratcheted GOOGL stop $312.05 → $314.60 (hwm $341.96 touched intraday). One-way ratchet intact.
- Stops set within 5min on all new positions: **yes** (GOOGL trailing 8% placed at 13:37:07Z, same txn as fill).

### Carry-forward for tomorrow (2026-04-24, Friday)
- **Aging J+1+**: GOOGL J+1 (entered 23/04). No aging concern. Pre-earnings exit mandatory **28/04 close** (still 3 TD away).
- **Pre-earnings tomorrow on book**: none. GOOGL earnings = 29/04 AMC (J-3 TD).
- **BMO 24/04**: SLB, PG, CHTR, NSC — none in book, none in queue.
- **Semis angle**: INTC reports AMC tonight (23/04). Impact on 24/04 open for SMH (WATCH) — if INTC beat → SMH breakout candidate for pre-market BUY queue; if miss → expected SMH -2%, potential reset-entry probe.
- **Re-queue for intraday-scan 10:30 or 24/04 open**: **VRT** only (spread-driven skip was mechanical, not thesis-driven — if spread < 0.5% and price still in zone, entry authorized via intraday-scan). **GEV** blocked for re-entry > $1,020 for the rest of 23/04 by FOMO guard; pre-market 24/04 to reassess fresh with updated quotes.
- **Macro 24h**: **PCE core Friday 25/04 07:30 CT** = primary macro event. FOMC 28-29/04 (hold 94.8%) → sizing remains normal until 27/04. Watch 10Y, DXY, VIX for flip signals.
- **Regime note**: Neutral lean risk-on confirmed pre-market, but broad tape sold -0.48% today on "priced-to-perfection" reactions (IBM -7.7%, NOW -14%, TSLA flat post-capex). If 24/04 delivers another red session, **regime flip to neutral** possible → tighten all stops one notch via intraday-scan.

### Lesson of the day (1 line, actionable)
- **Route PEAD/gap >10% leaders to intraday-scan 10:30, never market-open**: the 0.5% spread cap is designed to reject thin post-gap books — pre-market queues should explicitly stage such names for 10:30 entry from the outset, not market-on-open. Adjustment for next pre-market: flag any "gap > 10% in last session" idea with *"entry via intraday-scan 10:30"* directive.

### Grade coherence
- Alpha day +0.48%, zero violations, stops set within 5min, discipline perfect on two skips → **B is the right read** (alpha positive but not > +2%; 0 closed trades means hit-rate/avg-R N/A, preventing an A). The lone drag on grade is the unclosed activity-floor gap — a tactical miss, not a discipline failure.
