# Strategy — Bull

## Objective

Beat the **SPY** (total return). Benchmark recomputed every `market-close`, consolidated each `weekly-review`.

## Philosophy

- **Catalyst-driven short-swing**. The edge comes from intelligence (macro + catalyst + fundamentals + momentum) applied to setups **that play out within a few days**.
- **Target holding horizon per trade: 1 to 5 trading days** (base case). Exceptional extension up to **10 trading days** if the thesis keeps delivering and the runner gives a clear signal.
- **No day-trading, no intraday scalping**. Overnight hold is mandatory, but exit fast once the catalyst is digested or the stop is hit.
- **Multi-positions in parallel assumed**. Target 8-15 active positions to diversify catalysts — not 3 massive convictions.
- **Conviction over activity, but activity > 0**. Better 0 trade than a bad one, but natural turnover is high (positions rotate in 3-5 days).
- **Asymmetry**: setups with +8 to +20% upside within a few days, -5% max thanks to tight stop.

## Macro overlay (mandatory at every pre-market and weekly-review)

Classify the regime among: **risk-on / neutral / late-cycle / risk-off**.

**Signals to track**:
- **Fed & rates**: Fed funds expectations (CME FedWatch), latest FOMC speech, upcoming FOMC, Fed speakers this week.
- **Yield curve**: 2Y, 10Y, 2-10 spread.
- **Dollar**: DXY direction.
- **Volatility & credit**: VIX (<15 complacent / 15-25 normal / >25 stress), IG/HY spreads.
- **Commodities**: WTI, copper, gold.
- **Breadth**: % S&P > MA50 / MA200, sector leadership.
- **Weekly macro calendar**: CPI / PPI / NFP / PCE / FOMC / Powell / Jackson Hole / jobless claims, etc.
- **Geopol & policy**: tariffs, China, Middle East, elections, regulation (antitrust, FDA, export controls), shutdown risk.

**Rule**: every new setup must be **compatible** with the current regime, or carry explicit justification against the regime (hedge / very strong idiosyncratic catalyst).

## Setup universe we play

We look for **short-fuse catalysts (≤ 5 trading days)**:

1. **Pre-earnings momentum**: entry 1-5 days before an earnings print from a quality name with tailwind + estimate raise + positive whisper + clean technical setup. Decide to hold or exit **the day before** earnings (no blind earnings hold unless explicitly noted).
2. **Post-earnings drift (PEAD)**: beat + guidance raise + positive day-1 reaction → entry J+1 or J+2, exit within 5 days.
3. **Multi-source analyst upgrade** with new price target +15%+ on high conviction → entry J+0/J+1, exit within 3-5 days.
4. **Event-driven**: FDA advisory, DoD contract win, product launch, legal/regulatory ruling, credible sourced M&A rumor.
5. **Macro data play**: setup aligned with regime on CPI/NFP/FOMC (e.g. yields cracking → long duration-sensitive growth), 1-3 day window.
6. **Oversold bounce on quality**: quality stock (decent quality floor) down -8% to -15% with no structural idiosyncratic reason → 2-4 day bounce trade.
7. **Confirmed sector rotation**: breadth data + flows + leadership flipping (e.g. XLE leading on oil spike) → 3-5 day swing on sector leaders.

## Selection framework (Quality Light Score — short-horizon adapted)

Each new thesis scored /30 in `research_log.md`:

1. **Catalyst clarity & fuse** (0-10): **dated and precise** catalyst, triggers ≤ 5 days, downside known if catalyst fails.
2. **Quality floor** (0-10): decent moat OR clean balance sheet OR positive earnings growth (not required to have all three — but no dogs). Avoid existential-risk names: short horizon does not protect from gap-down fraud/guidance disasters.
3. **Technical setup & liquidity** (0-10): average daily volume > 2M, clean trend or base, RSI not > 80, no >5% pre-market gap we'd be chasing.

- Probe (2%): ≥ 18/30.
- Standard (4%): ≥ 22/30.
- High conviction (5%): ≥ 26/30 + strong catalyst + macro aligned.

## Valuation (light, not blocking at short horizon)

- **Red flag** only: P/E fwd > 2× sector median AND no growth to justify it → skip unless exceptional catalyst.
- No DCF on short-swing: at this horizon what prices the stock is flow and catalyst, not terminal cash flows.

## Exit signals

- **Trailing stop 6%** placed at entry (default, short-horizon adapted).
- **Cut -5%**: any position ≤ -5% unrealized at midday check.
- **Tighten trailing to 3%** when position ≥ +10% unrealized.
- **Trim 50%** when position ≥ +15%, tighten 3% on the rest.
- **Let winners run**: if a position moves > +20% with momentum, stop at 3% but keep the rest until trailing hits.
- **Time stop**: any position held > 8 trading days with no remaining active catalyst → **auto-close** at next midday or close. Short-swing shouldn't become a bad long-term through laziness.
- **Thesis broken**: exit immediately regardless of P&L.
- **Regime shift**: regime flips to violent risk-off (VIX > 30, hawkish Fed surprise, credit event) → raise cash to 30%+, tighten all stops, skip new opens.

## Target allocation

- **Catalyst book** (70-85%): 8-15 parallel positions, each on a short catalyst, average duration 3-5 days.
- **Cash** (≥ 10%, target 15-20% neutral, 25-35% late-cycle/risk-off): dry powder for setups that emerge mid-week.

No "core long-term" bucket in this setup — the agent lives on rotations. If a genuine buy & hold emerges, it's out-of-system (human call).

## Sizing by conviction (at entry)

- **Probe** (~2% portfolio): interesting setup, medium conviction, first test.
- **Standard** (~4%): solid setup, score ≥ 22/30, clear catalyst.
- **High conviction** (~5%, guardrail cap): score ≥ 26/30, strong catalyst, macro aligned.
- **Top-up forbidden** on short-swing (a position is sized at entry or not — no averaging up on a 1-5 day trade).

## Daily cadence

- **Pre-market (06:00 CT)**: macro overlay + short-catalyst scan (earnings today, events this week) + 2-5 ideas. Written to `research_log.md`.
- **Open (08:30 CT = 09:30 ET)**: execute today's `BUY` ideas. Parallel multi-positions OK.
- **Midday (12:00 CT)**: cut -5%, tighten +10%, trim +15%, time stop > 8 days, check thesis on violent movers.
- **Close (15:00 CT)**: snapshot + macro + alpha vs SPY + stale positions watchlist.
- **Weekly (Friday 16:00 CT)**: hit rate, avg holding days, P&L by setup type, macro outlook next week, earnings calendar next week.

## Iteration

Each `weekly-review` may propose adjustments. Any change to `strategy.md` or `guardrails.md` requires written justification in `weekly_review.md` + dedicated commit `[strategy] …`.
