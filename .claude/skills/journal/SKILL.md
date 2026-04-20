---
name: journal
description: Update memory (trade_log, portfolio, learnings, research_log, weekly_review) at the end of a run, commit and push. Invoke at the end of every routine.
---

# Skill: journal

Memory discipline: append-only on logs, controlled overwrite on snapshots. Commit + push at every run or the next routine starts from stale state.

## Rules

- **Append-only**: `trade_log.md`, `research_log.md`, `weekly_review.md`, `learnings.md`. Never rewrite history.
- **Controlled overwrite**: `portfolio.md` ("Latest snapshot" block + refreshed positions table). `strategy.md` / `guardrails.md` only via weekly-review.
- **ISO UTC timestamps** everywhere: `2026-04-20T13:45:00Z`.
- **Never commit `.env`, a secret, or a full Telegram transcript**.

## End-of-run steps

1. Write appends to appropriate files.
2. `git status` to verify what will be committed.
3. `git diff --stat` to ensure no unexpected files modified.
4. `git add -A`
5. `git commit -m "[{routine}] YYYY-MM-DD — {1-line summary}"`
6. `git push origin main`
7. If push fails: append in `learnings.md` an incident `[INCIDENT] push failed: ...`, notify Telegram `DEGRADED`. Do not retry in a loop.

## Commit formats

- `[pre-market] 2026-04-20 — regime neutral, 3 BUY + 2 WATCH, 2 positions to watch`
- `[market-open] 2026-04-20 — 3 BUY (NVDA, LLY, XOP), 1 skip (META FOMO)`
- `[midday] 2026-04-20 — 1 cut (-5.2%), 2 tightens, 1 time stop J+9`
- `[market-close] 2026-04-20 — equity $97,432, day +0.32%, alpha day +0.12%, cumul +0.8%, 12 positions (2 aging)`
- `[weekly-review] 2026-04-24 — grade B, week +1.8%, alpha +0.4%, hit rate 55%, avg hold 3.2d`

## Anti-noise

If nothing justifies a commit (e.g. pre-market with no idea, midday with no action):
- Still commit a minimal snapshot to `memory/runs.log` (append one line `YYYY-MM-DDTHH:MM:SSZ [{routine}] noop: reason`).
- Purpose: keep evidence the routine actually ran.
