# Guardrails — inviolable rules

These rules override any decision. If an action would violate a rule, **you do not act** and you log the situation in `learnings.md`. We operate in **catalyst-driven short-swing** regime, horizon 1-5 trading days per position.

## Investment universe

- **US-listed equities only** (NYSE, NASDAQ). No leveraged ETFs (TQQQ, SQQQ, SOXL, TMF, etc.). Classic ETFs OK (SPY, QQQ, IWM, sector ETFs).
- **Forbidden**: options, crypto, forex, futures, short selling, illiquid ADRs.
- **Liquidity required**: average daily volume > 2M shares (short-swing requires fast in/out). No penny stocks (< $5 share price). Market cap ≥ $2B (unless documented exception in research_log).

## Sizing & risk (conviction-based, parallel multi-positions)

- **Probe**: ~2% portfolio — first test.
- **Standard**: ~4% — solid setup, quality score ≥ 22/30.
- **High conviction**: ~5% (entry cap) — score ≥ 26/30, strong catalyst, macro aligned.
- **Top-up (ADD) forbidden** on short-swing: no averaging on a 1-5 day trade. Sized at entry or not sized.
- **Minimum cash**: ≥ 10% at all times. Target 15-20% in neutral regime, 25-35% in late-cycle/risk-off.
- **New positions max**: **5 per day** (short-horizon turnover is expected), **15 per week**.
- **Total positions max**: **20 concurrent** (parallel multi-positions are explicitly wanted).
- **Sector concentration**: no sector > 35% of portfolio (technology included). If exceeded, no new buy in that sector.
- **Catalyst concentration**: no more than 5 positions exposed to the same single event (e.g. don't hold 6 positions all depending on Wednesday's FOMC).

## Stops (1-5 day horizon)

- **Trailing stop 6%** placed at entry of every new position.
- **Cut -5%**: any position ≤ -5% unrealized at midday check. Tight stop because horizon is short — a multi-day thesis running -5% against you is very likely broken.
- **Tighten trailing to 3%** when position ≥ +10% unrealized.
- **Trim 50%** when position ≥ +15%, tighten 3% on the rest.
- **Time stop**: position held > 8 trading days with no remaining active catalyst → close at next midday or close.
- **Pre-earnings hold**: **never hold a position** through an earnings release unless explicitly stated and the BUY was designated as an "earnings play" in the research note. Default = exit the day before.

## Daily / weekly / drawdown caps

- **Daily loss cap**: day loss > 3% → freeze any new opens until the next day. No panic selling — let the stops work.
- **Weekly loss cap**: week at -5% → defensive mode (no new position next week, raise cash to 25%+).
- **Drawdown cap**: drawdown from ATH > 12% → strict defensive mode (no new position, cash ≥ 30%, weekly-review triggers full strategy audit).

## Regime & macro

- **Confirmed late-cycle or risk-off** (VIX > 25 over 5 days, HY spreads > 500bp, 2-10 inversion + abrupt un-inversion, hawkish Fed surprise): target cash 25-35%, max 5 active positions, focus on defensive setups and oversold-bounce on quality.
- **Violent regime shift** detected intra-week: notify Telegram `REGIME SHIFT`, tighten all stops to 3%, freeze new opens until next pre-market.
- **Major macro events this week** (FOMC, CPI, NFP, PCE, Powell testimony): default sizing one notch down (Standard → Probe) unless explicit alignment.

## Pre-earnings & events

- Holding through earnings = forbidden by default (see Stops).
- Holding through a major FOMC / CPI / NFP = allowed but forced 3% stop the day before.
- If a known catalyst is within 24h, no new sizing > Standard (4%).

## Mode

- **Paper by default** (`TRADING_MODE=paper` + `ALPACA_BASE_URL` on paper).
- **Live switch**: never without explicit human intervention documented in `learnings.md`.

## Hygiene

- **Never commit a secret**, never include a secret in a notification.
- **Never delete** entries from `trade_log.md` or `research_log.md`. Append only, no rewriting history.
- **ISO UTC date format** everywhere: `2026-04-20T13:45:00Z`.
- **Revenge trading forbidden**: if a ticker was cut in the last 5 trading days, re-entry only with an explicit new thesis and a "re-entry justified by …" line in research_log.
