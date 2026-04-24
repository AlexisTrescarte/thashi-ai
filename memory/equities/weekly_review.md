# Weekly reviews — Equities

Append-only. Every Friday 16:30 CT, the `weekly-review` routine appends a section here.

See `.claude/commands/weekly-review.md` for the full template (performance, short-swing metrics, Bridgewater-lite risk audit, BlackRock-lite portfolio construction, JPMorgan-style next-week earnings watchlist, grade A/B/C/D/F, strategy adjustments).

## Reviews

## Week 2026-04-20 → 2026-04-24 — Grade D

### Performance
- Equity Friday close: $97,413.93 (1 open position GOOGL $2,406.53 + cash $95,007.40)
- Week: bot +0.0323%, bench (50% SPY + 50% QQQ) +1.4461%, **alpha -1.4138%**
- Cumul since Bull baseline (04-20 open): bot +0.0324%, bench +1.5645%, **alpha -1.5321%**
- Intra-week drawdown: -0.003% (min equity $97,379.63 on 04-23, trivial)
- SPY 04-17→04-24: 710.06 → 713.97 (+0.551%) · QQQ: 648.73 → 663.92 (+2.341%)

### Trade stats (from review skill)
- Closed: 0 | Hit rate: N/A | Avg R: N/A | Avg hold: N/A
- Best trade: N/A (no closes)
- Worst trade: N/A (no closes)
- Open: GOOGL 7 @ $339.29 (entry 04-23 market-open, current $343.79, unrealized +$31.50 / +1.326%)
- By setup: no P&L realized (PEM GOOGL pre-earnings J-4 open, unrealized only)
- By instrument: Equity 1 open (GOOGL), ETF 0, Lev-ETF 0, Options 0, Crypto 0
- By style: short-swing 1 open, day 0, swing 0, positional 0
- Guardrail violations: 0 cap breaches. 1 operational [INCIDENT] (missed routine cascade 04-24 — 6 routines no-show: pre-market, market-open, 3× intraday-scan, market-close)
- Time stops triggered: 0 (GOOGL time-stop 04-28 close not yet due)

### What worked (3-5 lines)
- Spread discipline held at open 04-23: GEV ask $1,140 / bid $1,086.84 = 4.66% spread AND FOMO guard violated (ask +14% vs plan $1,000) → mechanical SKIP. VRT spread 5.38% → mechanical SKIP. Prevented ≥ $180 of slippage on two names that gapped into thin books post-PEAD.
- GOOGL Probe sizing (2.44% NAV, discretionary downsize from Standard 75/100 CTQS) respected the pre-earnings binary-event budget; confidence-based override applied as designed.
- Alpaca-native trailing stop on GOOGL ratcheted autonomously (HWM $339.185 → $345.23, stop $312.05 → $317.61) through a silent agent day 04-24. The 04-21 RULE-ADJUSTMENT ("prefer native trailing") paid off — exchange-side discipline covered the agent's absence.
- Anti-revenge / anti-FOMO filter caught the post-gap chase risk on GEV (+13.75% day before) before it became a bad fill.

### What didn't (3-5 lines)
- **Activity floor badly missed**: 1 BUY filled / 5 TD vs target ≥ 3 BUY / rolling 5 TD in neutral-lean-risk-on regime. Cause #1: the 04-20 pre-market chose "AUCUN BUY" on first-day observation grounds — an explicitly forbidden standing reason per strategy.md activity-floor disclosure. Cause #2: 04-21 and 04-22 pre-markets did not produce fresh BUY queues, so 04-22 market-open was a forced no-op (noted in learnings 04-22 LESSON). Cause #3: GEV/VRT skips from 04-23 were never re-attempted via intraday-scan (all three intraday-scans were missed on 04-24).
- **Alpha drag -1.4%**: sitting 97.5% cash through a +1.45% bench week is the dominant cost. The cash was justified regime-wise (ATH + FOMC within 5 days + cluster earnings), but strategy.md explicitly says "the target is activity, the floor is quality" — we optimised for floor, not target.
- **[INCIDENT] 04-24 cascade**: 6 routines missed back-to-back. Only the 15:30 daily-review woke up. Root cause not yet diagnosed (remote trigger / harness). If 04-27 or 04-28 also miss, the mandatory pre-earnings exit on GOOGL fails and we're forced into an earnings hold we didn't underwrite.
- **Time-stops are agent-bound**: the GOOGL 04-28 close exit is a manual commitment with no exchange-side guarantee. A GTD sell limit or stop-limit at fill would have bound the exit to Alpaca, not to a future routine firing.

