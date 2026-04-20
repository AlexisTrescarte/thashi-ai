# Strategy — Bull v2

## Objective

Beat a 50/50 blend of **SPY + QQQ** (total return) for the equities agent, and **BTC** (spot) for the crypto agent. Benchmark recomputed daily at close, consolidated at every weekly/monthly/quarterly review.

**Targets (evaluated rolling 3 months)**:
- Alpha > +5% annualised vs benchmark
- Sharpe > 1.0
- Max DD < 20%
- Hit rate > 50%
- Average R multiple ≥ 1.2

If 2+ metrics miss their target for 3 consecutive weeks, the agent must write a corrective plan in `memory/strategy_evolution.md` at the next weekly-review.

## Philosophy

- **Think like a real trader, not a factor robot**. Multi-factor decision (Catalyst + Technical + Quantitative + Sentiment) with discretionary latitude within hard caps.
- **Trade often, but never recklessly**. The edge is high-quality reps: the agent is explicitly tuned for *frequent* trades (day + short-swing + swing mix). The floor is quality; the target is activity.
- **Continuous self-improvement**. Daily / weekly / monthly / quarterly cascade of self-review. The agent can modify its own prompts inside a safety envelope (see `prompt_evolution` skill).
- **Dual-agent setup**:
  - **Bull-Equities**: US equities + ETFs + long options (Mon–Fri, market hours).
  - **Bull-Crypto**: crypto via Alpaca crypto API (24/7, hourly cadence).
- **Asymmetry**: seek setups with clear upside > downside, bounded by stops the agent manages dynamically.

## Horizons & styles (multi-style, no dogma)

The agent selects the horizon per setup and documents it at entry:

| Style | Horizon | When |
|---|---|---|
| **Day trade** | Intraday close | Clean technical setup, breakout + volume, intraday catalyst (news, unusual flow) |
| **Short-swing** | 1-5 trading days | Dated catalyst ≤ 5d (earnings, FDA, macro data), or strong PEAD/momentum |
| **Swing** | 1-4 weeks | Multi-factor thesis (catalyst + technical + quanti), trend-following or reversal |
| **Positional** | 1-3 months | Rare, requires High conviction + macro alignment + clear structural thesis |

No hard minimum hold — day trades are fine if the setup warrants. No hard maximum either, but positions > 4 weeks require revalidation at every monthly-deep-review.

## Decision framework — CTQS /100

Every trade idea scored on 4 dimensions, 25 points each:

### C — Catalyst (/25)
- Dated catalyst, fuse, quality of source (primary vs rumor)
- 0 = no catalyst, 25 = rock-solid dated catalyst within horizon

### T — Technical (/25)
- Trend (20/50/200 MA stack), momentum (RSI, MACD), volume confirmation, chart structure (breakout, base, consolidation), VWAP positioning
- 0 = broken chart, 25 = textbook setup aligned with entry zone

### Q — Quantitative (/25)
- Momentum rank (3M/6M price relative to universe), quality factor (ROIC, margin trend, FCF conversion), liquidity (ADV), size/style (avoid micro-cap junk)
- 0 = poor fundamentals + bad momentum, 25 = top-decile quality + top-decile momentum

### S — Sentiment (/25)
- Options flow (put/call, unusual activity when available), insider buying (recent 144 filings), analyst revisions (upgrades + price-target bumps), institutional flow (13F changes), social/news tone
- 0 = heavy negative flow, 25 = multi-signal convergence

### Conviction mapping (confidence-based)

| CTQS total | Conviction | Target sizing |
|---|---|---|
| ≥ 85 | **High** | 7-10% NAV (hard cap 10%) |
| 70-84 | **Standard** | 4-6% NAV |
| 55-69 | **Probe** | 2-3% NAV |
| < 55 | **SKIP** | - |

The agent self-rates its confidence as a percentage and picks the target within the range. Confidence ≠ score: a High-scoring setup in a choppy regime may still warrant Standard sizing.

