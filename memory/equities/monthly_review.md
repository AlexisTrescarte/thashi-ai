# Monthly deep reviews — Equities

Append-only. Every last Friday of the month at 17:00 CT the `monthly-deep-review` routine appends a section here.

Purpose: quantitative audit (Sharpe/Sortino/Max DD/Calmar, P&L by setup/instrument/style) + **prompt evolution proposals** gated by `guardrails.md`.

See `.claude/commands/monthly-deep-review.md` for the full template.

## Reviews

## 2026-04-01 → 2026-04-24 — Month 1 (partial, grade C)

### Performance
- Month return (since baseline 04-20): bot +0.03% ($97,382.41 → $97,413.65), bench N/A (baseline SPY/QQQ never captured at market-close), alpha N/A
- Cumul since baseline (04-20): bot +0.03% — same as month (first month of life)
- Sharpe (annualised): N/A — only 3 usable daily equity points (04-20, 04-22, 04-24); insufficient for a meaningful sigma. Computed stub ≈ 0 given ~flat equity.
- Sortino (annualised): N/A — no downside deviation (no negative daily return recorded).
- Max intra-month DD: 0.00% (equity monotonic flat → slight up; no drawdown observed).
- Calmar: N/A (return ~0 / DD 0).
- Vol: bot ~0% (3 pts) · bench N/A
- Correlation to bench: N/A

### Trade stats
- Closed: 0 | Hit rate: N/A | Avg R: N/A | Avg hold: N/A
- Open at EoM: 1 (GOOGL 7@$339.29 Probe 2.44% NAV, unreal P&L +$31.22 / +1.31%, native trail ratcheted HWM $345.23, stop $317.61, mandatory pre-earnings exit 04-28 close)
- Orders placed this month: 1 fill (GOOGL 04-23) + 1 native trailing stop
- Best setup: PEAD / pre-earnings momentum (GOOGL TPU+Anthropic fuse — single data point, unrealized +1.31%)
- Worst setup: N/A

### By instrument
- Equity: 1 open, 0 closed, unreal +$31.22
- ETF: 0
- Leveraged ETF: 0
- Options: 0
- Crypto: 0 (residual BTC $3.76 was auto-reattributed between 04-20 and 04-22, no trade placed from this agent)

### By style
- Day: 0
- Short-swing: 1 open (GOOGL, 3-4 TD to pre-earnings exit)
- Swing: 0
- Positional: 0

### Regime distribution + alpha per regime
- Daily regime tags captured (3/5 sessions): 04-20 late-cycle · 04-22 neutral · 04-23 neutral lean risk-on · 04-21 missed · 04-24 missed (harness [INCIDENT])
- Rough distribution on captured days: late-cycle 33% · neutral 33% · neutral-risk-on 33%
- Alpha per regime: N/A — no closed trades, and bench not captured at baseline → alpha uncomputable this month

### Discipline
- Trading guardrail violations: 0
- Operational [INCIDENT] count: 1 (2026-04-24 — six routines missed: pre-market / market-open / 3× intraday-scan / market-close; daily-review was first wake-up at 15:30 CT)
- Stop discipline: 1/1 new position received a native trailing stop within 5 minutes of fill (GOOGL, Alpaca native 8% trailing)
- Stop-update frequency: 1 native auto-ratchet (HWM $339.185 → $345.23, stop $312.05 → $317.61) executed by Alpaca without agent intervention on 04-24 (harness down) — the "prefer native trailing" rule (RULE-ADJUSTMENT 2026-04-21) is the reason the book survived the missed-routine day.
- Auto-defense triggers: 0
- Loss-cap triggers: 0 (daily), 0 (weekly)
- Activity floor: MISSED (target ≥ 1 BUY / 3 TD and ≥ 3 BUY / 5 TD in risk-on/neutral; actual 1 BUY / 5 TD)

