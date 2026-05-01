# Weekly reviews — Equities

Append-only. Every Friday 16:30 CT, the `weekly-review` routine appends a section here.

See `.claude/commands/weekly-review.md` for the full template (performance, short-swing metrics, Bridgewater-lite risk audit, BlackRock-lite portfolio construction, JPMorgan-style next-week earnings watchlist, grade A/B/C/D/F, strategy adjustments).

## Reviews

## Week 2026-04-27 → 2026-05-01 — Grade C

### Performance
- Equity Friday close: $97,619.60
- Week (Mon 04-27 close $97,461.46 → Fri 05-01 $97,619.60): bot **+0.16%**, bench (50% SPY + 50% QQQ) **+1.08%** (SPY $714.90 → $720.55 = +0.79% · QQQ $663.80 → $672.91 = +1.37%), alpha **−0.92%**
- Cumul since baseline 04-28: bot $97,455.66 → $97,619.60 = **+0.17%**, bench (SPY $711.55 → $720.55 = +1.27% · QQQ $658.23 → $672.91 = +2.23%) **+1.75%**, alpha **−1.58%**
- Intra-week drawdown: ≤ −0.10% (book stayed inside $97,397–$97,620 band; very mild)

### Trade stats (review skill — n too small for Sharpe/Sortino)
- Closed: **1** | Hit rate: **100%** (n=1, not statistically meaningful) | Avg R: **0.32** | Avg hold: **4 trading days**
- Best trade: **GOOGL** (+2.59% / +$61.50, pre-earnings momentum, 4 td)
- Worst trade: n/a (no closed loser)
- By setup: pre-earnings momentum (closed) +$61.50 · PEAD (open unrealized) GOOGL +$108.07 + LLY +$113.45 + AAPL −$45.83 = **+$175.69 unrealized open**, +$61.50 realized
- By instrument: equity +$61.50 realized, +$175.69 unrealized · ETF $0 · Lev-ETF $0 · Options $0 · Crypto $0
- By style: short-swing 100% (1 closed + 3 open) · day 0 · swing 0 · positional 0
- Guardrail violations: **0**
- Time stops triggered: **1 / 1** (GOOGL pre-earnings exit 04-28 close — honored cleanly via DAY+MOC pre-stage; reinforced 04-24 INCIDENT remediation)
- Trades opened this week: **3** (GOOGL re-entry 04-30, LLY 04-30, AAPL 05-01) — all Pathway A or B PEAD, all native trails placed within 60 sec of fill

### What worked
- **Pre-earnings exit pattern delivered**: GOOGL 04-28 DAY+MOC pre-stage + 04-29 DAY market sell residual = clean +2.59% close, 4 td hold, time-stop honored — direct payoff of 04-24 INCIDENT remediation lesson (exchange-bound, not run-dependent).
- **Pathway B opportunistic catches**: GOOGL re-entry 04-30 +4.18% J+1 + LLY 04-30 +2.42% J+1, both on textbook beat-and-raise PEAD; LLY caught by spread-normalization re-eval at 13:30 (2.14% → 0.097%) — direct payoff of 04-29 spread-protocol fix.
- **Native trailing discipline absorbed all 5 harness gaps** in 6 td — every position carried a native Alpaca GTC trail; one-way ratchets locked in protection across missed routines (AAPL HWM $287.22 / GOOGL HWM $386.74 / LLY HWM $984.45).
- **Anti-FOMO + spread guards rejected 4 chase candidates** (CAT 1.823% spread, RDDT +16% gap, EL +12% gap, RBLX broken-thesis) — none cost the book; CAT and RDDT carry forward to Monday 05-04 pre-market for J+1 fallback.
- **Activity floor restored**: 3 BUY / 5 td (target ≥ 3) — first time the floor has been met since launch.

### What didn't
- **Cumul alpha −1.58% since baseline** = 100%-cash drag through 04-29 (post-GOOGL exit, pre re-entry) while QQQ rallied +2.23% in 3 td. Re-deployment 04-30 partially recovered but the gap is the dominant alpha-killer this week.
- **5 harness gaps in 6 td** (4 of them = trades-fired-but-journal-failed; 1 of them = full slot miss at 12:30 CT 05-01). Structural operational degradation — promote-now remediation queued for 2026-05-29 monthly-deep-review.
- **Same-session spread normalization failed on CAT 05-01** (6.85% → 1.823%, never crossed 0.5% cap) — first clean data point that mega-cap industrial PEAD names normalize slower than tech (LLY 04-30 caught at 0.097% by 13:37) or do not normalize at all same-day. New "Pathway B J+1 fallback" proposal queued.
- **AAPL gap-fill pulled red** intraday (+0.20% at 11:30 → −1.01% at Fri close) — normal day-1 PEAD behavior but cost some of the entry edge; trail $269.99 still has 3.5% buffer below mark, no action.
- **AMZN day-2 PEAD never confirmed** the $270 reclaim across 11:30/13:30 scans — borderline tech setup deferred to Monday day-3 read.

