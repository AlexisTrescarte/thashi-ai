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

### 2026-04-20T20:45:00Z — INCIDENT
**Context**: Daily-review 20/04 (15:40 CT). `portfolio.md` est encore à l'état template vierge (baseline_date, baseline_equity, baseline_SPY, baseline_QQQ vides) malgré le passage théorique du `market-close` à 15:00 CT. `git log` confirme qu'aucun commit `[market-close]` n'existe pour 2026-04-20 — le routine n'a pas tourné, ou a tourné sans écrire le snapshot ni pousser. Résultat : daily-review force à grader sans baseline benchmark ni ATH initial, ce qui dégrade la comparabilité vs benchmark pour toutes les reviews suivantes.
**Takeaway**: Le chaînage `market-close → daily-review` est critique. Sans snapshot, la comparaison benchmark, le tracking drawdown-auto-defense et le sizing des probes deviennent approximatifs. La daily-review ne doit jamais « proceed blind » : soit elle écrit elle-même la baseline à partir de l'API Alpaca, soit elle tag `[INCIDENT]` explicitement.
**Action**: (1) Ajouter au prompt de `daily-review` : vérifier que `portfolio.md` a été mis à jour aujourd'hui, sinon écrire la baseline depuis l'état live avant de noter ; (2) demain 21/04 en pré-market, vérifier que `market-close` tourne bien à 16:00 ET (15:00 CT) et pousse ; (3) priorité absolue au market-close de demain = écrire baseline_date=2026-04-21, baseline_equity, baseline_SPY, baseline_QQQ dans `portfolio.md` + initialiser ATH.
**Agent**: equities

### 2026-04-20T20:46:00Z — INCIDENT
**Context**: Résidu BTCUSD ($3.82, 0.000049999 BTC, +4.30% unrealized) non liquidé au 3e run consécutif après identification initiale au pre-market. Les scopes utilisateur (BUY-only au market-open) et l'absence d'appel `intraday-scan` ont reporté le SELL. La discipline demande qu'une position hors-univers soit purgée avant toute nouvelle ouverture — on accumule une dette de discipline qui ne coûte rien aujourd'hui mais invalidera la pureté du mandat dès le premier BUY actions.
**Takeaway**: Une règle « clore hors-univers au prochain run SELL-autorisé » n'est pas suffisamment contraignante si aucun run SELL-autorisé ne se produit. Il faut un escalator : après N runs sans liquidation, le run suivant (quel que soit son scope) a l'obligation explicite de liquider avant toute autre action.
**Action**: Proposer (via monthly-deep-review) un ajout au prompt `market-close` : « si une position hors-univers equities est détectée, la liquider systématiquement avant le snapshot ». En attendant, demain 21/04 : liquidation BTCUSD au premier run autorisé (intraday-scan ou market-close).
**Agent**: equities
