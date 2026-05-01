# Trade log — Equities

Append-only. **Never rewrite** a past entry. Reverse chronological (most recent on top).

## Schema

```
### YYYY-MM-DDTHH:MM:SSZ — {BUY|SELL|TRIM|CUT|ADD|TIGHTEN|STOP-UPDATE} {SYMBOL} {qty}@{price}
- Order ID: {id}
- Value: ${value}
- % NAV at entry: {n}%
- Instrument: {equity | ETF | leveraged-ETF | option}
- Style: {day | short-swing | swing | positional}
- CTQS: C{xx}/T{xx}/Q{xx}/S{xx} = {total}/100 → Conviction {Probe|Standard|High}, confidence {xx}%
- Setup type: {setup}
- Catalyst: {event + date} OR "technical-only"
- Thesis: {1-3 lines}
- Stop: {type + level}
- Take-profit: {level or "trailing only"}
- Time stop: {date or "n/a"}
- Earnings hold: {yes/no}
- Routine: {routine name}
- Research note: {timestamp}
- Notes: {anything else}
```

## Stop-update schema (subsequent updates)

```
### YYYY-MM-DDTHH:MM:SSZ — STOP-UPDATE {SYMBOL}
- Previous stop: {type + level}
- New stop: {type + level}
- Reason: {trailing / locked profit / regime / thesis reinforcement}
- Routine: {routine name}
```

## Entries

### 2026-05-01T13:47:06Z — BUY AAPL 16@$282.834375 (RECONCILIATION ENTRY — logged retroactively at 11:30 intraday-scan)
- Order ID: **191486fb** (market BUY, TIF=day, qty=16, filled_avg_price=$282.834375, status=filled)
- Trail stop placed 13 sec later: order **43ed6c8b-7221-419b-a8c9-9bf7d7de945c** (trailing_stop sell, qty=16, trail_percent=6%, TIF=GTC, HWM $287.22 at quote time, initial stop $269.9868). Native Alpaca trailing — one-way ratchet engaged.
- Value: $4,525.35 (16 × $282.834375)
- % NAV at entry: **4.64%** (vs equity $97,565 at fill — within 4.5-5.0% Standard plan band)
- Instrument: equity
- Style: short-swing, J+0..J+5 (time stop 2026-05-08 close)
- CTQS: C23/T18/Q23/S20 = **84/100** → Standard tier (upper bound), confidence 68% per pre-market note (notched from 75% for NFP-fog + gap-up + Mag-7 capex spillover)
- Setup type: PEAD (post-earnings drift) Pathway A — pre-market WATCH queue confirmed at open
- Catalyst: AAPL Q2 FY26 print 04-30 AMC — EPS $2.01 vs $1.95 · revenue $111.18B vs $109.66B · iPhone +22% YoY (iPhone 17 demand) · **Greater China $20.5B vs $16B = +28% YoY** · Services $30.98B beat · gross margin 49.3% record · Q3 guide raise to +14-17% YoY revenue. Stock +1.86% AH on print, gapped up to ~$283 area at open.
- Thesis: clean Mag-7 PEAD on the China + iPhone + GM trifecta, multi-day drift highly probable. 6-month range break setup (was ranging $245-280 since Nov 2025). Mega-cap defensive characteristics on a breadth-deteriorating tape = constructive.
- Stop: 6% trailing native (Alpaca trailing_stop sell GTC, id 43ed6c8b) @ $269.9868 initial, HWM $287.22.
- Take-profit: trailing only (let PEAD run; one-way ratchet on the trail).
- Time stop: **2026-05-08 close** (J+5 short-swing horizon). Earnings hold: NO (next AAPL earnings late July 2026, well outside window).
- Routine: market-open (placed) → intraday-scan 11:30 (reconciled this run).
- Research note: memory/equities/research_log.md — 2026-05-01T11:27:37Z pre-market block, AAPL BUY queued verdict.
- Pre-trade gate (inferred from fill — actual run lost): pretrade_guards must have passed (order is filled, no rejection). Spread at fill window expected <0.05% on AAPL super-liquid name; FOMO guard (ask ≤ $310) easily satisfied at $283; NFP deferral (catastrophic miss → defer) was a non-issue because **NFP was actually rescheduled to 05-08, not released today** — so the macro-fog notch-down was already over-conservative on the entry.
- **RECONCILIATION**: this trade was placed by the market-open routine on 05-01 at 13:47:06Z (08:47 CT, 17 min after the 08:30 CT bell — same pattern as the GOOGL 04-30 reconciliation) but the journal failed to commit. **No 05-01 market-open block in research_log, no 05-01 market-open commit in git log** (last commit before this run is 96638cf = the 05-01 pre-market). The Alpaca order history (`alpaca_client.py orders --status all`) is the source of truth for the fill. **Fourth journal-commit failure in 6 trading days** (04-25 weekend, 04-27 partial pre-market, 04-30 pre-market+market-open both failed, 05-01 market-open). Surfaced as a fresh `[HARNESS-GAP]` entry in learnings and queued for monthly-review evolution proposal alongside the GTD-exit-at-fill remediation and journal-commit-retry remediation.
- Status at this scan (16:40 UTC = 11:40 CT): open J+0 · mark $283.39 · +$8.89 (+0.20%) · trail engaged (HWM $287.22 / stop $269.99 = 4.65% buffer below mark) · in-thesis. **Action this scan: HOLD** (no priority trigger, native trail handling exit risk).


