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

### 2026-04-22T13:38:30Z — LESSON
**Context**: Run `market-open` du 22 avril 2026 (09:38 ET). Marché ouvert. Équité $97,382.43, cash $97,382.43 (100%), 0 positions, 0 ordres ouverts — le résidu BTCUSD observé les 20 avril n'apparaît plus côté API equities (présumé liquidé ou réattribué à l'agent crypto entre les runs). Aucun bloc pre-market du 21/04 ni du 22/04 dans `research_log.md` : la dernière entrée pre-market date du 20/04 et listait explicitement "AUCUN BUY" + GEV/GOOGL en WATCH (pas en BUY queue). GEV publie ses résultats Q1 ce matin pre-market mais le plan du 20/04 exigeait une ré-évaluation post-earnings avant toute entrée — cette ré-évaluation relève du pre-market, pas du market-open.
**Takeaway**: Scope `market-open` = execution only. Sans bloc pre-market frais listant une BUY queue, le comportement correct est no-op. Ne pas improviser sur GEV même si le setup initial est validé : la règle "pas de nouvelle idée à l'open" prime. Preflight tous verts (pas d'auto-defense, pas de daily/weekly cap, cash 100% ≫ 10%, 0 positions ≪ 30).
**Action**: Aucun ordre placé. Aucune réconciliation de stop (pas de position). Pas de notification Telegram (règle market-open : uniquement si ≥ 1 trade ou skip remarquable — ici, l'absence de queue n'est pas un skip mais un no-queue). Commit no-op pour trace. À surveiller au prochain pre-market : inclure GEV post-earnings dans la BUY queue si le setup tient.
**Agent**: equities

### 2026-04-23T13:37:30Z — LESSON
**Context**: Run `market-open` du 23 avril 2026 (09:37 ET). BUY queue pre-market = 3 noms : GEV (Probe 3%), VRT (Standard 4%), GOOGL (Probe 2.5%). Préflight vert (cash 100%, pas d'auto-défense, pas de loss cap, FOMC 28-29 > 24h, régime neutre lean risk-on). Au fetch des quotes à l'ouverture +6 minutes : **GEV** ask $1,140 / bid $1,086.84 → spread 4.66% (au-dessus du cap 0.5%) ET ask +14% vs plan price $1,000 (FOMO guard +2% violé). **VRT** ask $310.30 / bid $293.62 → spread 5.38% (au-dessus du cap 0.5%). **GOOGL** ask $339.41 / bid $339.31 → spread 0.029%, sain. Les deux rejets GEV/VRT sont mécaniques (liquidity anomaly + FOMO guard), pas thèse-driven.
**Takeaway**: Le book post-gap des leaders PEAD de la veille (GEV +13.75%, VRT beat+raise) ouvre avec des spreads énormes à l'open (< 10 min). La règle 0.5% est stricte par dessein pour éviter le slippage sur gap days. Deux options pour réduire le rejet : (1) planifier l'entrée sur l'intraday-scan 10:30 quand le book s'est calmé (spread < 0.5% attendu sur GEV/VRT après 30-60 min de tape) ; (2) utiliser un ordre limit proche du bid plutôt que market. Pour ce run, la discipline "pas d'override de guardrail" prévaut → SKIP des deux noms, re-tentative possible via intraday-scan 10:30 si spread normalisé ET price toujours dans la zone plan. Pour GEV spécifiquement, le FOMO guard tient indépendamment du spread (ask $1,140 >> plan $1,000+2%) : ne pas re-rentrer plus haut dans la journée.
**Action**: (1) GOOGL 7 @ $339.29 fillé ($2,375.03, 2.44% NAV), trailing stop 8% Alpaca natif placé @ $312.05 — position short-swing avec sortie mandatoire 28/04 close pré-earnings 29/04 AMC. (2) Trade-log entry complet. (3) GEV et VRT en attente : **intraday-scan 10:30** doit re-évaluer quotes. Si spread < 0.5% ET VRT encore dans zone plan, autoriser entrée au scan. Pour GEV, FOMO guard interdit toute re-entry > $1,020 aujourd'hui. (4) Activity floor partiellement satisfait : 1 BUY placé sur 3 visés ; 2 skips mécaniques à re-tenter ce jour via intraday-scan.
**Agent**: equities

### 2026-04-24T15:35:00Z — LESSON
**Context**: Run `intraday-scan` 10:30 CT du 24 avril 2026 (vendredi, slot 1/3). Équité $97,388.73, cash $95,007.40 (97.56%), 1 position ouverte (GOOGL 7 @ $339.29 → $340.11, +0.24% / +$5.74), 1 ordre ouvert (trailing stop 8% Alpaca natif, hwm $341.96, stop $314.60). Day P&L +0.009% (flat, last_equity $97,379.63). **Aucun bloc pre-market 2026-04-24 dans research_log** — dernier bloc date du 23/04. Pre-market de ce matin a apparemment été sauté ou n'a rien écrit. Macro du jour : Nasdaq +1.11%, S&P +0.49%, Dow -0.33% ; VIX ~20 stable ; INTC +record highs post-beat (6e beat consécutif, revenue $13.58B vs $12.41B, AI-CPU demand +40% YoY) ; DOJ abandonne enquête Powell ; extension ceasefire Israel-Liban. Pas de shift régime (VIX pas de spike, pas d'event crédit, pas de Fed hawkish, pas de choc géopol). Régime confirmé : neutral → lean risk-on.
**Takeaway**: (1) **Pathway A (pre-market WATCH trigger) inapplicable** sans bloc 2026-04-24 frais — la skill exige explicitement "today's pre-market research_log block", pas celui de la veille. Le WATCH conditionnel SMH de 2026-04-23 (""si INTC beat → breakout candidate"") est considéré stale et ne peut pas fire intraday sous Bull v2. À retenir : un bloc pre-market sauté empêche toute exécution Pathway A pour la journée ; seuls B/C restent ouverts mais avec un rappel CTQS complet obligatoire. (2) **Pathway B (nouveau catalyseur INTC beat+raise)** rejeté malgré la qualité du catalyseur : (a) chase au record-high risqué — la leçon du 23/04 sur GEV (ask $1,140 vs plan $1,000, +14% au-dessus) montre que les leaders post-beat s'ouvrent déjà fumés, et aucun framework-CTQS prêt ne permet de sizer proprement sans note de recherche ≥ 20min ; (b) **FOMC 28-29 avril + earnings GOOGL 29/04 AMC** — deux events majeurs à T+2 TDs → environnement event-heavy qui justifie une discipline renforcée ; (c) priorité reste à protéger le seul book actuel (GOOGL) plutôt qu'empiler du risque. (3) **Pathway C (technical-only)** : aucun setup propre surfacé — SPY/QQQ aux records sans mean-reversion, pas de failed-breakdown reclaim visible. (4) **GOOGL** : trailing 8% natif Alpaca fait son job — hwm $341.96 (auto-tracked), stop $314.60 (auto-computed) = one-way ratchet enforcé par l'API. Aucune intervention manuelle requise. Priority 10 HOLD strict. (5) **Activity floor** : 1 BUY placé sur 5 TDs (20/04-24/04) — sous le seuil ""≥1/3 TDs et ≥3/5 TDs"". Discipline prime ici : FOMC + earnings cluster interdisent le déploiement forcé. À re-évaluer proprement lundi 27/04 pre-market avec INTC/SMH/TXN en candidats PEAD.
**Action**: Aucun ordre placé. GOOGL HOLD. Stop trailing 8% natif intact (pas de replacement nécessaire — ratchet API). Pas de notification Telegram (règle intraday-scan : uniquement si ≥1 action OR regime shift OR daily loss cap OR BUY opportuniste — aucun déclencheur réuni). Priorités lundi 27/04 pre-market : (a) constater rebound/drift overnight des gap-up winners de vendredi (INTC, TXN, SMH) ; (b) préparer BUY queue fraîche pour le lundi et surtout pré-FOMC ; (c) sortie mandatoire GOOGL au close du 28/04 (J-1 earnings) ; (d) investiguer pourquoi le bloc pre-market 24/04 a été sauté (trigger claude.ai failed ? next_run_at mal configuré ?) — vérifier memory/runs.log et enable status du trigger pre-market.
**Agent**: equities