### Macro context
- Regime: started late-cycle (ATH + hot CPI + FOMC hawkish bias) → drifted to neutral lean risk-on by 04-23 on Iran ceasefire + AI-capex tape (GEV +13.75% beat+raise, Alphabet TPU 8t/8i + Anthropic commitment).
- Benchmark vol: N/A (no SPY/QQQ series captured).
- Notable events: FOMC 04-28/29 (hold 94.8%), PCE 04-25 (pending at close 04-24 — no data captured due to missed routines), GOOGL earnings 04-29 AMC (pending, affects open position).

### What worked (3-5 lines)
- Conviction-over-activity discipline on 04-20–04-22: refused to chase a tape at ATH with CPI hot + earnings cluster; preserved 100% cash until a concrete catalyst (GEV Q1 beat+raise on 04-22) reset the opportunity set.
- Anti-FOMO + spread guards on 04-23 market-open: the 0.5% spread cap rejected GEV (4.66% spread + ask +14% vs plan) and VRT (5.38% spread) at thin open books, saving the book from gap-day slippage. GOOGL Probe still filled cleanly (0.029% spread).
- Native-trailing preference: GOOGL stop was placed as an Alpaca native 8% trailing (not manual-tracked), which auto-ratcheted on 04-24 when the harness was down — this is the *only* line of defense that held during the [INCIDENT] cascade.

### What didn't (3-5 lines)
- Activity floor chronically missed: 1 BUY over 5 TD vs target of 3 BUYs per 5 TD in neutral/risk-on. Two of three BUY-queue names (GEV, VRT) were skipped mechanically at open (spread) with an explicit "re-tempt at intraday-scan 10:30" plan, but the 04-23 intraday-scan runs never fired in our trace (daily-review references them only prospectively), and the 04-24 cascade killed any chance of re-attempting before the PEAD window degraded.
- Baseline benchmark (SPY+QQQ blend) was never posted at 04-20 market-close. `portfolio.md` still has `baseline_SPY: _(first live run date)_` stubs. Month-1 alpha is literally uncomputable.
- [INCIDENT] 2026-04-24 — six routines silent; time-stops in horizon (GOOGL 04-28) are exposed if 04-27 / 04-28 harness also misfires. The only survived-by-luck mechanism was the native trailing stop, which doesn't enforce dated pre-earnings exits.
- Stop-update logging frequency = 0 manual updates in the month (target ≥ 1 per open-trade-day). Only 1 native auto-ratchet. With 1 position open for 2 trading days, that's acceptable on paper — but the pattern would fail at scale.

### Prompt evolution proposals
- **Proposal 2026-04-24T22:00:00Z-1** — "Bind dated exits (pre-earnings, in-horizon time-stops) to GTD sell-limit / sell-stop orders at fill, not to future routines" — state: *proposed* → **blocked by G3 (sample size framework-wide 1 << 50)**. Kept in queue for re-examination once N ≥ 50.

### Next-month focus (May 2026)
- **Bias / lean**: PEAD continuation (GEV / VRT re-look on pullbacks within FOMO guard), GOOGL post-earnings reset on 04-30 (if catalyst survives the print). Post-FOMC tape 04-30/05-01 may open risk-on if dot plot is neutral.
- **Risks to watch**: FOMC 04-28/29 dot plot surprise · PCE 04-25 (data ingestion on 04-27 pre-market) · MSFT/META/AMZN earnings 04-29/30 (mega-cap tape risk for GOOGL) · harness stability (confirm 04-24 [INCIDENT] was one-off).
- **Evolution to monitor**: GTD-at-fill proposal stays queued — re-evaluate at May monthly if N ≥ 50, or accept the operational rule via human-edit if incidents recur.
- **Activity-floor remediation**: May target ≥ 3 BUYs / 5 TD in neutral/risk-on regime; if a BUY is skipped at open for mechanical reasons (spread/FOMO), log an explicit re-attempt plan **and** verify at next intraday-scan that it was executed or formally dropped.