### 2026-04-23T13:37:07Z — BUY GOOGL 7@$339.29
- Order ID: 1e58b2d7-9039-45bf-8b10-06e39c32f2d1 (stop: 45d94a3c-d7c9-44f6-bc8d-e6d38c6afef0)
- Value: $2,375.03
- % NAV at entry: 2.44%
- Instrument: equity
- Style: short-swing (3-4 trading days, pre-earnings exit mandatory)
- CTQS: C20/T19/Q18/S18 = 75/100 → Conviction Standard, downsized to Probe, confidence 55%
- Setup type: pre-earnings momentum + TPU/Anthropic catalyst reinforcement
- Catalyst: Earnings Q1 2026 on 2026-04-29 AMC (J-4 trading days). Secondary fuse: TPU 8t/8i launch + Anthropic multi-GW commitment announced 22/04.
- Thesis: Gemini 3 traction (750M MAU, +87% in 9 months), antitrust Mehta resolved Sep 2025, Cloud accelerating, TPU validated by Anthropic → convergence of signals pre-earnings. Scenario A activated (vs prior preference for post-earnings entry) due to 22/04 catalyst cluster.
- Stop: 8% trailing (Alpaca native, id 45d94a3c) @ $312.05 initial, hwm $339.185
- Take-profit: trailing only
- Time stop: 2026-04-28 close (mandatory pre-earnings exit)
- Earnings hold: NO (exit 28/04 close)
- Routine: market-open
- Research note: memory/equities/research_log.md — 2026-04-23 pre-market block, BUY 3
- Notes: Probe sizing $2,435 target; 7 shares × $339.29 = $2,375.03 (2.44% NAV — just under target but within Probe band 2-3%). GEV and VRT from the same BUY queue skipped at open due to wide spreads (GEV 4.66%, VRT 5.38% — early-open thin books) and FOMO guard on GEV (ask +14% vs plan $1,000).

### 2026-04-28T19:59:57Z — TRIM GOOGL 4@$349.85 (MOC partial fill)
- Order ID: 33e1dd7d-7c7f-4b2d-9d1f-2ecace102f20 (TIF=cls, qty=7 placed, qty=4 filled, qty=3 expired)
- Replaces native trailing stop 45d94a3c (canceled 2026-04-28T13:41:54Z when MOC was placed at market-open)
- Filled value: $1,399.40 (4 shares × $349.85 close auction)
- Realized P&L on the 4 shares: ($349.85 − $339.29) × 4 = +$42.24 (+3.11%)
- Reason: pre-earnings exit pre-staged at market-open per 04-27 daily-review carry-forward (post-04-24 INCIDENT remediation: exchange-bound exit not run-dependent). MOC partial-fill mechanics — 3/7 shares left unfilled at the close auction (Alpaca cls TIF expired at 20:02:20Z with filled_qty=4).
- Routine: market-open (placed) → market-close (audit + residual-cleanup follow-up)
- Notes: Partial fill is an unusual outcome on a $2T mcap name. Likely auction-imbalance routing chose to fill only 4/7 lots. Followup CUT for residual 3 shares queued same session — see 2026-04-28T20:10:26Z entry.

