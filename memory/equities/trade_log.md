# Trade log — Equities

Append-only. **Never rewrite** a past entry. Reverse chronological (most recent on top).

## Schema

```
### YYYY-MM-DDTHH:MM:SSZ — {BUY|SELL|TRIM|CUT|ADD|TIGHTEN|STOP-UPDATE} {SYMBOL} {qty}@{price}
- Order ID: {id}
- Value: ${value}
- % NAV at entry: {n}%
- Instrument: {equity | ETF | leveraged-ETF | option}
- Style: {day | short-swing | swing | positional}
- CTQS: C{xx}/T{xx}/Q{xx}/S{xx} = {total}/100 → Conviction {Probe|Standard|High}, confidence {xx}%
- Setup type: {setup}
- Catalyst: {event + date} OR "technical-only"
- Thesis: {1-3 lines}
- Stop: {type + level}
- Take-profit: {level or "trailing only"}
- Time stop: {date or "n/a"}
- Earnings hold: {yes/no}
- Routine: {routine name}
- Research note: {timestamp}
- Notes: {anything else}
```

## Stop-update schema (subsequent updates)

```
### YYYY-MM-DDTHH:MM:SSZ — STOP-UPDATE {SYMBOL}
- Previous stop: {type + level}
- New stop: {type + level}
- Reason: {trailing / locked profit / regime / thesis reinforcement}
- Routine: {routine name}
```

## Entries

_(empty — first run will append here)_
