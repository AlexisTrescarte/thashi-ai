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

## 2026-04-22 — Daily review (grade: C)

### Performance
- Equity: $97,382.43 (day +0.00%)
- Benchmark day (50% SPY + 50% QQQ): +1.36% | alpha day: -1.36%
  - SPY 703.91 → 711.20 = +1.04%
  - QQQ 644.24 → 655.085 = +1.68%
- Cumul baseline: N/A — baseline pas encore posée (portfolio.md template ; pas de snapshot market-close enregistré à date)

### Activity
- Trades opened today: 0
- Trades closed today: 0 (W:0 / L:0 / BE:0)
- Hit rate today: N/A | Avg R today: N/A
- Stops set within 5min on all new positions: N/A (0 new position)

### By setup (today)
- Aucun — 100% cash toute la session.

### What worked (2 lines)
- Discipline "conviction over activity" respectée : pas d'improvisation sur GEV à l'open alors que la note de ré-évaluation post-earnings était absente du research_log.
- Règle "market-open = execution only" a bien bloqué une entrée discrétionnaire sans pre-market frais, zéro violation guardrails.

### What didn't (2 lines)
- Aucun pre-market block le 21 (cap routines) ni le 22 → queue BUY vide alors que GEV publiait Q1 ce matin et que la note 20/04 l'avait flagué WATCH avec starter 3% conditionnel au rapport → cash drag -1.36% sur marché +1.36%.
- Résidu BTCUSD disparu de l'API sans ligne SELL/CUT dans trade_log : trou de traçabilité (liquidation présumée mais non auditable côté memory).

### Discipline log
- Guardrail violations: 0 — aucune
- Time stops honored: N/A (0 position)
- Stop updates logged: 0

### Carry-forward for tomorrow
- Aging (J+6+): aucune — 0 position
- Pre-earnings demain (23/04) : rien de dated dans la note 20/04 ; pre-market 23/04 devra balayer calendrier frais
- Pre-earnings J+N flaggés : GOOGL 29/04 (scénario B = attendre post-earnings) reste WATCH
- Macro 24h : neutre mercredi→jeudi ; FOMC 28-29 avril (hold 99,3%) ; cluster earnings J+2 (VRSN, BLK, BX, INTC) à surveiller
- Regime note : SPY 711.20 = nouveau close ATH, confirme poussée. Pas de flip. Posture late-cycle maintenue (CPI chaud, Fed hawkish)
- **Priorité pre-market demain (1)** : ré-évaluation GEV post-Q1 publié ce matin 22/04 → si beat + pas d'overshoot > 15% vs MA200, exécuter starter 3% (~$2,900) scénario A de la note 20/04
- **Priorité pre-market demain (2)** : audit trade_log pour confirmer liquidation résidu BTCUSD (ou ligne `[RÉCONCILIATION]` dans learnings si API≠log)

### Lesson of the day (1 line)
- Quand la note pre-market la plus récente dans `research_log.md` date de > 24h ET qu'un WATCH a un catalyseur daté J ou J-1, `market-open` doit logger `[PREMARKET-STALE]` dans `learnings.md` avec la liste des WATCH impactés, pour que le prochain pre-market traite en priorité un catch-up ciblé (évite le trou d'1 journée de cash drag comme aujourd'hui sur GEV).

### Grade coherence check
- Alpha -1.36% pousserait vers D, mais : (a) 0 trade = 0 perte réalisée, (b) discipline conforme à strategy.md ("cash is a position"), (c) cash drag résulte d'une limitation opérationnelle identifiée (cap routines → pre-market 21/04 pausé) et non d'une erreur de lecture. Grade **C** : pas A/B sans alpha positif ; pas D/F sans violation ni perte réalisée.