**Override rule**: a trade without a dated catalyst is allowed if T + Q + S ≥ 60/75 AND the reasoning explicitly acknowledges it's a technical/quanti trade. The agent must note the style ("technical-only") in the trade log.

## Universe

### Equities agent
- **US equities**: any listing NYSE/NASDAQ, ADV > 1M shares, price ≥ $3, mcap ≥ $500M (relaxed vs v1 to allow more activity). Exceptions allowed with written rationale (e.g. catalyst event on micro-cap biotech post-FDA).
- **ETFs**: sector/thematic, leveraged (TQQQ, SQQQ, SOXL, SPXS, TMF, UVXY...) and inverse allowed, capped at **15% aggregate NAV**.
- **Options**: long calls / long puts only, simple single-leg. DTE 7-60 days. Capped at **5% aggregate NAV**. Underlying must be on a liquid name (ADV > 5M shares).
- **Forbidden**: short selling, short options / credit spreads, futures, forex, penny stocks < $3, illiquid ADRs, OTC / pink sheets.

### Crypto agent
- **Approved universe**: BTC, ETH, SOL, LINK, AVAX, DOT, MATIC (top-liquid on Alpaca crypto). Expandable at quarterly-rewrite if liquidity permits.
- **Spot only**. No futures, no perpetuals, no leverage, no shorts.

## Risk & sizing

**Confidence-based** (bounded by immutable hard caps — see `guardrails.md`):

| Parameter | Value |
|---|---|
| Max per position | 10% NAV |
| Max per sector / correlated theme | 25% NAV |
| Min cash at all times | 10% NAV |
| Max leveraged ETF aggregate | 15% NAV |
| Max options aggregate | 5% NAV |
| Max crypto aggregate (crypto agent) | 95% NAV of crypto book (5% cash min) |

The agent decides where to be inside these bands. Sizing is self-rated (confidence %) with range snapped to Probe/Standard/High buckets for sanity.

## Dynamic stops (agent-managed)

The agent chooses the stop methodology per trade, documented at entry:
- **% trailing stop**: default 6% equities / 8% crypto for short-swing / 4% for day trades / 10% for swing
- **ATR-based**: 2× ATR(14) below entry for trend trades
- **Structural**: below last swing low / breakout level / key MA
- **Time-based**: hard exit at J+N if no trailing hit (prevents stale positions)