### 2026-04-29T13:31:25Z — CUT GOOGL 3@$345.71 (DAY market sell filled at the open)
- Order ID: c9a545bd-3caa-41ae-a9ef-a4d084c37255 (status=filled, filled_qty=3, filled_avg_price=$345.71)
- Submitted: 2026-04-28T20:10:26Z post-close · Filled: 2026-04-29T13:31:25Z (09:31 ET regular open, ~1 minute after the bell)
- Filled value: $1,037.13
- Realized P&L on the 3 shares: ($345.71 − $339.29) × 3 = +$19.26 (+1.89%)
- Total realized P&L on the GOOGL trade (4 shares MOC 04-28 + 3 shares DAY 04-29): +$42.24 + $19.26 = +$61.50 on $2,375.03 entry = +2.59% return on the position
- Reason: pre-earnings exit (no earnings hold). Earnings Q1 2026 = 2026-04-29 AMC (~20:00 UTC today). Exit at the regular open captured >6h margin before the print.
- Routine: market-open (verify-and-confirm — order placed at market-close 04-28; verified filled and tallied this run)
- Notes: GOOGL position fully closed. Net trade P&L +$61.50 / +2.59%; holding period 4 trading days (J+0 to J+4). Reinforces the 04-27 carry-forward and 04-24 INCIDENT remediation: queue-during-day market sell + DAY/GTD TIF + 14:30 last-call IOC fallback is the correct pre-earnings exit pattern (MOC TIF=cls alone can leave residual on partial fill). Book post-fill: 0 positions, 100% cash.

