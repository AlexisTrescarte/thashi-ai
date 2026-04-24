# Guardrails — inviolable rules

These rules override any decision. If an action would violate a rule, **you do not act** and you log the situation in `memory/learnings.md`. We operate in a multi-style regime (day + short-swing + swing + occasional positional), multi-instrument (equities, ETFs, long options, crypto majors BTC/ETH/SOL) — single agent during US market hours.

## Immutable hard caps (NEVER modifiable by the agent)

The following caps are **immutable**: the agent cannot modify this file to loosen them, cannot override them via prompt evolution, cannot bypass them via creative accounting. They exist to prevent catastrophic self-modification.

| Cap | Value |
|---|---|
| **Max per position** (single ticker/symbol, incl. single coin) | 10% of NAV |
| **Max per sector / correlated theme** | 25% of NAV |
| **Min cash at all times** | 10% of NAV |
| **Max leveraged ETF aggregate** | 15% of NAV |
| **Max options aggregate premium** | 5% of NAV |
| **Max crypto aggregate** (BTC + ETH + SOL combined) | 15% of NAV |
| **Max new positions per day** | 10 |
| **Max new positions per week** | 30 |
| **Max concurrent positions** | 30 |
| **Daily loss cap** → pause opens J+1 | -4% NAV |
| **Weekly loss cap** → 3-day pause | -8% NAV |
| **Drawdown cap from ATH** → auto-defense mode | -20% NAV |

A change to any cap above requires direct human edit of this file. The agent must refuse any self-modification proposal that touches this section.

## Drawdown auto-defense (immutable mechanism)

At -20% drawdown from ATH:
1. Immediately close all positions except top-2 highest-conviction (by CTQS score at entry)
2. Raise cash to 80%+ of NAV
3. Sizing is automatically divided by 2 for the next 14 calendar days
4. Append `[DRAWDOWN-AUTO-DEFENSE] YYYY-MM-DDTHH:MM:SSZ — equity $X, ATH $Y, DD -X.X%` to `memory/learnings.md`
5. Mandatory Telegram notification
6. Normal sizing only resumes after **both**: 14 calendar days elapsed **and** equity recovers ≥ +10% from auto-defense trigger

The agent cannot disable, delay, or adjust this mechanism.

## Forbidden instruments (immutable)

- **Short selling** equities (any form)
- **Short options** (covered calls, cash-secured puts, credit spreads, naked options)
- **Futures** (equity, commodity, crypto, forex)
- **Forex pairs**
- **Penny stocks** < $3 share price
- **OTC / pink sheets** tickers
- **Illiquid ADRs** (ADV < 500k)
- **Crypto perpetuals / margin / leverage** (spot only)
- **Crypto alts outside approved list** (immutable list: **BTC, ETH, SOL** — expandable only via human edit of this file)

## Investment universe (modifiable within the floor below, immutable floor)

### Equities

- US-listed (NYSE, NASDAQ)
- **Liquidity floor** (immutable): ADV > 1M shares, price ≥ $3, mcap ≥ $500M
  - Exception path: documented catalyst event in research note + flagged "low-liquidity exception" with size capped at Probe (≤ 3%)
- Classic ETFs (SPY, QQQ, IWM, sector) + leveraged/inverse ETFs (within 15% cap)

### Options

- Long calls / long puts only, simple single-leg
- Underlying: ADV > 5M shares (liquid listed)
- DTE: 7-60 days (no weeklies < 7DTE, no LEAPS)
- Aggregate premium ≤ 5% NAV
- **Spreads/short premium forbidden** (immutable)

### Crypto (inside the equities routines)

- **BTC, ETH, SOL** only (immutable list)
- Spot only via Alpaca crypto API
- Aggregate crypto exposure ≤ **15% NAV** (immutable cap)
- Single-coin cap 10% NAV (same as per-position cap)
- Scanned/managed only during US market hours; Alpaca native trailing stops handle overnight + weekend risk

## Sizing — confidence-based within bands

The agent self-rates confidence per idea and picks sizing within the conviction band:

| CTQS score | Conviction | Sizing range | Hard cap |
|---|---|---|---|
| ≥ 85 | High | 7-10% | 10% |
| 70-84 | Standard | 4-6% | 6% |
| 55-69 | Probe | 2-3% | 3% |
| < 55 | SKIP | - | - |

**ADD / top-up on existing position**: allowed only if (a) original position < 50% of max cap AND (b) new dated catalyst distinct from original AND (c) post-ADD position ≤ hard cap for that conviction tier AND (d) combined sizing still ≤ 10% per-position absolute hard cap. Documented in trade log as "ADD justified by {new catalyst}".