### Risk snapshot (Friday open positions)
- AAPL 16 @ $282.83 → mark $279.97 → MV $4,479.52 → **4.59% NAV** (P&L −1.01%, native 6% trail GTC, HWM $287.22, stop $269.99)
- GOOGL 7 @ $369.71 → mark $385.15 → MV $2,696.05 → **2.76% NAV** (P&L +4.18%, native 7% trail GTC, HWM $386.74, stop $359.66)
- LLY 5 @ $939.54 → mark $962.23 → MV $4,811.15 → **4.93% NAV** (P&L +2.42%, native 7% trail GTC, HWM $984.45, stop $915.54)
- **Total deployed: $11,986.72 = 12.28% NAV · cash 87.72%**
- Sector: Tech 7.35% (AAPL + GOOGL) · Healthcare 4.93% (LLY) — both well under 25% immutable cap
- Catalyst concentration: 100% of book on PEAD setup (single setup-type cluster) but **distinct earnings events** (different prints, different sectors) → low single-event tail
- Correlation cluster: AAPL + GOOGL = 2 mega-cap tech (correlated); LLY orthogonal — yellow flag, not red (3+ to refuse new buy)
- Macro exposure: long mega-cap tech (long-duration tilt); LLY moderate-duration; net long-duration; USD-denominated; AAPL has Greater China exposure ($20.5B Q2 = 18% of revenue)
- Lev-ETF aggregate: **0%** (cap 15%) ✓ · Options aggregate: **0%** (cap 5%) ✓ · Crypto aggregate: **0%** (cap 15%) ✓
- Stress test (12.28% deployed):
  - **−2% SPX day** → est. −0.25% to −0.30% NAV (book beta ≈ 1)
  - **+15bp 10Y** → est. −0.10% to −0.15% NAV (modest duration tilt)
  - **VIX +30% intraday Mon** → est. −0.40% to −0.60% NAV (cash buffer absorbs most)
- Tail risks: (1) **NFP 05-08 hot print** → hawkish rate-path repricing, tech leg −0.5% to −1% NAV; (2) **AAPL Greater China shock** (tariff escalation) → −0.10% to −0.20% NAV on AAPL alone; (3) **GLP-1 competitive shock** (NVO breakthrough or LLY safety signal) → −0.20% to −0.40% NAV on LLY; (4) **VIX > 30 / credit event** → defensive trigger; (5) Iran/Strait of Hormuz dormant but live; oil +$10 ripples to inflation re-acceleration narrative.

### Portfolio construction
- Catalyst book: **12.28% NAV** (target neutral risk-on regime ≈ 30-60% per strategy implicit; **drift > 10pp under-deployed**)
- Cash: **87.72%** (target neutral risk-on 10-15% per strategy.md; **drift > 70pp over-cash**)
- Instrument mix: Equity **100%** / ETF 0% / LevETF 0% / Options 0% / Crypto 0% (under-diversified vs strategy palette — no thematic ETFs, no commodity hedge, no crypto exposure)
- Style mix: short-swing **100%** / day 0% / swing 0% / positional 0%
- Active positions: 3 (within bands, not over-dispersed)
- **Rebalancing recommended: YES** — primary action item for next week is sustained capital deployment via Pathway B/C BUYs to close the cash drift; secondary is instrument diversification (consider an ETF or commodity hedge if PEAD wave thins, consider crypto sleeve when ETF flows turn).

