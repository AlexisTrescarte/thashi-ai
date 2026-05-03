#!/usr/bin/env bash
# Bull-HF-BTC Codex continuous loop.
# Each iteration:
#   1. harness.py prepare              — pulls data, builds /tmp/hf_codex_prompt.md
#   2. codex exec (non-interactive)    — emits JSON decision to /tmp/hf_codex_decision_envelope.json
#   3. harness.py post                 — parses, validates, executes, telegram, commit
#   4. harness.py sleep_until_next     — aligns to next 15-min UTC boundary
#
# Daily report at 23:55 UTC (handled inside post when minute >= 55).
#
# Usage:
#   ./run_loop.sh              # foreground
#   ./run_loop.sh > /var/log/bull-hf-btc-codex.log 2>&1 &   # background on VPS

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

if [[ -n "${CODEX_BIN:-}" ]]; then
    :  # honor explicit override
elif [[ -x "/usr/bin/codex" ]]; then
    CODEX_BIN="/usr/bin/codex"
else
    CODEX_BIN="codex"
fi
CODEX_MODEL="${HF_CODEX_MODEL:-gpt-5.5}"
TICK_TIMEOUT="${HF_TICK_TIMEOUT:-180}"
CODEX_SEARCH="${HF_CODEX_SEARCH:-1}"

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
    log "WARNING: no timeout binary found (install via 'brew install coreutils' for gtimeout) — codex will run without hard cap"
fi

log "Bull-HF-BTC Codex loop started · CODEX_BIN=$CODEX_BIN · CODEX_MODEL=$CODEX_MODEL · PYTHON_BIN=$PYTHON_BIN · TIMEOUT_BIN=${TIMEOUT_BIN:-none}"

while true; do
    TICK_START=$(date +%s)

    # Phase 1 — prepare context
    if ! "$PYTHON_BIN" "$ROOT/scripts/harness.py" prepare; then
        log "prepare failed — sleeping 60s"
        sleep 60
        continue
    fi

    # Phase 2 — invoke codex
    if [[ ! -f /tmp/hf_codex_prompt.md ]]; then
        log "/tmp/hf_codex_prompt.md missing after prepare — skipping LLM, post will SKIP"
        echo '{"result":""}' > /tmp/hf_codex_decision_envelope.json
    else
        if [[ -n "$TIMEOUT_BIN" ]]; then
            log "invoking codex (timeout ${TICK_TIMEOUT}s via $TIMEOUT_BIN)..."
            CODEX_CMD=("$TIMEOUT_BIN" "$TICK_TIMEOUT" "$CODEX_BIN")
        else
            log "invoking codex (no timeout)..."
            CODEX_CMD=("$CODEX_BIN")
        fi
        CODEX_ARGS=()
        if [[ "$CODEX_SEARCH" == "1" ]]; then
            CODEX_ARGS+=(--search)
        fi
        CODEX_ARGS+=(
            --model "$CODEX_MODEL"
            --ask-for-approval never
        )
        CODEX_ARGS+=(
            exec
            --sandbox read-only
            --cd "$ROOT"
            --output-last-message /tmp/hf_codex_last_message.md
        )
        if ! "${CODEX_CMD[@]}" "${CODEX_ARGS[@]}" - \
                < /tmp/hf_codex_prompt.md \
                > /tmp/hf_codex_stdout.log 2> /tmp/hf_codex_stderr.log; then
            log "codex failed or timed out — post will SKIP. stderr:"
            tail -5 /tmp/hf_codex_stderr.log || true
            echo '{"result":""}' > /tmp/hf_codex_decision_envelope.json
        else
            "$PYTHON_BIN" -c 'import json, pathlib, sys; p=pathlib.Path(sys.argv[1]); print(json.dumps({"result": p.read_text() if p.exists() else ""}))' \
                /tmp/hf_codex_last_message.md > /tmp/hf_codex_decision_envelope.json
        fi
    fi

    # Phase 3 — post
    if ! "$PYTHON_BIN" "$ROOT/scripts/harness.py" post; then
        log "post failed — continuing"
    fi

    TICK_END=$(date +%s)
    log "tick complete in $((TICK_END - TICK_START))s"

    # Phase 4 — sleep until next 15-min boundary
    "$PYTHON_BIN" "$ROOT/scripts/harness.py" sleep_until_next || sleep 60
done
