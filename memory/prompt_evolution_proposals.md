# Prompt evolution proposals

Append-only queue. The `monthly-deep-review` and `quarterly-rewrite` routines write proposals here. The `evolve` skill reads, gate-checks, and applies (or blocks) them.

## States

- `proposed` — freshly written, awaiting gate check
- `applied` — gates passed, change executed, logged to `strategy_evolution.md`
- `blocked: {reason}` — gate failed, awaits human review

## Schema

```markdown
## {proposal-id: YYYY-MM-DDTHH:MM:SSZ-N} — {title}

**State**: proposed
**Scope**: {target file path}
**Proposed by**: {routine}
**Sample size**: N trades in window {YYYY-MM-DD → YYYY-MM-DD}

### Problem observed
{2-3 lines — metric drift, setup bleeding, etc., with numbers}

### Proposed change
```diff
- old line
+ new line
```

### Rationale
{2-3 lines}

### Gates
- [ ] min sample size met (N ≥ 20 per-setup / N ≥ 50 framework)
- [ ] no modification of immutable guardrails section
- [ ] no forbidden feature enabled
- [ ] no disabling of auto-defense
- [ ] no disabling of evolution gates
- [ ] no active drawdown auto-defense
- [ ] no active daily/weekly loss cap

### Decision
{applied | blocked: reason}
{timestamp of decision}
```

## Proposals

## 2026-04-24T22:00:00Z-1 — Bind dated exits to GTD sell-limit orders at fill

**State**: proposed
**Scope**: `.claude/commands/market-open.md` (execution-playbook section) + `.claude/commands/intraday-scan.md` (stop management section)
**Proposed by**: monthly-deep-review (2026-04 month-1 partial)
**Sample size**: N = 1 closed-or-open trade in window 2026-04-01 → 2026-04-24 (framework-wide scope requires ≥ 50 — will fail G3)

### Problem observed
On 2026-04-24 all six scheduled routines (pre-market, market-open, 3× intraday-scan, market-close) failed to fire (harness/remote-trigger [INCIDENT], see `memory/learnings.md` 2026-04-24T20:45:00Z). GOOGL's mandatory pre-earnings exit at 2026-04-28 close is currently a **manual** time-stop: it depends on a future routine waking up to issue the SELL before earnings 2026-04-29 AMC. If 04-27 and/or 04-28 routines also miss, the book will hold through a binary event with no agent intervention possible. Alpaca-native trailing stops (which ratcheted autonomously on 04-24) are the only defense that held — but they cannot enforce a dated exit (they only react to drawdown from HWM).

Observed metric: 1 missed-routine day in 5 TD = 20% harness reliability gap. Single position (GOOGL) exposed; if the 04-27/04-28 harness misses again, a 100% failure of pre-earnings exit discipline on this trade.

### Proposed change
```diff
# In .claude/commands/market-open.md, execution-playbook section
# (illustrative — exact diff to be authored at apply time)
- For every BUY with a time-stop in horizon: log the time stop in trade_log and
-   rely on intraday-scan / market-close to enforce the exit.
+ For every BUY with a dated exit inside the expected holding horizon (pre-earnings
+   exit, explicit time-stop), place a companion GTD sell-limit or sell-stop order
+   at Alpaca at fill-time — bound to the dated exit — so the exchange enforces
+   the exit if the agent harness misses subsequent routines. Alpaca-native trailing
+   stop remains the primary drawdown defense; the GTD order is the backstop for
+   calendar-based exits only.
```

### Rationale
- **Operational**: 2026-04-24 [INCIDENT] proved that harness availability is not 100%. Relying on "a future routine will fire" is a single point of failure for any dated exit.
- **Consistent with existing rule**: the `prefer native trailing` rule (2026-04-21 RULE-ADJUSTMENT) already recognises that exchange-enforced stops outperform manual ones. Extending the same principle to dated exits is a natural follow-on.
- **Risk-reducing, not risk-adding**: GTD sell-limit does not remove any agent discretion (agent can cancel/replace at any intraday-scan if thesis evolves), it only guarantees a floor in the failure mode where the agent is silent.

### Evidence
- **Window**: 2026-04-01 → 2026-04-24 (5 trading days of life).
- **Incidents**: 1 (six routines missed on 04-24).
- **Affected positions**: 1 (GOOGL, pre-earnings exit 04-28 close pending).
- **Delta vs baseline discipline**: under current rule, 04-27 or 04-28 miss → 100% pre-earnings-exit failure. Under proposed rule, exit is enforced by exchange GTD regardless of harness state.
- **Statistical limit**: N = 1 trade in window → sample size insufficient for framework-wide gate (G3 requires ≥ 50). The proposal is expected to be blocked at this monthly cycle; it remains in queue for re-examination as N grows.

### Revert trigger
Revert if, after application (once gates pass), over any 50-trade window: (a) rate of pre-empted-but-later-needed GTD cancellations > 30% (meaning the dated-exit rule is too rigid), OR (b) any dated-exit GTD fires incorrectly due to stale data and produces a bad fill worse than a subsequent agent-managed exit would have produced. Track in monthly review "Stop discipline" section under a new sub-bullet "Dated-exit GTD outcomes: {fired-on-target / pre-empted / misfired}".

### Gates (evolve skill, 2026-04-24T22:05:00Z, rhythm=monthly, agent=equities)
- [x] G1 target scope allowed (.claude/commands/*.md — monthly-legal target)
- [x] G2 immutable content preserved (no edit to hard-cap / auto-defense / forbidden-instrument / self-evolution-gates sections)
- [ ] G3 sample size met — **FAIL (N=1 trade in window, framework-wide scope requires ≥ 50)**
- [x] G4 no forbidden-feature enablement (no shorts/naked/futures/margin/cap-raise)
- [x] G5 no evolution-gate weakening (does not target evolve/SKILL.md, does not modify gates)
- [x] G6 no active risk event (no auto-defense in 14d, no daily/weekly loss cap in 3d, last run not API-degraded)
- [x] G7 evidence with concrete numbers + window (N=1, 2026-04-20→2026-04-24, 1 [INCIDENT])
- [x] G8 revert trigger defined (pre-emption rate > 30% over 50-trade window, or any misfire bad-fill vs counterfactual)

### Decision
**State**: blocked: G3 — insufficient sample size (N=1 trade, framework-wide scope requires N ≥ 50)
**Decided at**: 2026-04-24T22:05:00Z
**Disposition**: remains in queue for re-evaluation at next monthly-deep-review once cumulative sample crosses the N ≥ 50 framework threshold. No [INCIDENT] logged (G3 is not an immutable-attack gate). No entry appended to `memory/strategy_evolution.md` (only applied proposals go there).

