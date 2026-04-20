---
name: research
description: Institutional multi-factor research using the CTQS framework (Catalyst + Technical + Quantitative + Sentiment, /100). Works for equities, ETFs, long options, and crypto. Produces BUY / WATCH / SKIP / AVOID verdict with explicit sizing target. Invoke from pre-market, intraday-scan, and crypto-hourly.
---

# Skill: research

Produce a research note using the **CTQS /100** framework. You play a senior analyst at a multi-strat hedge fund — the note must stand up to a demanding PM across multiple horizons (day / short-swing / swing / positional).

> You are a **discretionary trader with a systematic scorecard**. The score bounds your conviction, the narrative explains why the score is valid, the plan is executable at the next run.

## Scope

One ticker/symbol per note. If screening multiple, produce multiple notes.

Works for:
- **Equities / ETFs / leveraged ETFs** (use benchmark = SPY+QQQ blend)
- **Long options** (add DTE + Greeks + underlying CTQS)
- **Crypto** (BTC, ETH, SOL, LINK, AVAX, DOT, MATIC — use benchmark = BTC)

## Steps

1. **Gather primary sources** (min 2) with `WebSearch` + `WebFetch`:
   - Equities: IR pages, 8-K/10-Q, earnings call transcripts, FDA/DoD calendars, CME FedWatch, FRED
   - Options: underlying data (spot, IV, term structure), option chain (bid/ask, OI, volume), earnings calendar
   - Crypto: on-chain (Glassnode-style metrics via public), exchange news, whitepapers, CoinGecko fundamentals
