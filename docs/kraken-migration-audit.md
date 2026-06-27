# Kraken Migration Audit — Bull v2

**Date:** 2026-06-27
**Scope:** Feasibility audit only. No code changes, no live migration. Assesses whether the existing bots can move to Kraken (instead of the venue the user believes is "Hyperliquid"), the fee impact, and whether a second bot on Kraken tokenized stocks (xStocks) is viable in the EEA.
**Trigger:** Binance lost / did not obtain its MiCA (CASP) authorization to serve EEA retail; the user must move crypto funds to a MiCA-licensed venue (Kraken).

---

## 0. Reality check — what the code actually does today

This is the most important correction before any migration discussion. The audit of the codebase contradicts the mental model in the request.

| User's belief | What the repo actually contains |
|---|---|
| "My bots run on Hyperliquid" | **No Hyperliquid integration exists.** Zero references in source, config, env, or git history. |
| "My crypto bots trade live" | `hf_btc/` and `hf_btc_codex/` are **simulation-only**. They pull market data from Alpaca and book fills against an internal `sim_portfolio.py` engine. No real orders are sent anywhere. |
| Fee model | The sim assumes **Binance Futures** fees: maker `0.02%`, taker `0.05%`, default `taker`, slippage `0.01%` (`hf_btc/scripts/sim_portfolio.py:36-39`). These are reference numbers, not a real venue. |
| "My market bot makes micro-profits" | The "Bull" equities agent trades **US equities/ETFs/options + crypto majors on Alpaca (paper by default)**. There is **no dedicated market-making bot** — `scripts/microstructure.py` is only a defensive spread/queue-imbalance gate, not a trading strategy. |

**Implication:** "Migrate the bots from Hyperliquid to Kraken" is really two separate, smaller projects:
1. **Move crypto funds** Binance → Kraken (an account/custody task, not a code task).
2. **Decide whether to wire any bot to a real Kraken execution venue** (today nothing executes live on crypto except the Alpaca-paper crypto sleeve of the equities agent).

There is no large Hyperliquid codebase to rip out. Migration surface is small.

---

## 1. Can the project run on Kraken? — Crypto

### 1.1 Regulatory: yes, cleanly

- Kraken (Payward Europe Solutions Ltd) holds a **MiCA CASP license from the Central Bank of Ireland**, authorised **25 June 2025** — first major global exchange to get CBI authorization, and it now passports across **all 30 EEA countries** including France.
- Authorised services include execution of orders, reception/transmission of orders, custody, and exchange crypto↔funds and crypto↔crypto. This is exactly the surface a trading bot needs.
- MiCA hard-enforcement date is **1 July 2026** (no extension). Kraken is compliant well ahead; Binance is the one losing EEA standing. So Kraken is the correct destination.

### 1.2 Technical: feasible, moderate effort

- Kraken exposes a documented **REST + WebSocket API** (`https://api.kraken.com/0/`) for spot, available to authenticated EEA clients. BTC/ETH/SOL all trade as spot pairs (e.g. `XXBTZUSD`, `XETHZUSD`, `SOLUSD`).
- The repo's clients are **stdlib-only `urllib` wrappers** (`scripts/alpaca_crypto_client.py`, ~181 lines). A Kraken equivalent is a self-contained new client of similar size: HMAC-SHA512 request signing (Kraken's auth scheme), pair-name mapping, and order/position/balance endpoints. **No SDK or dependency changes needed.**
- The decision logic (`hf_btc` harness, indicators, CTQS framework) is venue-agnostic — it consumes OHLCV and emits a JSON decision. Only the **data fetch** and **execution layer** are venue-specific.

**Effort estimate (if/when you choose to go live):** one new `kraken_crypto_client.py` (~200 lines), a data-source toggle, and an env/fee-config update. Days, not weeks.

### 1.3 The fee problem — the real catch for the HF bot

This is where the migration *costs* you, and it is significant for a high-frequency, micro-profit BTC bot.

**Kraken spot fee schedule (2026), lowest volume tier:**

| 30-day volume (USD) | Maker | Taker |
|---|---|---|
| $0+ | **0.25%** | **0.40%** |
| $50k+ | 0.14% | 0.24% |
| $100k+ | 0.12% | 0.22% |
| $250k+ | 0.10% | 0.20% |
| $1M+ | 0.06% | 0.16% |
| $10M+ | 0.00% | 0.10% |

**Compare round-trip cost (open + close) at the starting tier:**

