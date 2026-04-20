---
name: review
description: Compute institutional performance metrics (Sharpe, Sortino, Max DD, Calmar, hit rate, avg R, P&L by setup/instrument/style) from agent-namespaced trade log. Produces a review block ready to append to daily_review.md / weekly_review.md / monthly_review.md / quarterly_rewrite.md. Invoke from any review routine.
---

# Skill: review

Compute quantitative performance metrics for a given window + agent, distill into an institutional-grade review block. Does not modify strategy — that's `evolve`'s job.

## Invocation contract

Inputs (from the calling routine):
- `agent`: `equities` or `crypto`
- `window_start`: ISO date
- `window_end`: ISO date
- `rhythm`: `daily` / `weekly` / `monthly` / `quarterly`

Outputs:
- A markdown block appended to `memory/{agent}/{rhythm}_review.md`
- A grade A/B/C/D/F (per the criteria table below)
- Optional proposals queued to `memory/prompt_evolution_proposals.md` (monthly and quarterly only)

## Steps

1. **Read inputs**:
   - `memory/{agent}/trade_log.md` (all entries in window)
   - `memory/{agent}/portfolio.md` (latest + equity series if available)
   - `memory/{agent}/research_log.md` (for CTQS at entry, setup types)
   - `memory/{agent}/daily_review.md` / `weekly_review.md` (for continuity)
   - `memory/learnings.md` (for violations, caps, regime shifts)
   - Run `python scripts/metrics.py --agent {agent} --start {window_start} --end {window_end}` to get JSON of metrics
2. **Compute if not already**:
   - Total return (window, cumulative since baseline)
   - Benchmark return (window, cumulative) — SPY+QQQ blend for equities, BTC for crypto
   - Alpha (window, cumulative)
   - Hit rate (winners / total closed)
   - Average R (avg_gain / |avg_loss|)
   - Average holding (calendar days closed trades)
   - Max intra-window drawdown
   - **Sharpe (annualised, 0% rf assumption)** — monthly and quarterly only
   - **Sortino (annualised)** — monthly and quarterly only
   - **Calmar (return / max DD)** — monthly and quarterly only
   - P&L by setup type, by instrument (equity/ETF/leveraged-ETF/option/crypto), by style (day/short-swing/swing/positional)
   - Guardrail violations count
   - Time stops triggered / total time stops expected
3. **Write the review block** (template per rhythm below)
4. **Grade** (A/B/C/D/F per criteria)
5. **Monthly/quarterly only**: emit prompt evolution proposals if criteria met

## Grading criteria

| Grade | Window alpha | Hit rate | Avg R | Violations | Extra conditions |
|---|---|---|---|---|---|
| **A** | > +2% | > 55% | > 1.5 | 0 | Sharpe > 1.5 (monthly+) |
| **B** | > 0 | ≥ 50% | ≥ 1.2 | 0-1 minor | Sharpe > 1.0 (monthly+) |
| **C** | ±1% | 40-50% | ≈ 1 | 1 minor | Sharpe > 0.5 |
| **D** | -1 to -3% | < 40% | < 1 | 1-2 | OR violations of stop discipline |
| **F** | < -3% | - | - | major violation | OR immutable-cap breach attempted |

## Templates

### Daily review block

```markdown
## YYYY-MM-DD — Daily review (grade {X})

### Performance
- Equity: $X (day {+/-X.XX}%)
- Benchmark day: {+/-X.XX}% | alpha day: {+/-X.XX}%
- Cumul baseline: bot {+X.XX}%, bench {+X.XX}%, alpha {+X.XX}%

### Activity
- Trades opened today: N
- Trades closed today: N (W:{n} / L:{n} / BE:{n})
- Hit rate today: XX% | Avg R today: X.X
- Stops set within 5min on all new positions: yes/no

### By setup (today)
- Earnings momentum: {W-L, P&L}
- PEAD: ...
- Technical breakout: ...

### What worked (2 lines)
- ...

### What didn't (2 lines)
- ...

### Discipline log
- Guardrail violations: N — {details or "none"}
- Time stops honored: yes / partial / no
- Stop updates logged: N

### Carry-forward for tomorrow
- Aging (J+6+): ...
- Pre-earnings tomorrow: ...
- Macro 24h: ...
- Regime note: ...

### Lesson of the day (1 line)
- ...
```

### Weekly review block

Per `.claude/commands/weekly-review.md` template (Bridgewater-lite risk audit, BlackRock-lite portfolio construction, JPMorgan-style earnings watchlist).

### Monthly review block

```markdown
## {YYYY-MM-DD → YYYY-MM-DD} — Month {N} (grade {X})

### Performance
- Month return: bot {+X.XX}%, bench {+X.XX}%, alpha {+X.XX}%
- Cumul since baseline: bot {+X.XX}%, bench {+X.XX}%, alpha {+X.XX}%
- Sharpe (annualised): X.XX
- Sortino (annualised): X.XX
- Max intra-month DD: -X.XX%
- Calmar: X.XX

### Trade stats
- Closed: N | Hit rate: XX% | Avg R: X.X | Avg hold: X.X d
- Best setup: {type} ({+X.X%})
- Worst setup: {type} ({-X.X%})

### By instrument
- Equity: N trades, P&L $X
- ETF: ...
- Leveraged ETF: ...
- Options: ...
- Crypto (crypto agent only): ...

### By style
- Day trades: N, P&L $X, hit rate XX%
- Short-swing: ...
- Swing: ...
- Positional: ...

### Discipline
- Total violations: N
- Stop-update frequency: X.X per open-trade-day
- Auto-defense triggers: 0/1
- Loss-cap triggers: {daily/weekly}

### Macro context
- Regime distribution: {risk-on X%, neutral X%, late-cycle X%, risk-off X%}
- Benchmark volatility: X%
- Our vol: X%
- Correlation to benchmark: X.X

### What worked (3-5 lines)
- ...

### What didn't (3-5 lines)
- ...

### Prompt evolution proposals
- Proposal {id-1} — {summary} — state: {proposed | applied | blocked: reason}
- Proposal {id-2} — ...
- (empty if none)

### Next-month focus
- Bias / lean: {setups to favor}
- Risks to watch: {events, regime triggers}
```

### Quarterly rewrite block

Per `.claude/commands/quarterly-rewrite.md` template.

## Proposal generation rules (monthly + quarterly only)

Emit a proposal when:
- A setup has N ≥ 20 trades AND hit rate is > 10pp below cohort average AND avg R < 0.9 → propose raising its CTQS threshold by +5
- A setup has N ≥ 20 trades AND hit rate > 60% AND avg R > 1.5 → propose lowering its CTQS threshold by 2 (more activity)
- Stop-methodology X has N ≥ 20 and MFE/MAE ratio < 0.5 → propose swapping default stop type for that setup
- Regime-X exposure produces < 0 alpha for 2+ consecutive months → propose reducing new-opens in that regime by one sizing notch

All proposals follow the schema in `memory/prompt_evolution_proposals.md`.

## Guardrails for review itself

- Never write to any file outside `memory/{agent}/{rhythm}_review.md` and `memory/prompt_evolution_proposals.md`
- Never modify `trade_log.md` or `research_log.md`
- Never delete past review entries
- If metrics script fails: log `[API-DEGRADED]` in learnings and produce a qualitative review only, explicitly noting missing metrics
