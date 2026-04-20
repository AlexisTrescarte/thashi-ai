---
name: research
description: Short-horizon institutional research (Goldman/Morgan Stanley-grade rigor, 1-5 trading day horizon) with dated catalyst, quality light score, light valuation, short-window scenarios, execution plan. Verdict BUY / WATCH / SKIP / AVOID. Invoke at each pre-market or on demand.
---

# Skill: research

Produce a research note matching the schema of `memory/research_log.md`. You play a senior analyst at an event-driven hedge fund — the note must stand up to a demanding PM, **but calibrated to short-swing (1-5 trading days)**, not to a long-term hold.

> You write for a short-horizon PM. Dated catalyst + coherent macro + clean setup = a note that matters. No 10-year DCF here: what matters at this horizon is flow, catalyst, and the skew of the setup.

## Steps

1. **Scope** the work: single ticker or thematic shortlist (max 5 tickers to screen individually).

2. **Gather primary sources** (minimum 2) with `WebSearch` then `WebFetch`:
   - Investor relations (latest earnings release, recent 8-Ks, presentations)
   - Earnings call transcripts (SeekingAlpha, Motley Fool, direct IR)
   - Official filings (FDA, DoD, SEC filings 13D/13G, 8-K)
   - Catalyst calendars (Earnings Whispers, IR calendars, FDA advisory calendar)
   - Macro data: FRED (yields, CPI, unemployment), EIA (energy), CME FedWatch.

3. **Complement** with 1-2 quality tertiary sources (Bloomberg, Reuters, WSJ, FT, Barron's). Never forums/Twitter as primary source.

4. **Synthesize** with the template below (disciplined, compact, clear verdict).

5. **Filter against strategy and guardrails**:
   - Universe compliance (US-listed, volume > 2M, price ≥ $5, mcap ≥ $2B unless documented exception).
   - Quality light score ≥ conviction threshold (Probe 18 / Standard 22 / High 26).
   - **Dated catalyst ≤ 5 trading days** (mandatory for BUY).
   - Macro regime alignment OK, or deviation justified.
   - Not a revenge trade (check `trade_log.md` over last 5 trading days).
   - At least 2 of the 3 key signals (catalyst fuse, quality floor, technical setup).

6. **Append** to `memory/research_log.md` with ISO UTC timestamp.

## Note template (follow strictly)

```markdown
### {YYYY-MM-DDTHH:MM:SSZ} — {TICKER} {Short name} — {VERDICT}

**Setup type**: {Pre-earnings momentum / PEAD / Analyst upgrade / Event-driven / Macro data play / Oversold bounce / Sector rotation}
**Target horizon**: {typical 2-5 trading days, latest exit J+8}
**Conviction**: Probe 2% / Standard 4% / High 5%

#### 1. Snapshot (numbers)
- Price: $X | MCap: $XB | Sector: X | ADV: X M shares | Beta: X
- EPS growth YoY: X% | Revenue growth YoY: X% | Gross margin: X%
- Next earnings: {date + BMO/AMC} — {HOLD through earnings? yes/no}

#### 2. Thesis (3-5 lines)
What has to happen within 1-5 days for this trade to pay off? What flow / narrative / repricing do we expect?

#### 3. Catalyst(s) — fuse ≤ 5 days
- {Event} — {precise date} — source
- Why is the market **not yet** correctly pricing this catalyst?

#### 4. Quality Light Score (/30)
| Dimension | Score /10 | Justification |
|---|---|---|
| Catalyst clarity & fuse | X | precise date, known downside if missed |
| Quality floor | X | decent moat / clean balance sheet / positive earnings growth |
| Technical setup & liquidity | X | ADV > 2M, clean trend/base, RSI < 80, no >5% gap |
| **Total** | **X/30** | |

#### 5. Valuation (red flag check only)
- Fwd P/E: X (sector median X)
- Growth YoY: X%
- Red flag? (Fwd P/E > 2× median with no growth): yes / no

#### 6. Scenarios (2-5 day window)
- **Bull**: +X% (e.g. +12%) if catalyst plays as expected — assumptions: …
- **Base**: +X% (e.g. +5%)
- **Bear**: -X% (e.g. -5%, stop triggers) — assumptions: …

#### 7. Specific risks
- Risk 1 (e.g. adverse macro data in the window)
- Risk 2 (e.g. major peer's earnings in the window)
- …

#### 8. Macro alignment
- Current regime: {risk-on / neutral / late-cycle / risk-off}
- Macro events in the trade window: {FOMC J+2, CPI J+3, …}
- Compatible: **yes / partial / against-regime** — justification

#### 9. Execution plan
- **Entry zone**: $X-$Y (do not chase above, skip if > +2% vs plan)
- **Sizing**: Probe 2% / Standard 4% / High 5%
- **Initial trailing stop**: 6%
- **Hard cut**: -5% unrealized at midday
- **Tighten**: at +10% → stop 3%
- **Trim 50%**: at +15%
- **Time stop**: forced exit at J+8 if no trailing hit
- **Earnings hold?**: no (default) / yes (explicit rationale)

#### 10. Sources
- {url 1} (primary)
- {url 2} (primary)
- {url 3}

#### 11. Verdict
**BUY / WATCH / SKIP / AVOID** — 1-sentence summary.
```

## Possible verdicts

- **BUY**: new position executable at the next `market-open`. Dated catalyst ≤ 5 days, score ≥ threshold, macro OK.
- **WATCH**: valid setup but entry or timing not ready yet (price too high, catalyst J+6, regime to confirm). Re-check at next pre-market.
- **SKIP**: fails a key criterion (score too low, no dated short catalyst, against-regime without justification, revenge trade).
- **AVOID**: structural red flag (broken balance sheet, fraud flags, heavy regulation, halt risk). Don't touch.

## Anti-bias checklist

- Does the **catalyst** have a **precise date** within ≤ 5 trading days? (If not = SKIP or WATCH)
- Do I know **why this trade resolves in 1-5 days** rather than "someday"? (If not = no short-swing thesis)
- Does the thesis hold without looking at the price? (If not = FOMO)
- Can I cite a **precise number** from a primary document? (If not = rumor)
- Is the ticker absent from positions cut in the last 5 trading days? (If not = revenge trade)
- Do I have **at least 2 primary sources**?
- Does the setup survive VIX +20% intraday during the window? (light stress test)
- Did I verify that **no earnings on the position** falls inside my window without an explicit plan?

## Output

Append to `memory/research_log.md`. **Do not** produce a Telegram message — that's the parent slash command's job (pre-market only notifies on urgency for an open position).
