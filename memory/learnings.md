# Learnings & incidents

Append-only. What Bull discovers that's useful for future runs: trade lessons, technical incidents, strategy adjustments, rules that prevented a mistake, regime shifts, auto-defense triggers, loss caps.

## Schema

```
### YYYY-MM-DDTHH:MM:SSZ — {LESSON | INCIDENT | RULE-ADJUSTMENT | REGIME-SHIFT | DAILY-LOSS-CAP | WEEKLY-LOSS-CAP | DRAWDOWN-AUTO-DEFENSE | PUSH-FAIL | API-DEGRADED}
**Context**: {what happened}
**Takeaway**: {1-3 lines}
**Action**: {file modified / rule added / nothing}
**Agent**: {equities | crypto | shared}
```

## Entries

### 2026-04-21T00:00:00Z — RULE-ADJUSTMENT
**Context**: Claude Routines daily-run cap set at 15/day on the subscription plan; crypto-hourly at cadence `0 * * * *` (24 runs/day) alone blows the cap. Email received 2026-04-21 notifying that routines were paused.
**Takeaway**: Operational cap is a hard constraint. Total daily budget must fit 15 runs: equities ~5–6 + crypto daily-review 1 + periodic reviews 1–3 = 6–10 non-crypto-hourly slots. Leaves 5–9 slots for crypto-hourly. Chose 6/day (cron `0 */4 * * *`, runs at 00/04/08/12/16/20 UTC) — tightest configuration that fits even quarter-end days (worst case: 5 equities + monthly + quarterly + crypto-daily + crypto-monthly + 6 crypto-hourly = 15).
**Action**: (1) Edited `.claude/commands/crypto-hourly.md` description + cadence references; (2) edited `routines/crypto-hourly.md` cron to `0 */4 * * *`; (3) updated `CLAUDE.md`, `memory/strategy.md`, `memory/guardrails.md` crypto line, `routines/README.md`, `.claude/commands/crypto-daily-review.md` + `crypto-monthly-review.md` (regime tally from 6 runs, stop-update freq target ≥ 4/day or native trailing preferred). (4) Manual step: user must edit the routine `crypto-hourly` cron field in Claude Desktop to `0 */4 * * *`. **Flash-crash gap** is mitigated by native trailing stops on Alpaca (execute independently of runs) — prefer native over manual-trailing.
**Agent**: shared

### 2026-04-20T12:30:00Z — INCIDENT
**Context**: Premier run pre-market de Bull. `alpaca_client.py positions` révèle une position résiduelle **BTCUSD** de 0,000049999 BTC ($3,76 valeur de marché, cost basis $3,65, P&L +$0,11). Compte paper Alpaca avec crypto_status=ACTIVE, options_level=3, shorting_enabled=true — le compte a des autorisations plus larges que le mandat Bull.
**Takeaway**: `guardrails.md` interdit crypto/options/short/leveraged ETF sans ambiguïté pour l'agent equities. Même un résidu négligeable doit être clos pour que le portefeuille equities reflète strictement le mandat. Note: sous Bull v2, l'agent crypto peut détenir BTC — mais il s'agit ici d'un résidu hérité listé côté equities qui doit être liquidé.
**Action**: (1) Plan écrit dans research_log.md demandant au market-open de SELL le résidu BTCUSD ; (2) règle mnémotechnique : **à chaque run equities, vérifier que toutes les positions listées par l'API Alpaca appartiennent à l'univers autorisé (actions US + ETFs + long options uniquement)**. Toute position hors univers = liquidation prioritaire avant toute nouvelle ouverture.
**Agent**: equities

### 2026-04-20T12:31:00Z — LESSON
**Context**: Premier run. Équity $97,382.41 / cash $97,378.65 → baseline portefeuille à poser. `portfolio.md` mentionne un capital de départ théorique $100,000, mais le compte paper affiche déjà un écart de -$2,617 lié au résidu BTC acheté à $73,094. `last_equity` = $97,382.51 → journée précédente quasi identique.
**Takeaway**: La baseline pratique de suivi vs benchmark (50% SPY + 50% QQQ sous Bull v2) = équity au premier market-close de Bull (20 avril 2026). Les closes SPY et QQQ doivent être capturés au même moment. Sans ça, comparaison vs benchmark faussée dès le départ.
**Action**: À consigner par le run `market-close` du 20 avril 2026 — `memory/equities/portfolio.md` devra être rempli avec baseline_date=2026-04-20, baseline_equity=valeur close, baseline_SPY, baseline_QQQ.
**Agent**: equities

