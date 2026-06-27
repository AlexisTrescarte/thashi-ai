# Audit — `tradingview-mcp` vs. Bull v2 architecture

Date: 2026-06-27
Subject: Instagram post (@aipagedaily) about a GitHub project linking Claude Code to TradingView Desktop via Chrome DevTools Protocol (CDP).

## 1. The repo identified

- **Repo**: `tradesdontlie/tradingview-mcp` ("TradingView MCP Bridge")
- **What the post describes is accurate**: it bridges Claude Code ↔ TradingView Desktop via CDP so the AI can read charts, switch symbols/timeframes, write/compile Pine Script, use replay mode, drawings, alerts, screenshots, with a `tv_health_check`.
- **Maturity**: ~4,000★ / ~1,900 forks, active, MIT license (code only). Author explicitly states it is **unofficial**, uses **undocumented internal Electron APIs**, and **may break on any TradingView update**.
- **NOTE on the screenshot**: the flashy dashboards in the Instagram post ("Probability Lattice / quincunx", "Tail Probability Ridge", "MIROFISH relationship graph", "MODEL CLAUDE-FABLE-5", "STACK MIROFISH-CORE • FABLE-FORK") are **AI-generated marketing visuals, not real output of this repo**. The repo does NOT produce those. It produces chart reads, Pine compile results, indicator tables, and PNG screenshots of the TradingView UI.

## 2. Architecture / runtime model

```
Claude Code ↔ MCP server (Node.js, stdio) ↔ CDP localhost:9222 ↔ TradingView Desktop (Electron GUI)
```

- ~78 MCP tools + a `tv` CLI. Categories: chart reading, Pine Script dev (inject/compile/console), chart control, multi-pane layouts, custom indicator data, replay mode, drawings/alerts, UI automation, streaming (poll-and-diff), connection mgmt.
- **Local-only**: everything goes through `localhost:9222` on the *same machine* that runs the TradingView Desktop GUI. No network server, no TradingView account credentials handled.
- **Requirements**: Node 18+, **TradingView Desktop app installed and running with `--remote-debugging-port=9222`**, a **graphical desktop environment (GUI)**, and a **paid TradingView subscription for real-time data**. Explicitly **no headless/server-only mode**.
- **Does NOT execute trades** — chart/analysis only.

## 3. Bull v2's actual runtime (the mismatch)

| Dimension | Bull v2 today | tradingview-mcp needs |
|---|---|---|
| Where it runs | **Ephemeral claude.ai cloud sandbox**, fresh per trigger, torn down after | A **persistent** host |
| Display | **Headless**, no GUI | A **running GUI desktop** with TradingView Desktop on :9222 |
| Market data | **Alpaca REST API** | TradingView Desktop (paid sub) |
| Execution | **Alpaca API** (paper/live) | None (chart-only) |
| State | Stateless, continuity via `memory/` in git | A long-lived local process holding a CDP session |
| Deps | Python stdlib, zero-dep | Node.js + Electron app + CDP |

**Core conclusion**: the two cannot be wired together in Bull's current autonomous loop. The cloud routine sandbox and any VPS/desktop running TradingView are **different machines**; `localhost:9222` is unreachable across them, and the MCP is designed for same-host stdio + local CDP, not remote exposure. Even on a single VPS, a standard trading VPS is headless; you'd need a Windows-RDP desktop (or Linux + Xvfb) keeping the Electron app alive 24/7.

## 4. Power assessment

- **As a live component of the autonomous loop**: LOW value, HIGH fragility.
  - No trade execution (Bull already has Alpaca for that).
  - Data is redundant — Bull already pulls quotes/bars from Alpaca.
  - Unofficial + breaks on TV updates → unacceptable for an unattended 24/7 agent.
  - Requires a persistent GUI host the current architecture doesn't have.
  - Potential TradingView ToS friction on programmatic data access.
- **As a separate strategy-R&D / research workstation tool**: MEDIUM-HIGH value.
  - Genuinely useful for **visual chart analysis**, **Pine Script authoring + compile checks**, **strategy-tester backtests**, and **replay-mode validation** — run interactively on *your own desktop* where TradingView Desktop already lives.
  - Output (validated setups, thresholds, Pine logic) can be **distilled by hand into `memory/strategy.md` / setup thresholds**, feeding Bull indirectly.

## 5. Recommendation

1. **Do NOT integrate it into the autonomous cloud-routine loop.** Architectural mismatch (headless, ephemeral, different host) + fragility + no execution + data redundancy.
2. **Optionally run it locally** on your own desktop (or a GUI/RDP VPS) as an **interactive R&D tool** to develop and backtest setups in TradingView, then port the validated logic into Bull's strategy memory manually.
3. If "richer charting data inside Bull" is the real goal, the in-architecture path is **better Alpaca/3rd-party data feeds + Python indicators in `scripts/`**, not a GUI-bound Electron bridge.
4. Treat the Instagram visuals as marketing — set expectations accordingly.

## 6. If you still want to pilot it (sandbox-safe checklist)

- Use a **paper-only** mindset; the tool can't trade, but keep it isolated from Bull's Alpaca keys.
- Pin the TradingView Desktop version; expect breakage on updates.
- Keep `9222` bound to `localhost` only — never expose the debug port to the network.
- Keep it OUT of this repo's automated path; it has Node/Electron deps that violate the zero-dep, headless design.
