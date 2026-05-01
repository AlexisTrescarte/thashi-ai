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

# Detect python binary: Debian/Ubuntu only ship `python3`, macOS has both.
if [[ -n "${PYTHON_BIN:-}" ]]; then
    :  # honor explicit override
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "[bull-hf-btc] no python interpreter found (need python3)"
    exit 1
fi

# Detect timeout binary: GNU `timeout` on Linux, `gtimeout` on macOS (brew coreutils),
# or fallback to no-timeout (dev only). systemd unit on VPS always has `timeout`.
if command -v timeout >/dev/null 2>&1; then
    TIMEOUT_BIN="timeout"
elif command -v gtimeout >/dev/null 2>&1; then
    TIMEOUT_BIN="gtimeout"
else
    TIMEOUT_BIN=""
fi

log() { printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"; }

trap 'log "SIGINT — stopping loop"; exit 130' INT TERM

if [[ -z "$TIMEOUT_BIN" ]]; then
    log "WARNING: no timeout binary found (install via 'brew install coreutils' for gtimeout) — claude will run without hard cap"
fi

log "Bull-HF-BTC loop started · CLAUDE_BIN=$CLAUDE_BIN · PYTHON_BIN=$PYTHON_BIN · MAX_TURNS=$MAX_TURNS · TIMEOUT_BIN=${TIMEOUT_BIN:-none}"

while true; do
    TICK_START=$(date +%s)

    # Phase 1 — prepare context
    if ! "$PYTHON_BIN" "$ROOT/scripts/harness.py" prepare; then
        log "prepare failed — sleeping 60s"
        sleep 60
        continue
    fi

    # Phase 2 — invoke claude
    if [[ ! -f /tmp/hf_prompt.md ]]; then
        log "/tmp/hf_prompt.md missing after prepare — skipping LLM, post will SKIP"
        echo '{"result":""}' > /tmp/hf_decision_envelope.json
    else
        if [[ -n "$TIMEOUT_BIN" ]]; then
            log "invoking claude (timeout ${TICK_TIMEOUT}s via $TIMEOUT_BIN)..."
            CLAUDE_CMD=("$TIMEOUT_BIN" "$TICK_TIMEOUT" "$CLAUDE_BIN")
        else
            log "invoking claude (no timeout)..."
            CLAUDE_CMD=("$CLAUDE_BIN")
        fi
        if ! "${CLAUDE_CMD[@]}" \
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
    if ! "$PYTHON_BIN" "$ROOT/scripts/harness.py" post; then
        log "post failed — continuing"
    fi

    TICK_END=$(date +%s)
    log "tick complete in $((TICK_END - TICK_START))s"

    # Phase 4 — sleep until next 5-min boundary
    "$PYTHON_BIN" "$ROOT/scripts/harness.py" sleep_until_next || sleep 60
done
