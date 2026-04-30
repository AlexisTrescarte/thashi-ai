#!/usr/bin/env bash
# Bull-HF-BTC continuous loop.
# Each iteration:
#   1. harness.py prepare              — pulls data, builds /tmp/hf_prompt.md
#   2. claude -p (non-interactive)     — emits JSON decision to /tmp/hf_decision_envelope.json
#   3. harness.py post                 — parses, validates, executes, telegram, commit
#   4. harness.py sleep_until_next     — aligns to next 5-min UTC boundary
#
# Daily report at 23:55 UTC (handled inside post when minute >= 55).
#
# Usage:
#   ./run_loop.sh              # foreground
#   ./run_loop.sh > /var/log/bull-hf-btc.log 2>&1 &   # background on VPS

set -uo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$ROOT/.." && pwd)"
ENV_FILE="$REPO/.env"

if [[ ! -f "$ENV_FILE" ]]; then
    echo "[bull-hf-btc] missing $ENV_FILE — copy from .env.example and fill secrets"
    exit 1
fi

# Load .env
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

cd "$ROOT" || exit 1

CLAUDE_BIN="${CLAUDE_BIN:-claude}"
MAX_TURNS="${HF_MAX_TURNS:-8}"
TICK_TIMEOUT="${HF_TICK_TIMEOUT:-180}"

log() { printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"; }

trap 'log "SIGINT — stopping loop"; exit 130' INT TERM

log "Bull-HF-BTC loop started · CLAUDE_BIN=$CLAUDE_BIN · MAX_TURNS=$MAX_TURNS"

while true; do
    TICK_START=$(date +%s)

    # Phase 1 — prepare context
    if ! python "$ROOT/scripts/harness.py" prepare; then
        log "prepare failed — sleeping 60s"
        sleep 60
        continue
    fi

    # Phase 2 — invoke claude
    if [[ ! -f /tmp/hf_prompt.md ]]; then
        log "/tmp/hf_prompt.md missing after prepare — skipping LLM, post will SKIP"
        echo '{"result":""}' > /tmp/hf_decision_envelope.json
    else
        log "invoking claude (timeout ${TICK_TIMEOUT}s)..."
        if ! timeout "$TICK_TIMEOUT" "$CLAUDE_BIN" \
                --output-format json \
                --max-turns "$MAX_TURNS" \
                -p "$(cat /tmp/hf_prompt.md)" \
                > /tmp/hf_decision_envelope.json 2> /tmp/hf_claude_stderr.log; then
            log "claude failed or timed out — post will SKIP. stderr:"
            tail -5 /tmp/hf_claude_stderr.log || true
            echo '{"result":""}' > /tmp/hf_decision_envelope.json
        fi
    fi

    # Phase 3 — post
    if ! python "$ROOT/scripts/harness.py" post; then
        log "post failed — continuing"
    fi

    TICK_END=$(date +%s)
    log "tick complete in $((TICK_END - TICK_START))s"

    # Phase 4 — sleep until next 5-min boundary
    python "$ROOT/scripts/harness.py" sleep_until_next || sleep 60
done