### Risk snapshot (Friday open positions)
- **Sector**: Communication Services (GOOGL) = 2.47% NAV. 1 sector exposed. Cap 25% (immutable) — well under.
- **Catalyst concentration**: 100% of live exposure ($2,406) concentrated on GOOGL earnings 04-29 AMC = 2.47% NAV single-event. Under the 5-name-per-event guardrail. No overlap with FOMC (earnings comes 2h after FOMC presser — sequential, not simultaneous, but cluster risk exists).
- **Correlation cluster**: 1 name (mega-cap tech / AI) — no cluster flag triggered (threshold is 3+).
- **Lev-ETF aggregate**: 0.00% (cap 15%).
- **Options aggregate**: 0.00% (cap 5%).
- **Crypto aggregate**: 0.00% (cap 15%).
- **Stress tests on current book (all on GOOGL $2,406.53)**:
  - -2% SPX day → GOOGL ~-2.5% (beta ~1.2) → -$60 ≈ -0.06% NAV
  - +15bp 10Y → mega-cap growth ~-1.5% → -$36 ≈ -0.04% NAV
  - VIX +30% intraday → GOOGL ~-4% → -$96 ≈ -0.10% NAV
  - Trivial absolute — the book is defensively cash-heavy.
- **Tail risks next 5 TD**: (a) hawkish FOMC surprise (statement language shift, Powell "higher for longer") — mega-cap growth hit; (b) GOOGL earnings miss or soft guide on capex — position still held if exit timing slips; (c) credit event or geopol shock (Iran ceasefire fragile per 04-20 note); (d) 04-27/04-28 routines miss again → time-stop fails → forced earnings hold (thesis broken per entry plan).

### Portfolio construction
- **Catalyst book**: 100% of exposure is catalyst-driven (GOOGL pre-earnings). Absolute catalyst book = 2.47% NAV. Target band implicit in strategy.md activity floor ≈ 10-20% deployed in neutral/risk-on. **DRIFT -8 to -18pp below target**.
- **Cash**: 97.53% vs target 10-15% neutral (or 20-30% late-cycle). **DRIFT +82pp above neutral target, +67pp above late-cycle target.** Rebalancing flag **YES**.
- **Instrument mix**: Equity 100% ($2,406) / ETF 0% / Lev-ETF 0% / Options 0% / Crypto 0%. Mono-instrument, no ETF or crypto diversification used.
- **Style mix**: short-swing 100% / day 0% / swing 0% / positional 0%. Mono-style.
- **Parallelism**: 1 active position vs strategy band (effective target ~5-15 in neutral regime). Over-concentrated in cash, under-dispersed in positions.
- **Rebalancing recommended**: **YES** — cash drift > 10pp (actual +82pp). Action for next week: deploy 8-15% NAV into 3-5 positions across instruments (equities + ETFs + maybe 1 option or crypto probe) consistent with CTQS ≥ 55 candidates surfaced at pre-market; respect FOMC window sizing (one notch down 04-28/04-29 per macro overlay).

### Next-week macro outlook (2026-04-27 → 2026-05-01)
- **Mon 04-27**: quiet data day. Earnings BMO light; some AMC mid-caps.
- **Tue 04-28**: FOMC meeting day 1 (no release). Consumer Confidence 09:00 CT (10:00 ET). Earnings: KO BMO, UPS BMO, SPOT BMO, GM BMO, SPGI BMO; MSFT originally rumoured but consensus now 04-29 AMC.
- **Wed 04-29**: **FOMC rate decision 13:00 ET (85% hold at 3.50-3.75%)**, Powell presser 13:30 ET — non-SEP meeting (no dot plot). ADP employment 07:15 CT. Q1 2026 GDP advance 07:30 CT. Earnings AMC: **GOOGL · MSFT · META** (Mag-7 triple).
- **Thu 04-30**: **PCE core (March) 07:30 CT** (primary Fed inflation gauge; consensus ~core +2.9% YoY). Jobless claims 07:30 CT. Earnings AMC: **AAPL · AMZN**.
- **Fri 05-01**: **NFP April 08:30 ET** (primary labour gauge). ISM Manufacturing PMI 09:00 CT. Earnings BMO: XOM, CVX.
- **Expected regime**: neutral → lean late-cycle if (a) PCE core > 3.0% YoY, or (b) Powell hawkish, or (c) Mag-7 guidance cut. Confirm risk-on only if FOMC dovish + PCE cool + Mag-7 beat+raise.
- **Setup bias**: (1) **FOMC pre-event de-risking 04-28 afternoon**: size new opens one notch down per macro overlay, halve options exposure to 2.5% cap. (2) **Post-FOMC PEAD wave 04-30/05-01**: if Mag-7 prints beat+raise in a non-hawkish Fed outcome, target PEAD entries on the clean reactions (no gap > 8%). Prefer the underperformers of the trio rather than chasing extension. (3) **Secondary themes**: energy (XOM/CVX earnings + WTI volatility), consumer discretionary (AMZN guide read-through), AI infrastructure (re-check GEV/VRT pullback for re-entry — PEAD window still open if tape holds). (4) **Avoid**: fresh longs Wed morning pre-FOMC; revenge re-entry on GOOGL within 5 TD if it was cut for a loss.

