# Research log — Crypto

Append-only. `crypto-hourly` runs append scan notes and idea tickets.

## Structure

- **crypto-hourly**: regime note (BTC dominance, ETH ratio, funding proxies, macro rates, DXY, key levels on majors) + ideas + actions
- **crypto-daily-review**: daily synthesis
- **crypto-weekly-review**: weekly outlook + setup map
- **crypto-monthly-review**: monthly macro + prompt evolution proposals

## Entries

### 2026-04-24T16:03:50Z — crypto-hourly (baseline / first run)

**Regime pulse**
- BTC $77,736 · 24h -0.14% · dominance ~59% (high → risk-off rotation within crypto)
- ETH $2,343 · 24h -1.98% · ETH/BTC ~0.0313 (below Jan 0.038 high, above Feb 0.028 low)
- Total crypto cap ~$2.62–2.70T · stables supply ATH $180B
- SOL $85.94 · 24h +0.70% · 7d +3.40% (71% below ATH)
- LINK $9.31 · AVAX ~$9 (testing key support post-KelpDAO hack) · DOT n/a · MATIC/POL n/a
- Macro cross-read: QQQ $655.95 firm, SPX 84% correlation, crypto increasingly macro-liquidity proxy
- Event of the day: **$8.6B BTC/ETH options expiry April 24** — expected to pin prices + increase realized vol
- ETF flows: tepid ($96.4M BTC spot inflows April 22)

**Regime classification**: NEUTRAL lean risk-off (BTC dominance rotation, options expiry pinning, ETH weakness). No shift callable — this is the baseline.

**Account state**: shared Alpaca paper account. Equity $97,420.16, cash $95,007.40, 1 GOOGL equities position $2,412.76, 0 crypto positions, 0 open crypto orders. Paper mode.

**CTQS scan (7-coin approved universe, all SKIP)**
| Coin | C | T | Q | S | Total | Verdict | Primary disqualifier |
|------|---|---|---|---|-------|---------|----------------------|
| BTC  | 10 | 12 | 15 | 10 | 47 | SKIP | No dated catalyst, options expiry pinning, $77-78k range, dominance-led rotation (defensive) |
| ETH  | 8 | 10 | 12 | 10 | 40 | SKIP | ETH/BTC weak, options expiry pinning, no near-term fuse |
| SOL  | 13 | 15 | 12 | 12 | 52 | SKIP | Alpenglow upgrade pushed to late 2026 (catalyst decayed); tokenization narrative positive but no dated fuse this week |
| LINK | 14 | 13 | 11 | 10 | 48 | SKIP | Data Streams upgrade (April 12) stale; RWA narrative long-term; no dated fuse |
| AVAX | —  | —  | —  | —  | —  | AVOID | Thesis risk active — KelpDAO hack April 20 → TVL -6.61%; testing $9 support |
| DOT  | 6 | 9 | 9 | 8 | 32 | SKIP | No identifiable near-term catalyst |
| MATIC/POL | 8 | 10 | 10 | 9 | 37 | SKIP | Giugliano Hard Fork (April 8) stale; Gigagas long-term roadmap, no dated fuse |

**Decision**: 0 BUY · 0 manage · book empty. Structurally, crypto options expiry today = volatility event; wait for post-expiry clarity before deploying capital. Reassess at next 4h run (20:00 UTC).

**Activity floor**: floor rules are equity-agent scoped; crypto has no activity floor in strategy.md. Regardless, baseline run with empty book justifies 0 BUY.

**API note**: two transient 503s on positions and open orders endpoints ("DNS cache overflow") — both recovered on single retry with 2s/4s backoff. Not persistent, no degraded-mode notification. Tracking for pattern.

