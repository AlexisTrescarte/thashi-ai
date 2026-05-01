---
name: hf-decide
description: Decision skill for Bull-HF-BTC — analyse multi-timeframe BTC indicators + WebSearch news + optional chart visual, then emit a strict JSON decision (OPEN_LONG/OPEN_SHORT/CLOSE/HOLD/SKIP) with limit_price/TP/SL/sizing. Used by hf-tick.
---

# hf-decide

Decision skill invoked at every 5-min tick by `hf-tick`. Wraps the analysis loop into a reproducible procedure.

## Input

- `/tmp/hf_prompt.md` — pre-built by `harness.py prepare`. Contains all numerical context.
- `/tmp/hf_context.json` — same data as JSON, for tool-driven access.
- WebSearch results — fetched in-tour for news.
- Optional chart PNG — path inside `/tmp/hf_prompt.md` if quota allowed it.

## Procedure

### Step 1 — Establish regime

Look at 1Hour first (macro), then 15Min (intraday trend), then 5Min (entry timing).
Tag each timeframe:
- **TREND UP** if price > EMA20 > EMA50 AND RSI 50-70 AND MACD hist > 0
- **TREND DOWN** if price < EMA20 < EMA50 AND RSI 30-50 AND MACD hist < 0
- **RANGE** if BB bandwidth < 0.6% AND |dist_EMA20| < 0.2% AND RSI 40-60
- **SQUEEZE** if BB bandwidth < 0.4% on 5Min (high-edge setup, often precedes break)
- **OVERBOUGHT** if RSI > 70 + price > BB upper
- **OVERSOLD** if RSI < 30 + price < BB lower

### Step 2 — Fetch news (mandatory)

Call `WebSearch` once with: `BTC bitcoin news {today} ETF spot flow funding rate sentiment`.

Synthesize 3-5 bullets:
- ETF spot flows (in/out, $M)
- Macro / Fed / regulatory headlines
- On-chain (LTH supply, miner outflows, funding rates)
- Sentiment derivatives (CME basis, options skew)

### Step 3 — Confluence scoring

Count alignement sources (max 7) for the candidate direction:
1. RSI 5m direction
2. MACD 5m hist sign
3. BB %B trend (rising %B = bullish, falling = bearish)
4. EMA20/EMA50 stack on 5Min
5. VWAP relationship (above = bullish bias, below = bearish)
6. Volume z-score (positive = momentum confirm)
7. News sentiment (positive flows / catalysts)

**Confluence required to OPEN** : ≥4/7 in PROD mode, ≥3/7 in TEST mode (see prompt banner). Below threshold → SKIP.

### Step 4 — Levels

Use ATR(14) on 5Min for SL/TP placement:
- SL distance: 1.0 to 1.5 × ATR (no tighter — gets eaten by noise)
- TP distance: 2.0 to 3.5 × ATR (R/R ≥ 1.8 minimum — hard guardrail; target 2.0-2.5)
- Limit price: current ask (LONG) or current bid (SHORT) ± 0.05% buffer for fill

If a key level (BB upper/lower, EMA50, VWAP) sits between entry and TP/SL — adjust to respect it.

### Step 5 — Sizing by confidence

Confidence (0-100) is YOUR estimate of edge quality. The prompt banner tells you the active mode.

**PROD mode**:

| Confidence | Sizing | Use when |
|---|---|---|
| < 50 | SKIP | not enough confluence |
| 50-59 | SKIP (sub-min) | borderline — saves a slot |
| 60-69 | 2-3% (probe) | 4/7 confluence, no chart confirm |
| 70-84 | 5-7% (standard) | 5/7 confluence, chart confirms |
| 85+ | 8-12% (high) | 6/7 confluence + clear pattern + news catalyst |

**TEST mode** (loosened to collect data):

| Confidence | Sizing | Use when |
|---|---|---|
| < 40 | SKIP | sub-min, harness rejects |
| 40-49 | 2% (probe-test) | 3/7 confluence borderline |
| 50-59 | 3% (probe-test) | 3-4/7 confluence valid |
| 60-69 | 4% (probe) | 4/7 confluence standard |
| 70-84 | 5-7% (standard) | 5/7 + chart |
| 85+ | 8-12% (high) | 6/7 + catalyst |

### Step 6 — Decide & emit JSON

Output structure (strict — harness parses with regex `\`\`\`json\\s*(\\{...\\})\\s*\`\`\``):

```json
{
  "action": "OPEN_LONG|OPEN_SHORT|CLOSE|HOLD|SKIP",
  "trade_id": null,
  "limit_price": 0.0,
  "tp": 0.0,
  "sl": 0.0,
  "sizing_pct": 0,
  "rr_ratio": 0.0,
  "time_horizon_min": 0,
  "confidence": 0,
  "reason_fr": "",
  "ctqs": {"T": 0, "Q": 0, "S": 0, "C": 0}
}
```

`reason_fr` is the user-facing notification reason. Vulgarize for a non-technical reader: "RSI sortait de zone survente, MACD croisait à la hausse, ETF in-flows confirmaient overnight." 2-3 sentences max.

## Forbidden

- Don't open if a position is already in `sim_portfolio.open_trades` — say HOLD or CLOSE.
- Don't widen R/R below 1.8 — hard guardrail; even with strong conviction, harness will reject.
- Don't size > 12% — harness rejects.
- Don't recommend instruments other than BTC/USD — out of scope.
- Don't invent indicators not present in the prompt.
