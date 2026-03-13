#!/bin/bash
# Run trigger accuracy tests for all LINE skills
#
# Usage:
#   ./test_all.sh              # evaluate only (1 iteration)
#   ./test_all.sh --verbose    # with per-query details

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS=(messaging-api line-login line-liff line-mini-app line-notification-message line-creators-market)

PASS=0
FAIL=0

for skill in "${SKILLS[@]}"; do
    echo "=== $skill ==="
    if "$SCRIPT_DIR/test_skill.sh" "$skill" --max-iterations 1 "$@"; then
        PASS=$((PASS + 1))
    else
        FAIL=$((FAIL + 1))
    fi
    echo ""
done

echo "========================================="
echo "Results: $PASS passed, $FAIL failed (${#SKILLS[@]} total)"
echo "========================================="