| Venue / model | Per side (taker) | Round-trip taker | Round-trip maker |
|---|---|---|---|
| Current sim (Binance Futures) | 0.05% | **0.10%** | 0.04% |
| Hyperliquid perps (reference) | ~0.045% | ~0.09% | ~0.03% |
| **Kraken spot, base tier** | **0.40%** | **0.80%** | 0.50% |
| Kraken spot, $1M+ tier | 0.16% | 0.32% | 0.12% |

> A 15-minute-loop BTC bot taking liquidity on **Kraken spot** at the base tier pays **~8× the fees** the simulation assumes. It would need **>0.80% net moves** just to break even on a taker round-trip. The current strategy's "micro-profit" edge does **not** survive this. **Kraken spot is the wrong venue for HFT-style crypto.**

**The mitigation: Kraken Perpetual Futures (now live on Kraken Pro in the EU under a CySEC MiFID license).**

- Derivatives use a much cheaper maker-taker schedule (comparable to the Binance-Futures numbers the sim already assumes — and a current **0-maker-fee** promo for the first 30 days for new EEA futures users).
- 300+ perpetual pairs, crypto-collateral supported.
- **Catch:** retail access requires passing **MiFID II appropriateness tests**, and leverage/eligibility vary by country. France is eligible but you'd onboard through the derivatives entity and accept product/leverage limits.

**Verdict (crypto):** Migration is regulatory-clean and technically modest. **But route any high-frequency BTC strategy to Kraken Futures, not Kraken spot** — spot fees would erase the edge. For the slower crypto-majors sleeve inside the equities agent (occasional BUYs, held for days), Kraken **spot** is fine; the fee per trade is negligible relative to holding period.

---

## 2. The second bot idea — Kraken tokenized stocks (xStocks)

You asked whether you could run a second bot on Kraken's tokenized stocks (xStocks), like your current equities ("market") bot but with better volume/edge. **Short answer: not as an automated bot in the EEA. This is a hard blocker, not a fee issue.**

### 2.1 What xStocks are

- ~60 tokenized US equities + ETFs (AAPLx, TSLAx, NVDAx, SPYx, QQQx…) issued by **Backed Finance** as SPL tokens on **Solana**, 1:1 collateralized by real shares custodied at a Swiss prime broker.
- Settlement is **T+0 on Solana** (sub-second), and they trade **24/5** (a subset of ~10 trade **24/7**). That part is genuinely attractive vs. a 6.5h US session.

### 2.2 The EEA blocker — no API, no Pro order book, fiat-only

For **EEA clients (France included)**, served by Payward's Bermuda/CySEC entities:

| Method | EEA allowed? |
|---|---|
| Buy / sell / convert on **kraken.com website** (manual) | ✅ |
| Kraken Pro **"Convert"** feature | ✅ |
| **Kraken Pro order books** | ❌ |
| **Kraken API** | ❌ |
| **Crypto/USDT funding** (must use fiat) | ❌ |

> **A bot cannot trade xStocks in the EEA.** There is no programmatic access — only manual, fiat-funded buy/sell/convert through the website. The whole premise of "a second automated bot on tokenized stocks" is blocked by Kraken's own EEA distribution rules, regardless of strategy quality.

### 2.3 Even if the API existed, the economics fight you

xStocks trade on Kraken Pro's standard **maker-taker schedule (0.25%/0.40% base)**. Your current equities bot trades on **Alpaca with $0 commission**. So a tokenized-stock bot would *add* 0.25–0.40% per side versus today's zero — the opposite of "better." The only structural wins are **24/7 access** and **T+0 settlement**, not cost. For a strategy whose problem is "micro profits," layering 0.40%/side on top makes the edge harder, not easier.

**Verdict (xStocks):** ❌ **Not viable as an automated second bot in the EEA today.** No API/Pro access for EEA, fiat-only, and fees higher than your current commission-free equities venue. The 24/7 + T+0 properties are interesting but only reachable by hand.

---

## 3. Moving the crypto funds Binance → Kraken (the actual urgent task)

This is independent of any bot work and is the thing MiCA actually forces:

1. Create/verify a Kraken EEA account (KYC).
2. Withdraw BTC/ETH/SOL on-chain from Binance to Kraken deposit addresses (or sell to EUR on Binance and SEPA-transfer fiat, if you want to avoid network fees / re-acquire on Kraken).
3. On-chain network fees + any Binance withdrawal fee apply; choosing the cheaper network (e.g. SOL for SOL, native chains) minimizes cost. This is operational, not a code change.