### 2026-04-20T14:36:00Z — LESSON
**Context**: Run `market-open` du 20 avril 2026. Marché ouvert (is_open=true, 09:36 ET). Équité $97,382.42, cash $97,378.65 (99,996%). Plan pre-market (note 2026-04-20T12:28:00Z) : **AUCUN BUY** aujourd'hui, cash préservé vu ATH + CPI chaud + cluster earnings. Instruction utilisateur explicite pour ce run : "UNIQUEMENT les idées BUY rédigées ce matin par pre-market".
**Takeaway**: Zéro trade placé = comportement conforme. La discipline "conviction over activity" de strategy.md valide un no-op. GEV reste en WATCH jusqu'au 22 avril post-earnings, GOOGL en WATCH jusqu'au 29 avril (scénario B).
**Action**: Aucun ordre. Pas de notification Telegram (règle market-open : uniquement si ≥1 trade).
**Agent**: equities

### 2026-04-20T14:36:30Z — INCIDENT
**Context**: Le plan pre-market demandait également de liquider le résidu BTCUSD ($3,77) au market-open. L'instruction utilisateur de ce run limite l'exécution aux **BUY uniquement**, ce qui exclut un SELL crypto. Tension entre pre-market (priorité = clore le résidu hors-univers) et scope du run (BUY only).
**Takeaway**: La contrainte utilisateur prime sur la note pre-market pour ce run. Le résidu BTCUSD reste ouvert ; il n'affecte ni le cash (99,996%) ni l'exposition (0,004% du portefeuille). À reprendre dès qu'un run autorise une action SELL (intraday-scan, market-close, ou l'agent crypto sous Bull v2).
**Action**: Résidu BTCUSD reporté. Le prochain run autorisé à vendre doit traiter ce reste en priorité avant toute nouvelle ouverture.
**Agent**: equities

### 2026-04-20T17:02:30Z — LESSON
**Context**: Run `midday` du 20 avril 2026 (legacy routine, remplacée par `intraday-scan` sous Bull v2). Marché ouvert (13:02 ET). Seule position = résidu BTCUSD (qty 0,000049999, unrealized_plpc +3,19%). Équité $97,382.42 vs last_equity $97,382.51 → day change ~0,00%. Aucune autre position actions US.
**Takeaway**: Règles midday legacy : cut à -7%, tighten à +15%. Sous Bull v2, `intraday-scan` remplace avec une grille P1-P8 (cut -5% equity / -8% crypto, trim +20%/+30% short-swing/swing+, tighten 3% trailing à +10%). Le résidu BTC reste ouvert pour un run ultérieur autorisé à liquider hors-univers equities.
**Action**: Aucun ordre. Pas de notification Telegram. Commit no-op pour trace.
**Agent**: equities

### 2026-04-21T15:31:38Z — LESSON
**Context**: Run `intraday-scan` slot 10:30 CT (2026-04-21). Alpaca confirme : equity $97,382.43, cash $97,382.43 (100%), 0 positions, 0 open orders. Day P&L = 0,00% (equity == last_equity). Aucune note pre-market postée pour 2026-04-21 ; dernier plan pre-market est celui du 2026-04-20 (GEV WATCH jusqu'au 22/04, GOOGL WATCH jusqu'au 29/04, aucun BUY prévu). Macro check : VIX ~18,87 (clôture 20/04), SPY/QQQ futures légèrement positifs, TSMC a relevé sa guidance 2026 (semis rebond), mais Hormuz "fermé ce matin", brut +5%, actions -0,4% en early trading. Audition du nominé Fed Kevin Warsh à 10:00 ET aujourd'hui. Cluster earnings INTC/LMT/HON/AXP ce soir.
**Takeaway**: Pas de regime-shift déclencheur (VIX pas +20%, pas de credit event, pas de surprise hawkish). Book vide → pas de décision P1-P10 à appliquer, pas de stop-update sweep. Opportunistic BUY bloqué : aucun nouveau catalyseur daté n'a émergé aujourd'hui, les WATCH (GEV/GOOGL) sont event-gated post-earnings. Discipline : ne pas forcer un BUY au sommet du marché sans note CTQS ≥ 70 dédiée. Cash 100% est cohérent avec "conviction over activity" face à ATH + Fed event risk + cluster earnings.
**Action**: Aucun ordre. Aucune notification Telegram (policy conditionnelle, zéro action). Commit no-op pour trace. À reprendre : pre-market 2026-04-22 doit couvrir la réaction GEV post-earnings et le verdict de l'audition Warsh.
**Agent**: equities
