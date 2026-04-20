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

_(empty — first run will append here)_
