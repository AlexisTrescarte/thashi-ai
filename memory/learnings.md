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

### 2026-04-23T19:40:00Z — LESSON
**Context**: Run `intraday-scan` 14:30 CT (last-call) du 23 avril 2026. Marché ouvert (close 15:00 CT). Équité $97,381.94 · last_equity $97,382.43 → day P&L **-0.0005%** (flat). Cash $95,007.40 (97.56%). 1 position : GOOGL 7@$339.29, prix $339.22, P&L intraday -0.02% (-$0.49). 1 ordre ouvert : trailing stop 8% Alpaca natif, hwm $341.96, stop $314.60. Aucune entrée `intraday-scan` 10:30 ni 12:30 dans runs.log — les deux slots antérieurs semblent ne pas avoir tourné (GEV/VRT skips du market-open pas re-évalués en séance). Macro : VIX 18.92 (-2.97%), SPY +1.05%, QQQ stable → régime **neutral lean risk-on confirmé** (pas de shift). Nouvelle antitrust ad-tech (EDVA) remontée par WebSearch : connue et déjà listée dans la section Risques du research note (EU DMA + ad-tech en cours). Pichai a réaffirmé capex $175-185B — connu. Deal Merck-Gemini Enterprise = signal qui **renforce** la thèse Cloud. Stock trade flat (pas de cassure technique).
**Takeaway**: Grille P1-P10 sur GOOGL : P1 thèse intacte (pas de halt, pas de guidance cut, nouvelles neutres-à-positives) → pas de CUT. P2 earnings 29/04 AMC = mercredi, pas demain BMO ni tonight AMC → la règle last-call pre-earnings ne tire pas aujourd'hui (sortie mandatoire reste 28/04 close à l'intraday-scan 14:30 de mardi prochain). P3 time stop : âge 0 TD, short-swing J+5 non atteint. P4-P5 N/A (equity). P6 -0.02% ≫ -5%, pas de cut. P7 flat, pas de trim. P8 flat, pas de tighten. P9 stop 8% trailing déjà en place, one-way ratchet respecté (hwm $341.96, current $339.22 — pas de reset nécessaire). P10 HOLD. Last-call interdit tout BUY → GEV/VRT NON re-tentés (la re-tentative aurait dû se faire aux slots 10:30/12:30 qui n'ont pas tourné). Day P&L -0.0005% ≪ -4% → pas de daily loss cap.
**Action**: 0 CUT, 0 TRIM, 0 TIGHTEN, 0 STOP-UPDATE, 0 BUY (last-call exits-only). Stop GOOGL laissé tel quel (trailing 8% natif, honnête vs P&L flat). Pas de notification Telegram (règle intraday-scan : uniquement sur action ou regime shift — ici aucun des deux). À surveiller pour le market-close 15:00 CT : snapshot EOD + baseline benchmark à poser (SPY/QQQ close vs 20/04 baseline). À surveiller pour pre-market 24/04 : (a) pattern de slots intraday-scan manquants (10:30 + 12:30 sans run) — vérifier schedule RemoteTrigger si récurrent ; (b) résultats INTC AMC ce soir pour signal semis pour demain ; (c) GOOGL : plus que 3 TD jusqu'à sortie pré-earnings mandatoire.
**Agent**: equities
