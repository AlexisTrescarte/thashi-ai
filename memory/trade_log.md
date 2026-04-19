# Journal des trades

Append-only. **Ne jamais réécrire** une entrée passée. Format chronologique inverse (plus récent en haut).

## Schéma

```
### YYYY-MM-DDTHH:MM:SSZ — {BUY|SELL|TRIM|ADD} {TICKER} {qty}@{price}
- Order ID Alpaca : {id}
- Valeur : ${value}
- % portefeuille à l'entrée : {n}%
- Thèse : {1-3 lignes}
- Trailing stop : {n}% / pas de stop
- Routine source : {pre-market|market-open|midday|market-close|weekly-review|manual}
- Lien vers research_log : {date de la note de recherche correspondante}
```

---

## Entrées

_(vide — le premier run du bot ajoutera ici)_