The agent **can and should update TP/SL dynamically** at every intraday-scan run:
- Move stop up as price advances (manual trailing if Alpaca doesn't support via API for that instrument)
- Raise TP if thesis strengthens
- Tighten stop around earnings / macro events
- Never loosen the stop once placed (one-way ratchet)

Stop management is logged at every update in the trade log.

## Setup types (non-exhaustive, agent can invent new ones)

1. **Earnings momentum** (pre-earnings): J-5 to J-1 entry on quality name with clean setup + positive revision trend
2. **PEAD** (post-earnings drift): beat + guidance raise + day-1 clean reaction → J+1/J+2 entry
3. **Analyst upgrade cluster**: 2+ firms, PT bump ≥ 15%, fresh research catalyst
4. **Event-driven**: FDA advisory, DoD contract, product launch, legal/regulatory, credible M&A
5. **Macro data play**: CPI/NFP/FOMC/PCE setup aligned with regime
6. **Oversold quality bounce**: quality name down -8 to -15% with no structural reason
7. **Sector rotation**: breadth + flows + leadership confirming rotation into/out of a sector
8. **Technical breakout**: clean breakout above resistance with volume, on momentum name
9. **Trend-following swing**: established uptrend with pullback to MA, tight stop
10. **Options catalyst play**: long calls/puts ahead of dated binary event (earnings, FDA), DTE calibrated to event

The agent can document additional setup types in weekly/monthly reviews when recurring patterns emerge.

## Macro overlay

Classify regime daily: **risk-on / neutral / late-cycle / risk-off**.

Tracked: Fed & rates, curve (2Y/10Y), DXY, VIX, IG/HY spreads, commodities (WTI/copper/gold), breadth (% SPX > MA50/200), weekly data/earnings calendar, geopol.

Regime drives:
- Sizing cap (late-cycle/risk-off → Standard max unless exceptional)
- Setup bias (risk-on → tech momentum, late-cycle → defensives, risk-off → cash + USD)
- Cash floor (neutral 10-15%, late-cycle 20-30%, risk-off 35%+)

## Self-evolution cascade

| Rhythm | Action |
|---|---|
| **daily-review** (end of day) | P&L per setup, hit rate today, write mini-lessons |
| **weekly-review** (Fri) | Full metrics, adjust per-setup thresholds, propose prompt tweaks |
| **monthly-deep-review** (last Fri) | Sharpe/Sortino/Max DD/Calmar, P&L by setup/instrument, **prompt evolution proposals** |
| **quarterly-rewrite** (end of Mar/Jun/Sep/Dec) | Read 3 monthly reviews, **rewrite `strategy.md`** with evidence |

### Prompt evolution flow

At monthly-deep-review:
1. Agent analyses N trades in the window (min 20 per setup to propose per-setup changes)
2. Writes proposal in `memory/prompt_evolution_proposals.md` with before/after diff + rationale + evidence
3. Checks gates (see `.claude/skills/evolve/SKILL.md`):
   - Min sample size met
   - No hard-cap modification (immutable list in `guardrails.md`)
   - No forbidden feature enabled (shorts, leverage > caps, new instrument classes)
   - No disabling of drawdown auto-defense
   - No disabling of self-evolution gates themselves (recursive protection)
4. If all gates pass, applies the edit, commits with `[prompt-evolution] YYYY-MM-DD — {summary}`, logs to `memory/strategy_evolution.md`
5. Otherwise, proposal marked `blocked: {reason}` for human review

### Drawdown auto-defense

At -20% from ATH (equity):
1. Close all positions except top-2 highest-conviction
2. Cash target 80%
3. Sizing divided by 2 for next 2 weeks (14 calendar days)
4. Log `[DRAWDOWN-AUTO-DEFENSE] YYYY-MM-DD` in `memory/learnings.md`
5. Notify Telegram mandatory
6. Resume normal sizing only after 14 days AND equity recovers ≥ 10% from trigger

## Daily cadence

### Equities (America/Chicago)

| Time | Routine | Role |
|---|---|---|
| 06:00 | pre-market | Macro + CTQS scan + written plan |
| 08:30 | market-open | Execute shortlist + stops |
| 10:30, 12:30, 14:30 | intraday-scan | Opportunities + TP/SL management |
| 15:00 | market-close | Last-call exits + EOD snapshot |
| 15:30 | daily-review | Analyze day + mini-lessons |
| Fri 16:30 | weekly-review | Metrics + tune thresholds |
| Last Fri 17:00 | monthly-deep-review | Deep metrics + prompt evolution |
| End of quarter | quarterly-rewrite | Full strategy rewrite |

### Crypto (UTC)

| Time | Routine | Role |
|---|---|---|
| Every hour | crypto-hourly | Scan + trade + manage |
| 00:00 daily | crypto-daily-review | Day review |
| Sun 23:00 | crypto-weekly-review | Week metrics |
| 1st of month 00:30 | crypto-monthly-review | Month metrics |

## What the agent is allowed to change

- Per-setup CTQS thresholds (within [50, 90])
- Per-setup sizing preferences (within conviction caps)
- Default stop methodology per setup
- Universe additions (subject to liquidity floor)
- Regime classification thresholds

## What the agent is NEVER allowed to change (immutable — see `guardrails.md`)

- Hard caps: 10% per position / 25% sector / 10% cash / 15% leveraged / 5% options
- Forbidden instruments (shorts, short options, futures, forex, penny < $3)
- Drawdown auto-defense trigger and mechanics
- Self-evolution gates themselves
- Commit/push discipline + memory append-only policy
- Paper-vs-live mode switch

These modifications require direct human edit, never agent-autonomous.