## Concentration

- No sector > 25% NAV (technology included, mega-cap tech counts as one sector)
- No more than 5 positions exposed to the same single event (e.g. max 5 names on FOMC Wednesday)
- Correlated-theme concentration: at most 4 highly-correlated names (e.g. 4 semis = OK, 5 = flag at next review, 6 = refuse new buy)

## Stops (the agent chooses methodology, but mandatory)

- **Every new position MUST have a stop** placed within 5 minutes of fill (trailing %, stop-market, or documented manual-trailing schedule at next intraday-scan if Alpaca doesn't support for that instrument).
- **Options positions**: hard time stop at DTE - 3 (never let option decay to worthless), hard price stop at -50% premium.
- **Crypto**: native trailing stop % via Alpaca crypto API (strongly preferred — stop executes 24/7 while the agent is asleep). If native unsupported for a given symbol, skip the buy entirely — no manual-trailing backup since the agent only wakes during US hours.
- **One-way ratchet**: once a stop is moved up (closer to price), it cannot be moved down.

## Exit triggers (must check at every run)

- **Thesis broken** (guidance cut, fraud, halt, FDA reject, contract loss, C-suite resign) → CUT immediately, ignore P&L
- **Stop hit** → executed by Alpaca if trailing, or manually if not
- **Time stop** exceeded (per entry plan) → CUT at next run
- **Pre-earnings exit** (if no explicit "earnings hold" in entry thesis) → CUT day before earnings
- **Take-profit target hit** (agent-defined at entry) → CUT or TRIM per plan
- **Regime shift** (VIX +30% intraday, credit event, hawkish Fed surprise) → tighten all stops to 3%, halt new opens

## Daily / weekly / drawdown caps

| Event | Action |
|---|---|
| Day equity ≤ -4% | Pause opens for J+1. Tighten all stops to 4%. Log `[DAILY-LOSS-CAP]` in learnings. |
| Week equity ≤ -8% | Pause opens for next 3 trading days. Raise cash to 30%+. Log `[WEEKLY-LOSS-CAP]`. |
| Drawdown ≥ -20% from ATH | Trigger auto-defense mechanism (see above). Immutable. |

## Macro & regime

- **Confirmed late-cycle or risk-off** (VIX > 25 over 5 days, HY spreads > 500bp, 2-10 inversion + abrupt un-inversion, hawkish Fed surprise): sizing cap = Standard, cash ≥ 25%, focus on defensives.
- **Violent intraday regime shift**: tighten all stops to 3%, notify Telegram, freeze new opens until next pre-market.
- **Major macro event within 24h** (FOMC, CPI, NFP, PCE, Powell): default sizing one notch down, max options exposure halved to 2.5% for the event window.

## Anti-revenge-trading

- If a ticker was cut in the last 5 trading days with P&L < 0, re-entry allowed **only** with:
  - Explicit "re-entry justified by {new catalyst}" line in research note
  - New CTQS score ≥ 70 (Standard or higher)
  - Sizing one notch below normal (max Standard even if High CTQS)

## Mode

- **Paper by default** (`TRADING_MODE=paper` + `ALPACA_BASE_URL` on paper)
- **Live switch**: never without explicit human edit of `.env` and corresponding log in `learnings.md`. The agent cannot flip modes.

## Self-evolution gates (immutable)

The agent can propose changes to `strategy.md` and command/skill prompts via `memory/prompt_evolution_proposals.md`. Applied changes require ALL of:

1. Proposal written with before/after diff + rationale + statistical evidence
2. Min sample size: 20 trades for per-setup tweaks, 50 trades for framework-wide tweaks
3. No modification to this `guardrails.md` immutable sections (hard caps, forbidden instruments, auto-defense, self-evolution gates themselves)
4. No new forbidden feature enabled
5. Change is append-only logged in `memory/strategy_evolution.md`
6. Drawdown auto-defense not currently active
7. No daily/weekly loss cap active

The agent must refuse to apply a proposal that fails any gate. Proposal marked `blocked: {reason}` and awaits human review.

## Hygiene

- **Never commit a secret**, never include a secret in a notification
- **Never delete** entries from `trade_log.md`, `research_log.md`, `strategy_evolution.md`, `prompt_evolution_proposals.md`, `learnings.md`, `daily_review.md`, `weekly_review.md`, `monthly_review.md`, `quarterly_rewrite.md` — all append-only
- **ISO UTC timestamps** everywhere: `2026-04-20T13:45:00Z`
- **Commit + push every run**. Missing pushes = stale state at next run
