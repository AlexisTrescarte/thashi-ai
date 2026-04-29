# Strategy evolution log

Append-only. **Never rewrite** a past entry. Every change to `memory/strategy.md` or to any command/skill prompt — whether agent-autonomous (via gated self-evolution) or human-edited — is logged here with rationale and evidence.

## Schema

```markdown
## YYYY-MM-DDTHH:MM:SSZ — {routine or "human"} — {title}

**Actor**: {agent-autonomous via monthly-deep-review | agent-autonomous via quarterly-rewrite | human}
**Scope**: {strategy.md | guardrails.md | .claude/commands/X.md | .claude/skills/X/SKILL.md}
**Gates passed** (if autonomous): {list of gate checks}

### Rationale
{2-4 lines — why this change}

### Evidence
{data points, metrics, sample size — concrete numbers}

### Before → After (diff summary)
{1-3 lines describing the delta}

### Follow-up
{metric to watch, revert criteria if it doesn't work}
```

## Log

## 2026-04-29T22:30:00Z — human — Active intraday universe scan (mandatory) + opportunistic cap 3 → 5 BUYs/day

**Actor**: human (user-directed, post-merge follow-up to address residual under-activity after spread/harness fix)
**Scope**: `.claude/commands/intraday-scan.md` (cadence rule + new "Mandatory active universe scan" section)

**Gates**: N/A (human edit). No hard-cap modification on guardrails.md. No change to forbidden instruments. No auto-defense / self-evolution gate touched. Quality filters (CTQS ≥ 60 Pathway B, T+Q+S ≥ 60/75 Pathway C, FOMO, spread, sector, position, revenge) all preserved.

### Rationale

After the 04-29 spread-protocol + harness-gap fix, residual concern: the existing intraday Pathway B/C language is **passive** ("if a catalyst surfaces"). Bot does not actively grate the universe at each wake-up — it only reacts to what enters its field of view. Combined with conservative filters this produces 1 BUY / 10 TD instead of the 3 BUY / 5 TD strategy floor.

Two complementary changes:
1. Make the universe scan **mandatory** at each BUY-eligible slot (10:30/11:30/12:30/13:30) with explicit minimum candidate count (5) and minimum research depth (top-2 through the `research` skill).
2. Raise the hourly-cap daily total for Pathways B+C combined from 3 → **5 BUYs/day** to match the wider discovery surface; Pathway C stays capped at 1/day.

Token cost is non-binding (user explicit). Routines/day cap (15) is non-binding (existing slots, no new wakes).

### Evidence

- 2-week post-launch sample (2026-04-20 → 2026-04-29): 1 BUY filled across 5 candidates dispatched, all 4 mechanical (non-thesis) skips. Activity floor target 3/5 TD missed by ~3×.
- Pathway B/C language audit confirms passive framing: "new dated catalyst surfaced today" + "clean technical setup surfacing intraday" — no mandatory scan, no minimum candidate count, no documentation requirement when 0 promote.
- Strategy.md philosophy "trade often, but never recklessly" + activity floor "≥1 BUY per 3 trading days when scan surfaces any CTQS ≥ 55 candidate" both presuppose the scan happens — the prompt did not enforce it.

### Before → After (diff summary)

**Before**: Pathway B/C are passive — bot evaluates if it happens to notice a setup. Daily cap 3 BUYs (B+C). No documentation requirement when nothing fires.

**After**:
- New "Mandatory active universe scan" block at the top of the BUY pathways section.
- Each slot 10:30/11:30/12:30/13:30 must run news + technical + flow sweep targeting ≥ 5 candidates, top-2 through `research` skill for full CTQS.
- Daily cap 5 BUYs (B+C); Pathway C still 1/day.
- Scan output documented in `research_log.md` even on 0-promote slots (rejection trail = signal for weekly review tuning).

### Follow-up

**Metrics to watch (next 4 weeks)**:
- BUY/day average (B+C): target 2-4, must not systematically hit the 5/day cap (signal of dilution).
- Pathway B hit rate vs Pathway A baseline: must not drop more than 5pp (signal that mandatory scan is finding lower-quality setups).
- 0-promote slot ratio: rejection trail should show that filters are working, not that the bot is just running through motions — weekly-review must inspect 5 random rejected candidates per week.
- Activity floor compliance: ≥ 3 BUY / 5 TD in risk-on/neutral regime.

**Revert criteria** (any triggers a revert at next monthly-deep-review):
- Hit rate Pathway B falls > 5pp below Pathway A on equal sample.
- Daily cap of 5 hit ≥ 3 days in a single week (dilution signal).
- Average CTQS at entry drops > 5 points below pre-fix baseline.