No code in this repo touches Binance, so nothing breaks by moving funds.

---

## 4. Gains / losses summary

### What you gain by moving to Kraken
- ✅ **MiCA-compliant home for EEA crypto** (mandatory; Binance can't serve you).
- ✅ A **real, API-accessible spot + futures venue** for crypto — today your crypto bots are simulation-only, so this is the first path to *actually* trading crypto live.
- ✅ **Kraken Futures** gives near-current fee economics for an HFT BTC strategy, plus a 30-day zero-maker promo.
- ✅ Optional manual access to **24/7 tokenized US stocks** (interesting for you personally, even if not bot-driven).

### What you lose / what costs you
- ❌ **xStocks automation is impossible in the EEA** — no API, no Pro book, fiat-only. The second-bot idea is blocked.
- ❌ **Kraken spot fees are ~8× the simulated Binance fees** — fatal for HFT on spot; forces you onto Futures (which adds MiFID appropriateness onboarding + leverage/eligibility constraints).
- ❌ Net-new **engineering**: a Kraken client, data-source toggle, fee re-calibration of the sim, and re-validation of the strategy's edge under realistic Kraken fees before any live switch.
- ⚠️ The equities bot stays on **Alpaca** regardless — Kraken does not replace it (and the commission-free Alpaca equities venue is cheaper than tokenized stocks anyway).

---

## 5. Recommendation

1. **Do the funds migration now** (Binance → Kraken). It's forced by MiCA and unrelated to code.
2. **Re-calibrate the HF-BTC simulation to Kraken's real fees first**, *before* writing any live client. Set the sim to Kraken spot (0.40% taker) and to Kraken Futures (~0.05% taker) and see whether the strategy is still net-positive. If it only survives on Futures, that decides the venue.
3. **If the edge survives:** build a single `kraken_crypto_client.py` and route the **HF-BTC bot to Kraken Futures** (not spot). Keep the slow crypto-majors sleeve on spot if you prefer no-leverage.
4. **Drop the xStocks-bot idea for now** — it's blocked for EEA automation. Revisit only if Kraken opens EEA API/Pro access to xStocks (watch their changelog). If your real goal is "more volume / bigger edge than the micro-profit equities bot," the better lever is **improving the Alpaca equities/options strategy or adding leverage via options**, not tokenized stocks.

### Decision matrix

| Component | Today | Move to Kraken? | Verdict |
|---|---|---|---|
| Crypto custody (funds) | Binance | **Yes — mandatory** | Do it now |
| HF-BTC bot (sim) | Alpaca data + Binance-fee sim | Kraken **Futures** if edge survives | Re-validate fees first |
| Crypto-majors sleeve (equities agent) | Alpaca paper | Kraken **spot** ok (slow trades) | Optional |
| Equities / ETFs / options ("market" bot) | Alpaca | **No** | Stays on Alpaca |
| New xStocks bot | — | **Blocked (no EEA API)** | Not viable |

---

## Sources

- [Kraken cements European leadership with MiCA license from Central Bank of Ireland](https://blog.kraken.com/news/mica-license-central-bank-of-ireland)
- [Kraken now live across all 30 EEA countries under MiCA](https://blog.kraken.com/news/all-30-eea-countries-mica)
- [Where is Kraken licensed or regulated?](https://support.kraken.com/articles/where-is-kraken-licensed-or-regulated)
- [What stocks and ETFs are available as xStocks? (EEA restrictions)](https://support.kraken.com/articles/xstocks-availability)
- [Tokenized Stocks and ETFs on Kraken (xStocks)](https://www.kraken.com/xstocks)
- [xStocks now available to EU clients](https://blog.kraken.com/product/xstocks/now-available-to-eu-clients)
- [Kraken Fee Schedule (spot maker/taker tiers)](https://www.kraken.com/features/fee-schedule)
- [Crypto-powered perpetual futures now live on Kraken Pro in EU](https://blog.kraken.com/product/kraken-derivatives/crypto-collateral-eu-futures)
- [New EEA futures traders: no trading fees for your first 30 days](https://blog.kraken.com/product/margin/eea-futures-30-days-no-trading-fees)
- [Linear Multi-Collateral Derivatives Contract Specs for EEA clients](https://support.kraken.com/articles/perpetual-contract-specifications-for-clients-in-the-eea)
</content>
</invoke>
