# Research log — Crypto

Append-only. `crypto-hourly` runs append scan notes and idea tickets.

## Structure

- **crypto-hourly**: regime note (BTC dominance, ETH ratio, funding proxies, macro rates, DXY, key levels on majors) + ideas + actions
- **crypto-daily-review**: daily synthesis
- **crypto-weekly-review**: weekly outlook + setup map
- **crypto-monthly-review**: monthly macro + prompt evolution proposals

## Entries

### 2026-04-21T12:14:00Z — crypto-hourly (12:00 UTC cycle) — REGIME BASELINE (first run)

**Account state (Alpaca paper)**
- Equity: $97,382.43 · Cash: $97,382.43 (100.0% cash)
- Positions: 0 · Open orders: 0
- Auto-defense: inactive · Daily/weekly loss cap: inactive
- Note: the BTCUSD residue ($3.77) logged in equities learnings on 2026-04-20 no longer appears on the API (long_market_value=$0). Crypto book starts clean.

**Regime pulse**
- BTC $76,490 (+1.52% 24h) — bouncing off $74,195 support, below $78,785 resistance, RSI 63.9, MACD bullish. Range-bound.
- ETH $2,329 (+0.60% 24h) — ETH/BTC 0.03065, below 3-month high 0.0313 (April 15). Mildly bullish bounce off ratio lows.
- Total crypto mcap ~$2.63T, down >20% YTD from mid-2025 peak $4T → broader crypto weakness.
- Equities cross-read: QQQ $646.79 near 52W high $650 → risk-on in equities, divergence vs crypto.
- Sector risks: KelpDAO DeFi hack ($14B exodus) on April 20, US-Iran geopolitical tension, DXY not surfaced.
- Approved-universe snapshot:
  - **AVAX** $9.00 — rich dated-catalyst stack (CME AVAX futures May 4 2026, Coinbase MM program May 1, Bitwise ETF BAVA launched April 15, KB Kookmin L1 on AVAX, RWA TVL ~$2.1B). Technical weak (price in bear YTD trend, no breakout). CTQS est. C18/T10/Q10/S12 = ~50/100 → SKIP (below 60 threshold), WATCH for technical confirmation pre-May 4.
  - **DOT** $1.26-1.30 — March 2026 tokenomics upgrade already priced in; Hyperbridge exploit April 18 recovered. Sentiment bearish 83%, F&G 29. No forward dated catalyst. SKIP.
  - **BTC/ETH/SOL/LINK/MATIC** — no dated catalyst firing. SKIP.

**Regime classification: NEUTRAL** (baseline). Justification: BTC holding support + equities risk-on, but crypto mcap down YTD + DeFi hack + geopol tension prevent "risk-on" stamp. Not "risk-off" because BTC structure intact above $74K.

**Actions**: 0 (no positions to manage, no CTQS ≥ 60 BUY candidate).

**Watchlist for next run (16:00 UTC)**:
- AVAX breakout above recent resistance with volume → promotes CTQS technical to 15+, potentially BUY-able as pre-CME-futures probe
- BTC close above $78,785 with volume → risk-on shift, more aggressive posture
- BTC breakdown below $74,195 → risk-off shift, tighten posture

**Baseline**: this run establishes the crypto agent's reference regime. Next `crypto-daily-review` (23:00 UTC) will set the formal portfolio baseline (equity, BTC benchmark price) in `memory/crypto/portfolio.md`.