2. **Complement** with 1-2 quality tertiary sources (Bloomberg/Reuters/WSJ/FT/Barron's for equities; The Block/CoinDesk for crypto).
3. **Score CTQS** (4 dimensions, 25 each = /100).
4. **Run valuation red-flag** (for equities) or **technical-structure sanity** (for crypto).
5. **Write scenarios** over the chosen horizon (bull / base / bear).
6. **Filter against guardrails** (universe, concentration, revenge trade, caps, auto-defense).
7. **Append** to `memory/{agent}/research_log.md` with ISO UTC timestamp and clear verdict.

## CTQS scoring rubric

### C — Catalyst (/25)

| Points | Signal |
|---|---|
| 20-25 | Primary-source dated catalyst within horizon (earnings date, FDA PDUFA, FOMC, DoD announce, product launch) |
| 15-19 | Secondary but credible catalyst (analyst cluster, strong PEAD setup, crypto upgrade, sector rotation confirmed) |
| 10-14 | Narrative catalyst without hard date (theme in vogue, sector flows) |
| 5-9 | Weak / stale catalyst |
| 0-4 | None |

### T — Technical (/25)

| Points | Signal |
|---|---|
| 20-25 | Clean structure (trend intact, MA stack aligned 20>50>200 or well-defined base), volume confirming, RSI 40-70, price near entry zone |
| 15-19 | Decent setup, 1 minor flag (RSI > 70 or volume lighter, still reasonable) |
| 10-14 | Choppy but tradeable (range, pre-breakout wedge) |
| 5-9 | Broken trend, below key MAs, weak volume |
| 0-4 | Downtrend + high volume selling |

### Q — Quantitative (/25)

| Points | Signal |
|---|---|
| 20-25 | Top-decile momentum (3M > +15% relative) + strong quality (ROIC > 15%, clean balance sheet) + liquid (ADV > 5M eq / top-5 crypto) |
| 15-19 | Good momentum + decent quality, liquid enough |
| 10-14 | Mixed (either momentum OR quality, not both) |
| 5-9 | Weak on both axes |
| 0-4 | Negative momentum + weak fundamentals |

### S — Sentiment (/25)

| Points | Signal |
|---|---|
| 20-25 | Multi-signal convergence: bullish options flow + insider buying + analyst upgrades + institutional flow positive |
| 15-19 | 2 of 4 signals positive |
| 10-14 | 1 signal positive, neutral elsewhere |
| 5-9 | Neutral to slightly negative |
| 0-4 | Heavy negative (insider selling + downgrades + outflows) |

**Total /100** → conviction:
- ≥ 85 → **High** (sizing 7-10%)
- 70-84 → **Standard** (4-6%)
- 55-69 → **Probe** (2-3%)
- < 55 → **SKIP** (no BUY)

**Exception** — technical-only trade: if C < 10 but T+Q+S ≥ 60/75, allowed as a technical trade, capped at Standard sizing.

## Note template (follow strictly)

```markdown
### YYYY-MM-DDTHH:MM:SSZ — {SYMBOL} {Short name} — {VERDICT}

**Instrument**: {equity | ETF | leveraged-ETF | option (call/put, strike, DTE) | crypto}
**Style**: {day | short-swing | swing | positional}
**Target horizon**: {exit window, e.g. 2-5 trading days}
**Conviction**: {Probe / Standard / High} — confidence {xx}%
**Proposed sizing**: {x.x}% NAV

#### 1. Snapshot
- Price: ${X} | Mcap/marketcap: $X | Sector: X | ADV: X | Beta: X
- Key fundamentals (equity): EPS growth YoY X%, revenue growth YoY X%, gross margin X%, ROIC X%
- Next earnings / major event: {date + BMO/AMC / pre-event window}
- (Option): underlying $X, strike $X, DTE X, IV X%, OI X
- (Crypto): BTC dominance X%, funding / open interest proxy, on-chain key metric

#### 2. Thesis (3-5 lines)
What has to happen within {horizon} for this trade to pay off?

#### 3. CTQS Score (/100)

| Axis | Score /25 | Justification |
|---|---|---|
| C — Catalyst | X | {dated event / narrative} |
| T — Technical | X | {trend, MA, RSI, volume, key levels} |
| Q — Quantitative | X | {momentum rank, quality factor, liquidity} |
| S — Sentiment | X | {options flow, insider, analyst, flow} |
| **Total** | **X/100** | → Conviction {Probe/Standard/High} |

#### 4. Valuation red-flag (equities only) / Structure sanity (crypto)
- Equity: Fwd P/E {X} vs sector {Y} — red flag yes/no
- Crypto: vs trend (above/below key MAs), vs BTC, vs sector leader

#### 5. Scenarios ({horizon} window)
- **Bull** ({+X%}): {assumptions}
- **Base** ({+X%}): {assumptions}
- **Bear** ({-X%}): {triggers}

#### 6. Specific risks
- Risk 1
- Risk 2
- Risk 3 (if any)

#### 7. Macro alignment
- Regime: {risk-on / neutral / late-cycle / risk-off}
- Events in window: {FOMC / CPI / NFP / earnings cluster / ...}
- Compatible: {yes / partial / against-regime — justify}

#### 8. Execution plan
- **Entry zone**: ${X}-${Y} (skip above + {2}% = ${Z})
- **Sizing**: {x.x}% NAV ({Probe / Standard / High})
- **Stop type**: {% trailing / ATR / structural / time} — level: {X}
- **Take-profit target**: ${X} or "trailing only"
- **Time stop**: {date or n/a}
- **Earnings hold**: {yes + rationale / no}
- **Stop-update policy**: how to tighten at each intraday-scan (e.g. "if +5%, move stop to BE; if +10%, trailing 3%")

#### 9. Sources (min 2 primary)
- {url 1} (primary)
- {url 2} (primary)
- {url 3} (tertiary)

#### 10. Verdict
**{BUY | WATCH | SKIP | AVOID}** — 1-sentence summary.
```

## Verdicts

- **BUY**: executable at next market-open (equities) / next crypto-hourly (crypto) / next intraday-scan (opportunistic)
- **WATCH**: valid setup, entry not ripe (price too high, catalyst too far, regime to confirm)
- **SKIP**: fails a criterion (score < 55 and no technical-only path, guardrail violation, revenge trade)
- **AVOID**: structural red flag (fraud flag, regulatory halt risk, broken balance sheet, liquidity collapse)

## Anti-bias checklist

- Does the **score breakdown** match the numbers (not inflated to hit a threshold)?
- If C < 10, did I explicitly mark this as a technical-only trade (capped at Standard)?
- Does the thesis hold **without looking at the price**?
- Can I cite a **precise number** from a primary source?
- Is this a **revenge trade** (cut < 5 trading days ago without "re-entry justified")?
- Am I respecting concentration (sector ≤ 25%, correlated theme ≤ 4 names)?
- Did I pick the **right horizon** for this setup, not the one that rationalizes holding?
- Is my stop methodology **documented** with a specific level, not vague?
- For options: DTE ≥ 7, aggregated options ≤ 5% NAV?
- For leveraged ETFs: aggregated ≤ 15% NAV?
- For crypto: single coin ≤ 40% of crypto book, aggregate ≥ 5% cash?

## Output

Append to `memory/{agent}/research_log.md`. The parent command decides Telegram notifications — not the research skill.
