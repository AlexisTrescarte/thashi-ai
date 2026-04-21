# Daily reviews — Equities

Append-only. Every trading day at 15:30 CT the `daily-review` routine appends a section here.

Purpose: distilled lessons of the day, fast retrospective, feeds weekly/monthly aggregation.

## Schema

```markdown
## YYYY-MM-DD — Daily review (grade: A/B/C/D/F)

### Performance
- Equity: $X (day {+/-X.XX}%)
- Benchmark day (SPY+QQQ blend): {+/-X.XX}% | alpha day: {+/-X.XX}%
- Trades closed: N (W/L/BE)
- Trades opened: N

### By setup (today)
- Earnings momentum: W-L $P&L
- PEAD: ...
- ...

### What worked (2 lines)
- ...

### What didn't (2 lines)
- ...

### Discipline
- Guardrail violations: N ({details})
- Stops set within 5min: yes/no
- Time stops honored: yes/no

### Carry-forward for tomorrow
- Aging watchlist: ...
- Pre-earnings tomorrow: ...
- Regime note: ...
```

## Reviews

## 2026-04-21 — Daily review (grade B)

### Performance
- Equity: $97,382.43 (day +0.00%)
- Benchmark day: n/a — baseline SPY/QQQ non capturée (market-close 20/04 n'a pas tourné) | alpha day: n/a
- Cumul baseline: n/a — baseline à poser au prochain market-close

### Activity
- Trades opened today: 0
- Trades closed today: 0 (W:0 / L:0 / BE:0)
- Hit rate today: n/a | Avg R today: n/a
- Stops set within 5min on all new positions: n/a (aucune nouvelle position)

### By setup (today)
- Aucun trade — journée flat, cash 100% ($97,382.43).

### What worked (2 lines)
- Discipline "conviction over activity" tenue au premier mardi earnings-cluster de la semaine (INTC/LMT/HON/AXP/NEE/BLK/BX aujourd'hui) : zéro exposition = zéro event risk absorbé, dry powder intact.
- Résidu BTCUSD liquidé hier soir (20/04 23:10 UTC, SELL 0,000049999 @ $75 797,33, realized ≈ +$0,14) → univers equities propre et conforme au mandat.

### What didn't (2 lines)
- Baseline portfolio.md toujours vide : le `market-close` du 20/04 n'a pas été exécuté → SPY/QQQ close non capturés → impossible de calculer alpha jour et cumul. Dette technique à régler dès le market-close de ce soir.
- `runs.log` non alimenté depuis le refactor Bull v2 ; aucune trace d'audit interne des routines du jour hors commits git.

### Discipline log
- Guardrail violations: 0 — none
- Time stops honored: n/a (aucune position)
- Stop updates logged: 0

### Coherence note on grade
- Pas de trade clos → métriques hit rate / R n/a. Alpha non mesurable (pas de baseline). Grade B retenu sur : (a) 0 violation, (b) cash dry-powder préservé au sommet historique, (c) décision pré-earnings documentée pre-market 20/04 et respectée. Pas de A car pas de contribution active ; pas de C car aucun signe de dérive.

### Carry-forward for tomorrow (2026-04-22)
- Aging (J+6+): aucune position.
- Pre-earnings tomorrow pre-market : **GEV Q1 2026** (22/04 avant open) — WATCH depuis 20/04. Plan : starter 3% (~$2 900) si beat + guidance 2026 tenue + prix < MA200 +30% + pas d'overshoot >15% post-rapport. Sinon attendre le retest de la première résistance cassée. Stop initial prévu : trailing 10%.
- Autres earnings 22/04 à surveiller : pre-market TMUS, BA, T, BSX, GD ; after-close META, IBM, NOW, CMG, LRCX, TSLA → cluster mega-cap tech = volatilité attendue sur QQQ.
- Macro 24h : pas de statistique US majeure prévue 22/04 (hebdo EIA pétrole seulement). Focus = tape des earnings.
- Regime note : SPY/QQQ toujours en zone ATH ; pas de shift confirmé aujourd'hui ; reste late-cycle → "conviction over activity" maintenu.

### Lesson of the day (1 line)
- Pour GEV post-earnings 22/04 : fixer **avant l'open** le prix max d'entrée (cap = MA200 +30% OU +15% au-dessus du close 21/04, le plus restrictif) et n'exécuter le starter **qu'après la 1ère 30-min-range** — pas de chase sur la cloche ; si gap > +15%, attendre le retest.

