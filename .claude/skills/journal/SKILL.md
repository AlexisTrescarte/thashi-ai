---
name: journal
description: Update memory (agent-namespaced trade_log, portfolio, research_log, daily_review, weekly_review, monthly_review, quarterly_rewrite, shared learnings, strategy_evolution, prompt_evolution_proposals) at the end of a run, commit and push. Invoke at the end of every routine.
---

# Skill: journal

Memory discipline: append-only on logs, controlled overwrite on snapshots. Commit + push every run or the next routine starts from stale state.

## Rules

- **Append-only files** (never rewrite history):
  - `memory/{agent}/trade_log.md`
  - `memory/{agent}/research_log.md`
  - `memory/{agent}/daily_review.md`
  - `memory/{agent}/weekly_review.md`
  - `memory/{agent}/monthly_review.md`
  - `memory/{agent}/quarterly_rewrite.md`
  - `memory/learnings.md`
  - `memory/strategy_evolution.md`
  - `memory/prompt_evolution_proposals.md`
  - `memory/runs.log`
- **Controlled overwrite** (snapshot block only):
  - `memory/{agent}/portfolio.md` — "Latest snapshot" block + regenerated positions table from API
  - `memory/strategy.md` — only via `quarterly-rewrite` (with logged diff in `strategy_evolution.md`)
  - `memory/guardrails.md` — **only via human edit** (immutable sections can never be changed by agent)
- **ISO UTC timestamps** everywhere: `2026-04-20T13:45:00Z`
- **Never** commit a secret or include one in a notification
- **Namespace discipline**: the equities agent writes only to `memory/equities/*` + shared; the crypto agent writes only to `memory/crypto/*` + shared

## End-of-run steps

1. Write appends/snapshot updates to the relevant files
2. `git status` to verify what will be committed
3. `git diff --stat` to ensure no unexpected file modified (refuse if `guardrails.md` or the immutable sections of another file changed without a human-edit flag)
4. `git add -A`
5. `git commit -m "[{routine}] YYYY-MM-DD — {1-line summary}"`
6. `git push origin {branch}` (branch from environment, typically `main`)
7. On push fail: append `[PUSH-FAIL] {timestamp} — {error}` to `learnings.md`, notify Telegram `DEGRADED`, do not retry in a loop

## Commit message conventions

### Equities

- `[pre-market] 2026-04-20 — regime neutral, 4 BUY + 2 WATCH, 3 positions to watch`
- `[market-open] 2026-04-20 — 4 BUY (NVDA, LLY, XOP, SOXL), 1 skip (META FOMO)`
- `[intraday-scan] 2026-04-20 10:30 — 1 tighten (NVDA +11%), 1 TP-update (LLY), 1 new BUY (AMD technical)`
- `[market-close] 2026-04-20 — equity $104,320, day +0.9%, alpha day +0.4%, cumul +4.3%, 12 positions (2 aging)`
- `[daily-review] 2026-04-20 — grade B, 4 new / 3 closed (2W/1L), lesson: tighten earlier on PEAD`
- `[weekly-review] 2026-04-24 — grade B, week alpha +0.6%, cumul +5.1%, hit rate 58%, avg hold 3.4d`
- `[monthly-deep-review] 2026-04-24 — Sharpe 1.2, Sortino 1.8, MaxDD -6.2%, 3 prompt proposals (1 applied)`
- `[quarterly-rewrite] 2026-06-26 — strategy v2.1, trimmed PEAD threshold 70→75, added crypto correlation gate`

### Crypto

- `[crypto-hourly] 2026-04-20T14:00Z — 1 BUY (ETH), 2 stop-updates, regime risk-on`
- `[crypto-daily-review] 2026-04-20 — grade B, day +1.8%, vs BTC +0.2%, 4 trades`
- `[crypto-weekly-review] 2026-04-20 — week +3.4%, vs BTC +1.1%, 22 trades, hit rate 55%`
- `[crypto-monthly-review] 2026-05-01 — MaxDD -8%, Sharpe 1.0, 2 prompt proposals`

## Anti-noise fallback

If nothing justifies a file change (e.g. pre-market with no idea, intraday-scan with no action):
- Still append one line to `memory/runs.log`: `YYYY-MM-DDTHH:MM:SSZ [{routine}] noop: {reason}`
- Purpose: keep evidence the routine ran + enable run-frequency diagnostics in reviews

## Sanity checks before commit

- Diff doesn't touch immutable sections of `guardrails.md` (see file for which sections)
- Diff doesn't touch `memory/strategy.md` unless routine is `quarterly-rewrite` or evolution gates passed
- Agent namespace respected: no crypto run writing to equities files
- No secrets or raw API keys in the diff
