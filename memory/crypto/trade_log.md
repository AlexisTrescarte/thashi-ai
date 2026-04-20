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

### 2026-04-20T23:10:12Z — CUT BTC/USD 0.000049999@~75790.80
- Order ID: 3d292f92-3969-4a6f-9270-8ec74d896c8f
- Value USD: ~$3.79
- % NAV at exit: 0.004%
- Style: orphan dust cleanup
- CTQS: n/a (inherited position, never CTQS-justified)
- Catalyst: none
- Thesis: Residual BTC inherited from legacy equities runs (see learnings 2026-04-20). Never had a documented CTQS, stop, or thesis under Bull-Crypto. Cleaned to establish a flat baseline for the Bull-Crypto namespace.
- Stop: n/a (never placed)
- Take-profit: n/a
- Time stop: n/a
- Routine: crypto-hourly
- Notes: Realized P&L ~+$0.13 (+3.69%). First Bull-Crypto action. Book now 100% cash at $97,382.43.