### 2026-04-28T20:10:26Z — CUT GOOGL 3 shares (DAY market sell, queued for 04-29 open)
- Order ID: c9a545bd-3caa-41ae-a9ef-a4d084c37255 (TIF=day, qty=3, market, status=accepted)
- Submitted post-close (20:10 UTC = 15:10 CT, 10 min after the bell)
- Expires: 2026-04-29T20:00:00Z (tomorrow's regular close) → will execute at tomorrow 13:30 UTC = 09:30 ET regular open
- Mark at queue: $349.62 (last trade) → notional ≈ $1,048.86
- Reason: cut pre-earnings — MOC partial-fill residual, no earnings hold. Earnings GOOGL Q1 2026 = 2026-04-29 AMC (~20:00 UTC tomorrow) → exit at tomorrow's regular open is well before the print and satisfies the no-earnings-hold guardrail.
- Routine: market-close (last-call)
- Notes: Considered extended-hours limit sell now (16:00-20:00 ET window) but Alpaca post-close quote was one-sided (bid $329.20 / ask $0) = no real liquidity at the moment of placement. DAY market sell is the safer mechanic — captures tomorrow's regular-session opening cross on a deep mcap. Reinforces the 04-24 INCIDENT remediation lesson: MOC TIF=cls is not deterministic on partial fills; for next pre-earnings exit, prefer queue-during-day market sell + GTD or use limit-IOC at the 14:30 last-call rather than rely on the close auction alone.

### 2026-04-30T13:47:31Z — BUY GOOGL 7@$369.7114 (RECONCILIATION ENTRY — logged retroactively at 11:30 intraday-scan)
- Order: market BUY filled 2026-04-30T13:47:31Z (08:47 CT, ~17 min after the 08:30 CT bell), qty=7, type=market, filled_avg_price=$369.7114, side=long.
- Cost basis: $2,587.98 → **2.65% NAV at fill** (Probe band 2-3%).
- Trail stop placed 10 sec later: order **74ec67e0-c744-45ca-a7dd-521b72caacf2** (trailing_stop sell, qty=7, trail_percent=7%, TIF=GTC, HWM $378.365 at quote time, stop $351.879). Native Alpaca trailing — one-way ratchet engaged.
- Reason: post-earnings PEAD entry on **GOOGL Q1 2026 beat** (revenue $109.9B vs $107.2B est, Cloud +63% to $20.02B vs $18.05B est, EPS beat). Earnings printed 04-29 AMC; stock gapped up ~+5.7% from 04-29 close $349.94 to fill price. **Pathway B opportunistic catalyst** (catalyst surfaced overnight, executed at next routine).
- **RECONCILIATION**: this trade was placed by the market-open routine on 04-30 but the journal failed to commit. No 04-30 pre-market block, no 04-30 market-open commit in git log (last commit before this run is 2949743 = the 04-30 prompt-evolution feat). The Alpaca order history is the source of truth for the fill. **Third journal-commit failure this week** — surfaced as `[HARNESS-GAP]` in learnings and queued for monthly-review evolution proposal alongside the GTD-exit-at-fill remediation.
- Routine: market-open (placed) → intraday-scan 11:30 (reconciled this run).
- Style/horizon: short-swing PEAD, J+0..J+5 (time stop on day J+5 = 2026-05-07 close); next earnings late July 2026 → no earnings-hold conflict.
- Status at this scan (16:35 UTC = 11:35 CT): open J+0 · mark $377.01 · +$51.09 (+1.97%) · trail engaged · in-thesis. **Action this scan: HOLD** (no priority trigger, trail ratcheting natively).


### 2026-04-30T18:41:35Z — BUY LLY 5@$939.54 (Pathway-B PEAD opportunistic, intraday-scan 13:30)
- Order ID: **4173f753-7f94-462e-a889-46b56bc8cce4** (market BUY, TIF=day, qty=5, filled_avg_price=$939.54, status=filled).
- Trailing stop placed 11 sec after fill: order **8e54102c-158f-4d66-bdd3-3270ebb7de39** (trailing_stop sell, qty=5, trail_percent=7%, TIF=GTC, HWM $938.34 at quote time, initial stop $872.6562). Native Alpaca trailing — one-way ratchet engaged.
- Cost basis: $4,697.70 (5 × $939.54). Filled at ~+0.155% above ask quote ($938.09 → $939.54) — small market-order cross with NEUTRAL microstructure verdict (QI -0.333 ask pressure).
- **Sizing: 4.82% NAV** ($4,697.70 / $97,543.02). Standard tier mid-band (4-6%).
- CTQS: C22/T17/Q22/S19 = **80/100** → Standard conviction, confidence 70% (Late-day entry on D+0 PEAD discounts confidence 5pp from a clean-morning 75%).
- Setup type: post-earnings drift (PEAD) on Q1 2026 beat+raise.
- Catalyst: **Q1 2026 print today AM** — revenue $19.8B (+56% YoY) vs $17.5B est; EPS $8.55 vs $6.85 est (+24.82% beat); Mounjaro WW $8.66B (+125% YoY) vs $7.26B est; Zepbound US $4.1B (+79% YoY); FY2026 revenue raised $80-83B → $82-85B; FY2026 adj EPS raised to $35.50-$37 ($36.25 mid, +5.8%).
- Thesis: Day-1 PEAD continuation on textbook beat-and-raise. Multi-day drift (3-5 sessions) backed by upgrade-cluster expectation, defensive sector fit (breadth 53% > MA50), GLP-1 monopoly with NVO. Target: capture $30-50 of continuation drift over horizon = +3 to +5% on the position ($150-250 unrealized).
- Stop: 7% trailing (Alpaca native, GTC, id 8e54102c) @ $872.6562 initial, HWM $938.34.
- Take-profit: trailing only (let PEAD run; one-way ratchet on the trail).
- Time stop: **2026-05-07 close** (J+5, short-swing horizon). Earnings hold: NO (next earnings ~late July 2026, well outside window).
- Routine: intraday-scan 13:30 (Pathway-B opportunistic — spread normalized from 2.14% at 11:30 to 0.097% at 13:37, qualifying for re-evaluation).
- Pre-trade gate: pretrade_guards PASS (killswitch ✓, fat_finger ✓, notional ✓, rate_limit ✓); microstructure NEUTRAL with spread 14.8 bps ≤ 20 bps Standard-tier threshold → cleared.
- Research note: memory/equities/research_log.md — 2026-04-30T18:40:00Z BUY verdict.
- Notes: Late-day D+0 PEAD entry (~1h20 to close) — accepted risk. The 11:30 scan flagged LLY for spread re-eval; 12:30 missed (harness gap); 13:30 caught the spread normalization. Activity floor progress: rolling 5td now 3 BUYs (GOOGL 04-23 close-out, GOOGL 04-30 fresh, LLY 04-30) — meets ≥3 target. Daily Pathway-B/C cap usage: 2/5 (GOOGL morning + LLY now); 3 BUYs remaining today but slot 14:30 is exits-only so effective cap reached. Sector mix post-buy: GOOGL ~2.7% tech + LLY 4.82% healthcare = 7.52% total, well under all caps. Cash post-buy ~92.4%.
