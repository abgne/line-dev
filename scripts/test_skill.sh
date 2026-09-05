#!/bin/bash
# Test trigger accuracy for a single LINE skill
#
# Usage:
#   ./test_skill.sh messaging-api --verbose
#   ./test_skill.sh line-login --max-iterations 3 --verbose --output results.json

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <skill-name> [options]" >&2
    echo "" >&2
    echo "Skills: messaging-api, line-login, line-liff, line-mini-app, line-notification-message, line-creators-market" >&2
    echo "Options: --max-iterations N, --runs-per-query N, --concurrency N, --verbose, --output FILE" >&2
    exit 1
fi

SKILL_NAME="$1"
shift

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
SKILL_DIR="$PLUGIN_DIR/skills/$SKILL_NAME"

if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "Error: Skill not found at $SKILL_DIR" >&2
    exit 1
fi

TEST_DATA_DIR="$SCRIPT_DIR/test-data/$SKILL_NAME"

if [ ! -f "$TEST_DATA_DIR/assessment_set.json" ]; then
    echo "Error: No assessment_set.json at $TEST_DATA_DIR/" >&2
    exit 1
fi

python3 "$SCRIPT_DIR/optimize_description.py" \
    --assessment-set "$TEST_DATA_DIR/assessment_set.json" \
    --skill-path "$SKILL_DIR" \
    --scope-config "$TEST_DATA_DIR/scope.json" \
    "$@"
