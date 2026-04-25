---
name: pretrade-check
description: Defensive pre-trade gate that runs BEFORE the trade skill submits an order. Combines kill-switch, fat-finger, notional cap, rate-limit (pretrade_guards.py) and microstructure confirmation (microstructure-confirm subagent). Returns a single JSON verdict {pass, blockers[]}. Invoke from market-open and intraday-scan immediately before each BUY/SELL.
---

# Skill: pretrade-check

This skill is the **defensive layer** between the LLM's trade decision and the broker API call. It exists because the dominant failure mode of an unattended LLM-driven trader is not market loss — it is hallucinated quantities, fat-finger prices, runaway loops, and adversarial input. Those are caught here, in deterministic Python and a tightly-scoped subagent, not in the trade prompt.

> The trade skill remains the executor. This skill is the **veto** that runs first.

## When to invoke

- Inside `trade` skill (BUY / ADD / TRIM / SELL), **immediately before** placing the order.
- Optionally from `intraday-scan` when sizing an opportunistic BUY.
- Skip for `STOP-UPDATE` (stop adjustments are not new exposure).

## Procedure

### 1. Pre-trade guards (deterministic Python)

```bash
python scripts/pretrade_guards.py check \
    --symbol {SYMBOL} --side {buy|sell} \
    --qty {QTY} --price {ORDER_PRICE} \
    --ref-price {MID_OR_LAST} \
    --equity {ACCOUNT_EQUITY} \
    --max-position-pct 10 \
    --max-fat-finger-pct 2 \
    --max-per-minute 6 --max-per-hour 30
```

The script returns `{"pass": bool, "reasons": [...], "checks": {killswitch, fat_finger, notional, rate_limit}}` and exits 2 on failure. If `pass: false`, **stop here** — log to `learnings.md` with the exact reason and return WITHOUT placing the order.

### 2. Microstructure confirmation (subagent)

If guards passed, invoke the `microstructure-confirm` subagent via the Task tool:

> "Use the microstructure-confirm subagent. symbol={SYMBOL}, side={buy|sell}, qi_threshold=0.10, max_spread_bps=30."

It returns a JSON `{verdict: CONFIRM|NEUTRAL|BLOCK, ...}`.

Decision matrix:

| LLM conviction (CTQS) | NEUTRAL verdict | BLOCK verdict |
|---|---|---|
| High (≥85) | proceed (LLM signal strong enough) | abort, log "microstructure block" |
| Standard (70-84) | proceed if spread ≤ 20 bps, else abort | abort |
| Probe (55-69) | abort (need micro confirmation for low conviction) | abort |

CONFIRM always proceeds.

### 3. Record + emit

After a successful fill:

```bash
python scripts/pretrade_guards.py record --symbol {SYMBOL} --side {buy|sell} --qty {QTY} --price {FILL_PRICE}
python scripts/otel_log.py event trade.fill --symbol {SYMBOL} --side {buy|sell} --qty {QTY} --price {FILL_PRICE} --reason "{CTQS_SCORE} {STYLE}"
```

If aborted at any stage:

```bash
python scripts/otel_log.py event trade.abort --symbol {SYMBOL} --side {buy|sell} --check {failed_check} --reason "{first blocker}"
```

## JSON contract returned by this skill

```json
{
  "pass": true,
  "blockers": [],
  "guards": { ... pretrade_guards JSON ... },
  "microstructure": { ... subagent JSON ... }
}
```

Or on failure:

```json
{
  "pass": false,
  "blockers": ["fat-finger: ...", "microstructure BLOCK: spread 47 bps > 30"],
  "guards": { ... },
  "microstructure": { ... }
}
```

## Hard rules

- This skill **never** places an order. It only blocks or clears.
- A `pass: false` result from this skill is **non-overridable** by the LLM in the same run. To bypass, a human must edit `.claude/settings.json` or deactivate the killswitch.
- `pretrade_guards.py record` is called only AFTER a fill is confirmed by Alpaca, never before.
- Failures are logged to `memory/runs.jsonl` via `otel_log.py` for audit.

## Wiring status

This skill is **available** but not yet auto-invoked by the existing `trade` skill (additive deployment — first land, then wire up after a paper-trading day shows no false positives). Until then, pre-market and intraday-scan commands may invoke it manually before each BUY queue dispatch.

Migration plan (next round):
1. Land this skill + the 4 supporting scripts.
2. Run for 1 paper-trading day, inspect `memory/runs.jsonl` for spurious blocks.
3. Tune `qi_threshold` / `max_spread_bps` based on observed false-positive rate.
4. Update the `trade` skill BUY section to call this skill as step 0.
