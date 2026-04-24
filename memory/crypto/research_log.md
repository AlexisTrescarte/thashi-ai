# Research log — Crypto

Append-only. `crypto-hourly` runs append scan notes and idea tickets.

## Structure

- **crypto-hourly**: regime note (BTC dominance, ETH ratio, funding proxies, macro rates, DXY, key levels on majors) + ideas + actions
- **crypto-daily-review**: daily synthesis
- **crypto-weekly-review**: weekly outlook + setup map
- **crypto-monthly-review**: monthly macro + prompt evolution proposals

## Entries

### 2026-04-24T04:22:00Z — crypto-hourly (04:00 UTC scan, Asia overnight)

**Regime: NEUTRAL (constructive undertone — first crypto run, baseline)**

| Dimension | Read |
|---|---|
| BTC | ~$77K (sources $76,252 / $78,597), +0.20% 24h, +2.80% 7d, dominance 57-59%, ~-20% from recent ATH (~$96K) |
| ETH | $2,343, -1.98% 24h, ETH/BTC 0.0306-0.0313 (10-week high — early leadership rotation signal) |
| Total cap | $2.50-2.70T |
| Stablecoins | $300B+ (ATH — sidelined dry powder) |
| BTC ETF flows | 5 consecutive days net inflow ($238M latest, $411M April 16); cumulative AUM $96.5B |
| Equities cross-read | SPY -0.15%, QQQ -0.50% (mild softness, AI/tech weak, value bid) |
| DXY | 98.70 (firm, +2.1% YTD; 10Y at 4.06%) |
| Events | **FOMC April 29-30 (5 days out — binary risk window)**, no major network/protocol events on calendar |

**CTQS scan — 7-coin approved universe (BTC/ETH/SOL/LINK/AVAX/DOT/MATIC)**

- **BTC**: C12 (sustained ETF bid + FOMC fuse, no fresh dated catalyst this cycle) + T15 (consolidation above $75K support, no breakout) + Q18 (deepest liquidity, top quality) + S15 (institutional ETF bid persistent, sentiment cautious-neutral) = **~60/100** → just at Probe threshold. Borderline.
- **ETH**: C13 (on-chain activity ATH, stable supply ATH, ETH/BTC turn) + T13 (down -1.98% intraday, no breakout) + Q17 (top-tier quality, on-chain momentum) + S16 (ETH/BTC 10-week high = leadership rotation signal) = **~59/100** → just below crypto threshold (60). SKIP.
- **SOL / LINK / AVAX / DOT / MATIC**: no fresh dated catalysts surfaced this cycle. SKIP all.

**Decision: NO-OP this run (no actions).**

Rationale:
1. First crypto run — book is empty, 0 positions to manage, no historical activity-floor pressure.
2. BTC at ~60 CTQS is borderline. No fresh dated catalyst (ETF inflows are a sustained narrative, not an event with a fuse). Setup is consolidation, not breakout.
3. **FOMC April 29-30 (5d out)** = binary macro risk; entering a Probe today means tightening stops at the 28/04 scan ahead of the event. Cleaner to wait for either (a) a clean technical trigger (BTC reclaim of $80K with volume / ETH breakout above $2,400) or (b) a clearer FOMC bias.
4. ETH at 59/100 is below the 60 crypto threshold. Borderline reject.
5. Discipline: "trade often, but never recklessly". The first crypto run sets the tone — no force-fill.

**Watchlist for next runs (08:00, 12:00, 16:00, 20:00 UTC)**:
- BTC: trigger BUY-Probe if reclaim above $80K with volume confirm, or fresh dated catalyst (FOMC bias clarification)
- ETH: trigger BUY-Probe if break above $2,400 with ETH/BTC > 0.0315, or stables-flow surge confirming leadership rotation
- Watch for ETF flow break (5-day inflow streak ending = sentiment shift signal)
- Pre-FOMC (April 28 scan): tighten any open positions to 5% trail

**Account snapshot (Alpaca paper)**:
- Total equity: $97,381.10 · Cash: $95,007.40 · Equities long-side: $2,373.70 (GOOGL — owned by equities agent)
- Crypto positions: 0 · Crypto open orders: 0
- No drawdown auto-defense, no daily/weekly loss cap active

**Ops note**: Alpaca paper API hit `503 DNS cache overflow` on first 2 calls (account + positions). Recovered after backoff (5s, then 3s). No degradation flag warranted (transient infra), but worth watching at next run.