### Next-week macro outlook (Mon 05-04 → Fri 05-08)
- **Mon 05-04**: ISM Services PMI 09:00 CT (forecast ~52.0), Factory Orders 09:00 CT
- **Tue 05-05**: **AMD Q1 2026 earnings AMC** (J−2 watch: capex narrative split post 04-30 META/MSFT, breadth confirmation needed); DIS BMO; MAR BMO; CVS, etc.
- **Wed 05-06**: light data
- **Thu 05-07**: Initial jobless claims 07:30 CT; FOMC minutes 13:00 CT (post 04-29 hold)
- **Fri 05-08**: **NFP April 07:30 CT** (rescheduled from 05-01) — binary macro event of the week; consensus ~+200k, unemp 4.0%; **major-macro-within-24h sizing notch-down rule activates Thu 05-07 from 13:00 CT onwards**
- Geopol: Iran peace process developments (tail compression continues); tariff calendar
- Expected regime: **neutral lean risk-on** (VIX <17, broad-tape participation, breadth firming) — confirm Monday at pre-market
- **Setup bias for next week**: (a) **PEAD continuation** on AAPL/GOOGL/LLY (already held — manage time-stops 05-07 / 05-08); (b) **AMD pre-earnings momentum probe** J−2/J−1 if breadth holds and capex narrative doesn't bleed semis (size Probe 2-3% on AMD given 04-30 META/MSFT post-print drag on AI capex names); (c) **CAT D+1 J+1 entry** Monday open if spread normalizes (≤ 0.5% AND FOMO guard on new mark); (d) **AMZN day-3 PEAD** if reclaims $270 with volume; (e) **RDDT pullback consolidation entry** if FOMO settles into a low-vol base; (f) NFP-week → reduce options exposure to 2.5% cap on Thu/Fri, freeze new opens during Friday's print window.

### Next-week earnings watchlist (JPMorgan-style)

| Ticker | Date | BMO/AMC | EPS cons. | Rev cons. | 4Q beat rate | Implied move | Avg 4Q reaction | Play |
|---|---|---|---|---|---|---|---|---|
| AMD | 2026-05-05 | AMC | $1.18 | $7.50B | 4/4 | ±9% | +/-/+/+ mixed | Pre-earnings momentum probe (J-2/J-1 if breadth + semis hold; Probe 2-3% NAV; 7% trail; mandatory exit 05-05 close) |
| DIS | 2026-05-07 | BMO | $1.20 | $24.0B | 3/4 | ±5% | mixed | Wait-and-see, no entry — non-tech secular headwind |
| MAR | 2026-05-06 | BMO | $2.45 | $6.40B | 3/4 | ±4% | mixed | Skip — no edge |
| CVS | 2026-05-07 | BMO | $1.70 | $94.0B | 2/4 | ±6% | mixed | Skip — sector noise |
| AAPL (held) | 2026-04-30 (printed) | — | — | — | — | — | — | **Hold** to time-stop 2026-05-08 close; PEAD play; trail 6% engaged |
| GOOGL (held) | 2026-04-29 (printed) | — | — | — | — | — | — | **Hold** to time-stop 2026-05-07 close; PEAD play; trail 7% engaged |
| LLY (held) | 2026-04-30 (printed) | — | — | — | — | — | — | **Hold** to time-stop 2026-05-07 close; PEAD play; trail 7% engaged |
| CAT (watch) | 2026-04-30 (printed) | — | — | — | — | — | — | **D+1 J+1 entry Monday pre-market** — re-CTQS at open quote, FOMO + spread re-checked |
| AMZN (watch) | 2026-04-29 (printed) | — | — | — | — | — | — | **Day-3 PEAD watch** Monday — entry only on $270 reclaim with volume |
| RDDT (watch) | 2026-04-30 (printed) | — | — | — | — | — | — | **Pullback consolidation entry** Monday if FOMO settles |
| NVDA (watch) | late May 2026 | AMC | TBD | TBD | 4/4 | ±8% | +/+/+/+ strong | Probe pre-earnings momentum build later in May (10-14d J−5 setup) |

### Adopted adjustments
- **None this week** — strategy.md and guardrails.md both untouched (per template; weekly-review does not modify strategy).
- **Carry-over to 2026-05-29 monthly-deep-review proposal queue** (4 items pending):
  1. **[promote-now] Journal-commit retry + [JOURNAL-COMMIT-FAIL] direct-write fallback** — 5 harness gaps in 6 td is structural; cannot wait another month.
  2. **GTD-exit-at-fill remediation** for any BUY with a dated exit (pre-earnings, time-stop in horizon) — first articulated 04-24 INCIDENT, reinforced 04-28 MOC partial-fill.
  3. **14:30 last-call IOC fallback** for pre-earnings MOC partial-fill scenarios.
  4. **Pathway B J+1 fallback** for same-session spread-skipped names (3 data points: GEV/VRT 04-23, LLY 04-30 caught D+0, CAT 05-01 abandoned D+0).
- **Operational follow-up**: surface harness scheduling diagnostic to user — RemoteTrigger introspection vs runs.log over the 04-23 → 05-01 window to identify root cause of journal-commit failures.
