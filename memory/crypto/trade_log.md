# Trade log — Crypto

Append-only. **Never rewrite** a past entry. Reverse chronological.

## Schema

```
### YYYY-MM-DDTHH:MM:SSZ — {BUY|SELL|TRIM|CUT|ADD|STOP-UPDATE} {SYMBOL} {qty}@{price}
- Order ID: {id}
- Value USD: ${value}
- % NAV at entry: {n}%
- Style: {short-swing | swing | momentum | breakout}
- CTQS: C{xx}/T{xx}/Q{xx}/S{xx} = {total}/100 → Conviction {Probe|Standard|High}, confidence {xx}%
- Catalyst: {event/narrative} OR "technical-only"
- Thesis: {1-3 lines}
- Stop: {type + level}
- Take-profit: {level or trailing}
- Time stop: {UTC ISO or n/a}
- Routine: {crypto-hourly / crypto-daily-review}
- Notes: ...
```

## Entries

### 2026-04-20T21:13:00Z — STOP-UPDATE BTCUSD 0.000049999@75999.72
- Order ID: n/a (manual-trail bookkeeping, no order placed)
- Value USD: $3.80
- % NAV at entry: 0.004% (dust — inherited stub)
- Style: inherited (legacy from equities-side fill, pre-Bull-v2)
- CTQS: n/a (not opened by Bull-Crypto)
- Catalyst: n/a (legacy)
- Thesis: Inherited residual BTC stub (avg entry $73,094.17, +3.97%). BTC is in approved crypto universe → retain; size ($3.80) is below any meaningful market-impact cut threshold.
- Stop: manual-trail init — max_price_since_entry=$75,999.72, trail=8% → stop level $69,919.74. Updated each crypto-hourly run (P2). If price < max × 0.92 → CUT at market.
- Take-profit: trailing only
- Time stop: n/a (legacy stub, no horizon)
- Routine: crypto-hourly
- Notes: P7 housekeeping init. No order placed, no Telegram (not a moved stop). Future hourly runs ratchet max_price upward only.
