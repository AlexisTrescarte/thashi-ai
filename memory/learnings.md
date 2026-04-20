# Learnings & incidents

Append-only. Ce que Bull découvre d'utile pour les runs futurs : leçons de trades, incidents techniques, ajustements à la stratégie, règles qui ont empêché une bêtise.

## Schéma

```
### YYYY-MM-DDTHH:MM:SSZ — {LESSON | INCIDENT | RULE-ADJUSTMENT}
**Contexte** : {ce qui s'est passé}
**Ce que j'en tire** : {1-3 lignes}
**Action** : {fichier modifié / règle ajoutée / rien}
```

---

## Entrées

### 2026-04-20T12:30:00Z — INCIDENT
**Contexte** : Premier run pre-market de Bull. `alpaca_client.py positions` révèle une position résiduelle **BTCUSD** de 0,000049999 BTC ($3,76 valeur de marché, cost basis $3,65, P&L +$0,11). Compte paper Alpaca avec crypto_status=ACTIVE, options_level=3, shorting_enabled=true — le compte a des autorisations plus larges que le mandat Bull.
**Ce que j'en tire** : `guardrails.md` interdit crypto/options/short/leveraged ETF sans ambiguïté. Même un résidu négligeable doit être clos pour que le portefeuille reflète strictement le mandat. Le P&L du résidu doit être consigné dans trade_log quand liquidé. En pre-market, aucun ordre placé — c'est au market-open de liquider.
**Action** : (1) Plan écrit dans research_log.md demandant au market-open de SELL le résidu BTCUSD ; (2) règle mnémotechnique ajoutée ici : **à chaque run, vérifier que toutes les positions listées par l'API Alpaca appartiennent à l'univers autorisé (actions US non-leveraged uniquement)**. Toute position hors univers = liquidation prioritaire avant toute nouvelle ouverture.

### 2026-04-20T12:31:00Z — LESSON
**Contexte** : Premier run. Équity $97,382.41 / cash $97,378.65 → baseline portefeuille à poser. `portfolio.md` mentionne un capital de départ théorique $100,000, mais le compte paper affiche déjà un écart de -$2,617 lié au résidu BTC acheté à $73,094. `last_equity` = $97,382.51 → journée précédente quasi identique.
**Ce que j'en tire** : La baseline pratique de suivi vs SPY = équity au premier market-close de Bull (aujourd'hui, 20 avril 2026). Le prix SPY doit être capturé au même moment. Sans ça, comparaison vs SPY faussée dès le départ.
**Action** : À consigner par le run `market-close` du 20 avril 2026 — `portfolio.md` devra être rempli avec baseline_date=2026-04-20, baseline_equity=valeur close, baseline_SPY=close SPY.

### 2026-04-20T14:36:00Z — LESSON
**Contexte** : Run `market-open` du 20 avril 2026. Marché ouvert (is_open=true, 09:36 ET). Équité $97,382.42, cash $97,378.65 (99,996%). Plan pre-market (note 2026-04-20T12:28:00Z) : **AUCUN BUY** aujourd'hui, cash préservé vu ATH + CPI chaud + cluster earnings. Instruction utilisateur explicite pour ce run : "UNIQUEMENT les idées BUY rédigées ce matin par pre-market".
**Ce que j'en tire** : Zéro trade placé = comportement conforme. La discipline "conviction over activity" de strategy.md valide un no-op. GEV reste en WATCH jusqu'au 22 avril post-earnings, GOOGL en WATCH jusqu'au 29 avril (scénario B).
**Action** : Aucun ordre. Pas de notification Telegram (règle market-open : uniquement si ≥1 trade).

### 2026-04-20T14:36:30Z — INCIDENT
**Contexte** : Le plan pre-market demandait également de liquider le résidu BTCUSD ($3,77) au market-open. L'instruction utilisateur de ce run limite l'exécution aux **BUY uniquement**, ce qui exclut un SELL crypto. Tension entre pre-market (priorité = clore le résidu hors-univers) et scope du run (BUY only).
**Ce que j'en tire** : La contrainte utilisateur prime sur la note pre-market pour ce run. Le résidu BTCUSD reste ouvert ; il n'affecte ni le cash (99,996%) ni l'exposition (0,004% du portefeuille). À reprendre dès qu'un run autorise une action SELL (midday, market-close, ou instruction explicite).
**Action** : Résidu BTCUSD reporté. Le prochain run autorisé à vendre doit traiter ce reste en priorité avant toute nouvelle ouverture.
