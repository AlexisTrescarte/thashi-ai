# Portfolio — Crypto

> Source of truth = Alpaca crypto API. This file is a **snapshot** written at every `crypto-daily-review`. Before any decision, refresh via `python scripts/alpaca_crypto_client.py positions`.

## Latest snapshot

- **Date (UTC)**: 2026-04-23T04:12:24Z (first crypto-hourly run — baseline)
- **Account equity total (USD)**: $97,382.43 (shared with equities agent)
- **Crypto positions value**: $0.00
- **Cash (USD)**: $97,382.43
- **Crypto book NAV (30% cap of total)**: $29,214.73 max
- **Crypto allocation used**: 0.00%
- **BTC benchmark price (baseline anchor)**: $78,553
- **Performance vs BTC since baseline**: 0.00% (baseline run)
- **Regime (crypto)**: crypto-neutral (recovery bounce, unconfirmed)
- **Auto-defense active**: no
- **Daily/weekly loss cap active**: no

## Baseline

- **Starting capital**: $29,214.73 notional (30% of $97,382.43 shared NAV cap)
- **Baseline date (UTC)**: 2026-04-23T04:12:24Z
- **BTC baseline**: $78,553

## ATH tracking

- **ATH equity (crypto book)**: $0 (no positions yet)
- **ATH date**: —
- **Current drawdown from ATH**: 0.00%

## Open positions

_Regenerated from API at every `crypto-daily-review`. Format:_

| Symbol | Qty | Avg cost | Price | Value | P&L $ | P&L % | Entry (UTC) | Age (h) | CTQS | Style | Stop | TP | Catalyst |
|--------|-----|----------|-------|-------|-------|-------|-------------|---------|------|-------|------|----|----------|

_(empty — no crypto positions open)_

## Open risks

- First run of Bull-Crypto v2 — no book established. BTC +3.75% 24h recovery bounce after Q1 2026 weakness; ETH/BTC at 3-month high but below 0.035 durable-rotation threshold. Waiting for confirmed setup with dated catalyst before opening.
- Shared account with equities agent; aggregate crypto book hard-capped at 30% of total NAV.