## 2026-04-29T22:00:00Z — human — Spread protocol (wait-and-retry + open-retry pathway) + harness-gap self-healing

**Actor**: human (user-directed fix after 2-week post-launch review identified two structural drags)
**Scope**:
- `.claude/skills/trade/SKILL.md` (BUY equities/ETFs spread protocol)
- `.claude/commands/market-open.md` (Step 1-bis harness-gap, Step 4 open-retry tagging, Forbidden list reword)
- `.claude/commands/intraday-scan.md` (Step 1-bis harness-gap fallback at 10:30, Pathway A-prime open-retry)

**Gates**: N/A (human edit). No hard-cap modification, no forbidden feature enabled, no auto-defense / self-evolution gate touched. Conservative additions only.

### Rationale

Two-week post-launch review (2026-04-20 → 2026-04-29) surfaced two compounding drags:

1. **Single-shot spread filter at T+0 to T+6min rejects gap-day winners**. On 04-23 GEV (4.66%) + VRT (5.38%) skipped at open, never re-attempted. On 04-28 VRT (5.90%) + AMD skipped. Pattern: PEAD leaders open with anomalous spreads that normalize within 30-60 min, but the agent had no retry mechanism. 2 of 3 BUY queue dispatches on 04-23 = mechanical (non-thesis) skips with no recovery path.
2. **Harness misses ~50% of routines** (6/6 missed on 04-24, 5/9 on 04-27 incl. pre-market 3 days running). Sans pre-market block, market-open + intraday-scan have no BUY queue → forced cash 98%.

Together these two issues drove activity floor to **1 BUY / 10 TD** vs target ≥ 3/5 TD.

### Evidence

- `runs.log` 2026-04-22 → 2026-04-29: 1 BUY filled out of 5 candidates dispatched (GEV, VRT×2, AMD, GOOGL). 4/5 mechanical skips, 0/5 thesis-driven skips.
- `learnings.md` 2026-04-23T13:37:30Z: spread skip pattern documented with exact remediation proposed.
- `learnings.md` 2026-04-24T20:45:00Z [INCIDENT]: 6/6 routines missed, queued GTD-at-fill rule as proposal but did not address the harness-gap recovery path.
- `learnings.md` 2026-04-27T20:32:00Z: 5/9 missed, 3rd consecutive pre-market gap, "structural operational degradation" tag.
- `daily_review.md` 04-24, 04-27: both grade C, both citing recurring harness gap as primary degradation driver.

### Before → After (diff summary)

**Before**: Spread > 0.5% at single quote-fetch → permanent skip for the day. Pre-market routine miss → no BUY pathway possible (Pathway A in intraday-scan only handled WATCH triggers, not absent pre-market).

**After**:
- Market-open implements wait-and-retry window (T+0/+60s/+180s/+300s) for spreads 0.5-1.5%; spread-only skips get an `[OPEN-RETRY]` tag in research_log.
- Intraday-scan 10:30 introduces Pathway A-prime: re-evaluates `[OPEN-RETRY]` tags as the FIRST action of the slot (one ticker per day max, FOMO guard preserved).
- Both market-open and intraday-scan-1030 implement a **harness-gap fallback express scan** when the upstream routine missed: max 2 candidates, Probe-only sizing, CTQS ≥ 65 floor (vs 55 normal), 1+1 sources, dated catalyst required, no technical-only.
- Limit-IOC at `bid + 0.3 × spread` introduced as a slippage-reducing alternative to market orders for moderate spreads (0.3-0.5%).

### Follow-up

**Metrics to watch (next 4 weeks)**:
- Pathway A-prime fill rate: target ≥ 50% of `[OPEN-RETRY]` tags resolve into a BUY by 13:30
- Average spread cost on open-window BUYs: target ≤ 0.4% (vs current rejection threshold 0.5%)
- Activity floor compliance: target ≥ 3 BUY / 5 TD in risk-on/neutral regime

**Revert criteria** (if any of these fire, revert at next monthly-deep-review):
- Pathway A-prime hit rate < 30% (signal: open-spread anomaly is not consistently transient)
- Express-scan harness-gap BUYs underperform standard-pre-market BUYs by > 10pp on hit rate (signal: rushed research → bad picks)
- Any guardrail breach traceable to these changes (sector cap exceeded via A-prime stacking, etc.)

**Out of scope for this fix (separate work item)**:
- The harness scheduler itself (claude.ai remote triggers firing ~50%) is not addressable in this codebase. Self-healing routines mitigate the impact but the root cause requires user action on triggers config.
