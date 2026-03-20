#!/bin/bash
# End-to-end trigger accuracy test using actual Claude Code invocation
#
# Unlike test_skill.sh (which simulates triggering via Agent SDK),
# this script runs real `claude -p` commands and checks whether
# the Skill tool was actually called — matching the approach from
# https://agentskills.io/skill-creation/optimizing-descriptions
#
# Usage:
#   ./test_skill_e2e.sh messaging-api
#   ./test_skill_e2e.sh messaging-api --runs 3
#   ./test_skill_e2e.sh messaging-api --runs 3 --verbose

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <skill-name> [--runs N] [--verbose]" >&2
    echo "" >&2
    echo "Skills: messaging-api, line-login, line-liff, line-mini-app, line-notification-message, line-creators-market" >&2
    exit 1
fi

SKILL_NAME="$1"
shift

RUNS=1
VERBOSE=false

while [ $# -gt 0 ]; do
    case "$1" in
        --runs) RUNS="$2"; shift 2 ;;
        --verbose) VERBOSE=true; shift ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
SKILL_DIR="$PLUGIN_DIR/skills/$SKILL_NAME"
TEST_DATA_DIR="$SCRIPT_DIR/test-data/$SKILL_NAME"

if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "Error: Skill not found at $SKILL_DIR" >&2
    exit 1
fi

if [ ! -f "$TEST_DATA_DIR/assessment_set.json" ]; then
    echo "Error: No assessment_set.json at $TEST_DATA_DIR/" >&2
    exit 1
fi

ASSESSMENT_FILE="$TEST_DATA_DIR/assessment_set.json"

check_triggered() {
    local user_query="$1"
    claude -p "$user_query" --output-format stream-json --verbose 2>/dev/null \
        | jq -r '.message?.content[]? | select(.type == "tool_use" and .name == "Skill") | .input.skill' 2>/dev/null \
        | grep -q "^${SKILL_NAME}$"
}

COUNT=$(jq length "$ASSESSMENT_FILE")
TOTAL_PASS=0
TOTAL_FAIL=0

echo "Testing skill: $SKILL_NAME ($COUNT queries × $RUNS runs)" >&2
echo "" >&2

RESULTS="[]"

for i in $(seq 0 $((COUNT - 1))); do
    QUERY=$(jq -r ".[$i].query" "$ASSESSMENT_FILE")
    SHOULD_TRIGGER=$(jq -r ".[$i].should_trigger" "$ASSESSMENT_FILE")
    TRIGGERS=0

    for run in $(seq 1 "$RUNS"); do
        if check_triggered "$QUERY"; then
            TRIGGERS=$((TRIGGERS + 1))
        fi
    done

    RATE=$(echo "scale=2; $TRIGGERS / $RUNS" | bc)

    if [ "$SHOULD_TRIGGER" = "true" ]; then
        DID_PASS=$(echo "$RATE >= 0.5" | bc)
    else
        DID_PASS=$(echo "$RATE < 0.5" | bc)
    fi

    if [ "$DID_PASS" -eq 1 ]; then
        STATUS="PASS"
        TOTAL_PASS=$((TOTAL_PASS + 1))
    else
        STATUS="FAIL"
        TOTAL_FAIL=$((TOTAL_FAIL + 1))
    fi

    if [ "$VERBOSE" = true ]; then
        EXPECT="should"
        [ "$SHOULD_TRIGGER" = "false" ] && EXPECT="not  "
        printf "  [%s] %s %d/%d %s\n" "$STATUS" "$EXPECT" "$TRIGGERS" "$RUNS" "${QUERY:0:60}" >&2
    fi

    RESULTS=$(echo "$RESULTS" | jq \
        --arg query "$QUERY" \
        --argjson should_trigger "$SHOULD_TRIGGER" \
        --argjson triggers "$TRIGGERS" \
        --argjson runs "$RUNS" \
        --arg rate "$RATE" \
        --argjson did_pass "$([ "$DID_PASS" -eq 1 ] && echo true || echo false)" \
        '. + [{query: $query, should_trigger: $should_trigger, triggers: $triggers, runs: $runs, trigger_rate: ($rate | tonumber), pass: $did_pass}]'
    )
done

TOTAL=$((TOTAL_PASS + TOTAL_FAIL))
echo "" >&2
echo "Results: $TOTAL_PASS/$TOTAL passed ($TOTAL_FAIL failed)" >&2

jq -n \
    --arg skill "$SKILL_NAME" \
    --argjson runs "$RUNS" \
    --argjson passed "$TOTAL_PASS" \
    --argjson failed "$TOTAL_FAIL" \
    --argjson total "$TOTAL" \
    --argjson results "$RESULTS" \
    '{skill: $skill, runs_per_query: $runs, summary: {total: $total, passed: $passed, failed: $failed}, results: $results}'