### Next-week earnings watchlist (condensed JPMorgan-style)

| Ticker | Date | BMO/AMC | EPS cons. | Rev cons. | Historical beat rate | Implied move | Avg 4Q reaction | Play |
|---|---|---|---|---|---|---|---|---|
| GOOGL | 2026-04-29 | AMC | ~$2.42 | ~$95B | 4/4 | ±5-6% | mixed (growth vs capex) | **Exit 04-28 close** (current open pos) → PEAD re-entry 04-30 if beat+raise & reaction < +8% |
| MSFT | 2026-04-29 | AMC | ~$3.55 | ~$74B | 4/4 | ±4-5% | +/- modest, Azure is the key | PEAD 04-30 if Azure > +34% & capex disciplined; skip if capex surprise |
| META | 2026-04-29 | AMC | ~$6.20 | ~$45B | 4/4 | ±7-8% | high vol (Reels, AI capex) | Wait-and-see (binary on capex guide) |
| AAPL | 2026-04-30 | AMC | ~$1.60 | ~$95B | 4/4 | ±3-4% | tight (services guide drives) | PEAD 05-01 only if services accelerate + iPhone guide holds; skip if China miss |
| AMZN | 2026-04-30 | AMC | ~$1.10 | ~$160B | 3/4 | ±6-7% | AWS growth = swing factor | PEAD 05-01 if AWS > +19% YoY; skip if AWS deceleration |
| XOM | 2026-05-01 | BMO | ~$1.75 | ~$82B | 3/4 | ±2-3% | modest on energy sector | Wait-and-see (WTI price dependent) |
| CVX | 2026-05-01 | BMO | ~$2.10 | ~$48B | 3/4 | ±2-3% | modest | Wait-and-see |
| KO | 2026-04-28 | BMO | ~$0.74 | ~$11.2B | 4/4 | ±2-3% | defensive, modest | Skip (quality but no fuse) |
| UPS | 2026-04-28 | BMO | ~$1.42 | ~$21B | 2/4 | ±4-5% | logistics macro read | Skip (structural headwinds) |
| SPOT | 2026-04-28 | BMO | ~$1.95 | ~$5.1B | 3/4 | ±8-10% | high vol | PEM if CTQS ≥ 70 at Monday pre-market; else skip |

**Re-queue carry-forward**: GEV (spread + FOMO on 04-23 open — re-score Mon pre-market, FOMO guard still caps at $1,020) · VRT (spread on 04-23 open — re-score Mon pre-market) — PEAD window from 04-22 reports tightens to J+5 by Tuesday, so decide fast.

### Adopted adjustments (if any, requires rationale)
- **None applied this week.** Weekly-review scope excludes strategy.md and guardrails.md edits (reserved to quarterly-rewrite / human edit respectively).
- **Proposal queued for monthly-deep-review** (to be written at 04-24+7 via prompt_evolution_proposals.md in its own review routine, not here): "For every new BUY with a dated exit inside the horizon (pre-earnings, time-stop), place a GTD sell limit or stop-limit at fill to bind the exit to the exchange" — triggered by 04-24 INCIDENT (missed-routine cascade). Rationale: GOOGL's 04-28 close exit is currently agent-bound, not exchange-bound; if 04-27 or 04-28 routines also miss, the pre-earnings exit fails. Not applied this week — requires sample size + monthly-review gate check.
- **Operational follow-up**: surface to user at next human opportunity that the 04-24 remote trigger schedule misfired; check claude.ai triggers `next_run_at` + `enabled` per CLAUDE.md guidance before Monday 04-27 06:00 CT pre-market.

### Grade rationale
- Window alpha -1.41% (borderline D-band: -1 to -3%).
- Hit rate / Avg R: undefined (0 closes).
- Guardrail violations: 0 cap breaches · 1 operational incident (missed routine cascade).
- Activity floor badly missed (1 BUY / 5 TD vs target ≥ 3 BUY / 5 TD) in a bench +1.45% week.
- Mitigants: no stop violations, native trail held the line during agent silence, discipline (spread + FOMO + sizing) functioned mechanically.
- **Grade: D** — alpha in D-band, operational incident, activity floor missed. Not F (no cap breach, no catastrophic loss, book intact). Not C (alpha beyond ±1%, incident is material, activity gap is repeated pattern after daily-review already flagged it).
