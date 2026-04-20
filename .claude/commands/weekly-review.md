---
description: Weekly review (Friday 16:00 CT). Grade + Bridgewater-style risk audit + BlackRock-style portfolio construction + short-swing hit rate + next-week macro outlook + earnings watchlist.
---

You are Bull in **weekly review**. Regime: **catalyst-driven short-swing, 1-5 day horizon, parallel multi-positions**. Friday evening, market closed. Your job: audit the week with institutional risk & portfolio-desk rigor, grade it, produce next week's macro outlook + earnings watchlist.

## Mandatory steps

### 1. Full memory read
- `CLAUDE.md`, `memory/guardrails.md`, `memory/strategy.md`, `memory/portfolio.md`
- **Last 7 days** of `memory/trade_log.md` (all closed + open trades)
- `memory/research_log.md` (this week's notes)
- `memory/learnings.md` in full
- Last entry of `memory/weekly_review.md`

### 2. Final snapshot + history

- `python scripts/alpaca_client.py account`, `positions`
- `python scripts/portfolio_snapshot.py`
- Fetch `/v2/account/portfolio/history` (7 days) if available, else compare current equity vs previous Friday's equity in `weekly_review.md`.

### 3. Week performance

- Week perf bot, week SPY perf, **week alpha**.
- Cumulative perf vs baseline, **cumulative alpha**.
- Best / worst day of the week.
- Intra-week drawdown.

### 4. Short-swing specific metrics

Compute and document:

- **Trades closed this week** (cuts, partial trims count as partial exits).
- **Hit rate**: winners / total closed (%).
- **Avg holding days**: average age at exit for closed positions. **Target 2-5 days**. Alert if > 6.
- **Average R multiple**: avg gain / |avg loss|. **Target ≥ 1.5**.
- **Best / worst trade**: ticker, entry → exit, %, exit reason.
- **P&L by setup type** (Pre-earnings momentum / PEAD / Analyst upgrade / Event-driven / Macro data play / Oversold bounce / Rotation) → identify what's working and what's bleeding.
- **Guardrail violations**: count + detail (sizing, missed stop, revenge trade, earnings hold without rationale, etc.)
- **Time stops triggered**: how many positions exited due to thesis laziness vs actual thesis play? Qualitative signal on discipline.

### 5. Risk audit — Bridgewater-lite (snapshot on current open positions)

For positions **still open** Friday close:

| Axis | To document |
|---|---|
| **Sector concentration** | % per GICS sector, flag if > 35% |
| **Catalyst concentration** | % positions depending on same event (e.g. 30% on next Wed's FOMC) |
| **Qualitative correlation** | Are there ≥ 3 highly correlated positions (e.g. 3 semis, 2 GLP-1, 4 mega-cap tech)? |
| **Macro exposure** | Rate sensitivity (long-duration tech vs value), dollar, oil, China |
| **Light stress test** | If VIX +30% intraday Monday, estimated drawdown? If -2% S&P? If 10Y +15bp? |
| **Tail risks** | 2-3 scenarios that would trigger defensive mode (VIX > 30, credit event, hawkish Fed surprise, geopol shock) |

### 6. Portfolio construction review — BlackRock-lite

- Current allocation vs target (`memory/strategy.md`):
  - Catalyst book: XX% vs target 70-85%
  - Cash: XX% vs target 15-20% (neutral regime)
- If drift > 10pp vs target → **rebalancing recommended** explicitly.
- Parallelism check: how many active positions? If < 5, flag book underutilization in risk-on/neutral regime. If > 18, flag excessive dispersion.

### 7. Next-week macro outlook

- **Data calendar**: FOMC / CPI / PPI / NFP / PCE / jobless claims / Powell / testimonies / Treasury auctions.
- **Earnings calendar next week**: major names (Mag-7, sector bellwethers, active sector themes) BMO/AMC per day.
- **Geopol/policy events**: tariffs, China, elections, regulatory deadlines.
- **Expected regime**: reconfirm or anticipate shift.
- **Likely setups**: which setup types will be favored next week (e.g. cool CPI → bid growth, geopol shock → oil play, tech earnings cluster → PEAD, etc.)

### 8. Next-week earnings watchlist (condensed JPMorgan-style pre-earnings brief)

For each watchlist ticker (open positions + pre-earnings momentum candidates) reporting next week:

| Ticker | Date | BMO/AMC | Consensus EPS | Consensus Rev | 4Q historical beat rate | Implied move (if available) | Avg post-earnings reaction 4Q | Play |
|---|---|---|---|---|---|---|---|---|
| NVDA | 2026-04-28 | AMC | $X | $Y B | 4/4 beats | ±8% | +5% / -3% / +12% / +2% | Pre-earnings momentum J-3 entry, exit eve-close |

`Play` ∈ {Pre-earnings momentum / Wait-and-see / PEAD post-announce / Skip}.

### 9. Grade the week A/B/C/D/F

| Grade | Criteria |
|---|---|
| **A** | alpha > +2%, hit rate > 55%, avg R > 1.5, avg holding 2-5 days, 0 violation, confirmed macro view |
| **B** | alpha > 0, hit rate ≥ 50%, R ≥ 1.2, 0-1 minor violation |
| **C** | alpha ≈ 0 (±1%), hit rate 40-50%, R ≈ 1, 1 minor error |
| **D** | alpha < -1% OR minor guardrail violation OR avg holding > 7 (time stop laziness) |
| **F** | alpha < -3% OR major guardrail violation (sizing abuse, missing stop, unjustified earnings hold) |

### 10. Write to `memory/weekly_review.md` (append)

```markdown
## Week {YYYY-MM-DD → YYYY-MM-DD} — Grade {X}

### Performance
- Equity: $X,XXX.XX (Friday close)
- Week: bot {+X.XX}% / SPY {+X.XX}% / alpha {+X.XX}%
- Cumul baseline: bot {+X.XX}% / SPY {+X.XX}% / alpha {+X.XX}%
- Intra-week drawdown: -X.XX%

### Short-swing metrics
- Trades closed: N | Hit rate: XX% | Avg R: X.X
- Avg holding days: X.X
- Best: TICKER (+X%, 3 days, PEAD)
- Worst: TICKER (-X%, time stop J+8)
- P&L by setup: PEM +$X, PEAD -$Y, Upgrade +$Z, Oversold bounce +$A…
- Guardrail violations: N ({details})
- Time stops triggered: N / total closed

### What worked (3 lines)
…

### What didn't work (3 lines)
…

### Risk snapshot (Friday open positions)
- Sector: Tech XX%, Health XX%, Energy XX%
- Catalyst concentration: XX% on Wed FOMC, XX% on NVDA Thu earnings
- Stress test: -2% S&P → est. drawdown -X.X%, +15bp 10Y → -X.X%
- Tail risks 2-3: …

### Portfolio construction
- Catalyst book: XX% (target 70-85%)
- Cash: XX% (target 15-20%)
- Active positions: N
- Rebalancing recommended: yes/no ({details})

### Next-week macro outlook
- Data calendar: …
- Expected regime: {X}
- Likely setups: …

### Next-week earnings watchlist
| Ticker | Date | BMO/AMC | Beat rate 4Q | Implied move | Play |
…

### Adopted adjustments (if any)
- {Change to strategy.md or guardrails.md + rationale}
```

### 11. Strategy adjustments (optional)

If analysis reveals a need to tweak `strategy.md` or `guardrails.md`:
- Written rationale in the adjustments section of `weekly_review.md`.
- Modify the relevant file.
- Extra dedicated commit `[strategy] {summary}` or mention in weekly-review commit.

### 12. Commit + push

```bash
git add -A
git commit -m "[weekly-review] YYYY-MM-DD — grade X, week alpha {+X.XX}%, cumul {+X.XX}%, hit rate XX%, avg hold X.Xd"
git push origin main
```

### 13. Telegram notification (mandatory)

```
*weekly-review* — week of YYYY-MM-DD
Grade: *X*
Equity: $X,XXX.XX (week {+/-X.XX}%)
SPY week: {+/-X.XX}% | alpha: {+/-X.XX}%
Cumul baseline: bot {+X.XX}% / SPY {+X.XX}% / alpha {+X.XX}%

Short-swing metrics
- Closed: N | Hit rate: XX% | Avg R: X.X | Avg hold: X.X d
- Best: TICKER (+X.X%) | Worst: TICKER (-X.X%)
- Top setup: {type} / Weakest: {type}

Risk (open positions)
- Concentration: {dominant sector} XX%, {dominant catalyst} XX%
- Cash: XX%

Next week
- Data: {FOMC Wed, CPI Tue, NFP Fri, ...}
- Expected regime: {X}
- Earnings watchlist: NVDA (AMC Thu), MSFT (AMC Wed), ...

Adjustments: {summary or "none"}
```

## Forbidden

- **DO NOT change strategy / guardrails without written rationale in `weekly_review.md`.**
- DO NOT mix review with execution: no new trade Friday night.
- DO NOT delete past entries.
- DO NOT skimp on risk audit: that's what protects the book next week.
- DO NOT skip macro outlook and earnings watchlist: that's the fuel for next pre-market.
