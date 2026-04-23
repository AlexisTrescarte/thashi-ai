# Research log — Crypto

Append-only. `crypto-hourly` runs append scan notes and idea tickets.

## Structure

- **crypto-hourly**: regime note (BTC dominance, ETH ratio, funding proxies, macro rates, DXY, key levels on majors) + ideas + actions
- **crypto-daily-review**: daily synthesis
- **crypto-weekly-review**: weekly outlook + setup map
- **crypto-monthly-review**: monthly macro + prompt evolution proposals

## Entries

### 2026-04-23T00:40:30Z — crypto-hourly (00:00 UTC slot, FIRST CRYPTO RUN, baseline)

**Account state (Alpaca, shared with equities agent)**
- Equity: $97,382.43 · Cash: $97,382.43 (100%) · Positions: 0 · Open orders: 0
- Crypto book exposure: 0% of NAV (cap 30%)
- No auto-defense / daily-cap / weekly-cap active

**Regime pulse**
| Dim | Reading |
|---|---|
| BTC | $78,924 · 24h +3.75% to +4.49% (mixed sources) · 24h range $74,935-$79,389 (volatile bounce) · dominance ~57-61% |
| ETH | ~$2,305 · ETH/BTC ~0.0306-0.0313 (3-month high mid-April, hint of alt rotation) |
| SOL | $87.57 · +3.88% 24h |
| AVAX | $9.36 · +1.72% 24h |
| DOT | $1.26 · -6% 24h (laggard) |
| MATIC | ~$0.23 (sparse data) |
| LINK | data sparse — skip |
| Total cap | $2.50T (post-Q1 pullback from highs) |
| Stables | $317B (ATH ~$316B Q1 — large dry powder) |
| BTC ETF flows | -$325M outflow on 2026-04-13 (recent negative) |
| ETH ETF flows | +$7.7M daily, +$187M weekly (best week of 2026) |
| Equities cross | QQQ $647.97 close 2026-04-21; ceasefire extension lifted tape 2026-04-22 |
| DXY | 4-year low (USD weakness — crypto-supportive) |
| Events | Geopol ceasefire extension, no FOMC/CPI within 24h |

**Regime classification**: **NEUTRAL leaning risk-on**. BTC reclaiming $79k after $74.9k flush, DXY weak, equities firmer, ETH/BTC firming. Caveats: BTC ETF flows still net-negative this month, total cap below cycle highs, DOT bleeding. Not yet confirmed risk-on (need BTC > $79.4k breakout + sustained ETF inflows).
**Shift vs prior**: N/A — this is the baseline regime note for the crypto agent.

**Per-position management**: Book empty → P1-P7 not applicable.

**CTQS scan (7-coin universe, threshold ≥ 60 BUY / ≥ 70 technical-only Probe)**
| Coin | C/T/Q/S | Total | Verdict | Disqualifier |
|---|---|---|---|---|
| BTC | 8/14/12/10 | 44 | SKIP | mid-bounce, no dated catalyst, ETF flows net-neg |
| ETH | 8/14/14/14 | 50 | SKIP | ETF flows turning + ETH/BTC firming, but no dated catalyst, marginal |
| SOL | 8/15/12/10 | 45 | SKIP | momentum without catalyst |
| LINK | n/a | <55 | SKIP | sparse data, no catalyst surfaced |
| AVAX | 7/12/10/9 | 38 | SKIP | mild bounce, no thesis |
| DOT | 5/8/9/8 | 30 | SKIP | -6% laggard |
| MATIC | n/a | <55 | SKIP | sparse data, no catalyst |

**Decision**: 0 BUY (all candidates < 60). No-op on dispatch. Activity floor n/a — none of the seven coins surface a CTQS ≥ 60 candidate; per crypto skill the floor is implicit (only act on real conviction).

**Actions taken this run**: baseline portfolio.md initialised (snapshot + baseline + ATH tracking), research_log seeded.

**Telegram**: NOT sent (no action, no regime shift to/from risk-off, no cap, no API issue).

**Next run**: 2026-04-23T04:00Z (4h cadence). Watch for BTC clearing $79.4k on volume, ETH ETF flow continuation, and any dated catalysts on the seven coins.
