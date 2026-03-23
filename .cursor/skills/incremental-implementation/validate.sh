#!/usr/bin/env bash
# Local validation script for incremental-implementation skill.
# Runs: pytest → ruff → mypy → bandit → frontend checks
# Usage: bash .cursor/skills/incremental-implementation/validate.sh [test_path]

set -euo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

TEST_PATH="${1:-}"
FAILED=0

echo "=== Local Validation ==="
echo ""

# 1. Pytest
echo "--- Running Pytest ---"
if [ -n "$TEST_PATH" ]; then
  echo "Running: pytest $TEST_PATH"
  pytest "$TEST_PATH" || FAILED=1
else
  echo "Running: pytest (full suite)"
  pytest || FAILED=1
fi

# 2. Ruff (only changed Python files)
echo ""
echo "--- Running Ruff (changed Python files) ---"
CHANGED_PY=$(
  { git diff --name-only -- '*.py'; git diff --name-only --cached -- '*.py'; } | sort -u | tr '\n' ' '
)
if [ -n "$CHANGED_PY" ]; then
  echo "Running: ruff check $CHANGED_PY"
  # shellcheck disable=SC2086
  ruff check $CHANGED_PY || FAILED=1
else
  echo "No changed Python files detected."
fi

# 3. mypy (app/)
echo ""
echo "--- Running mypy ---"
mypy app || FAILED=1

# 4. Bandit
echo ""
echo "--- Running Bandit ---"
bandit -r app || FAILED=1

# 5. Frontend checks when package.json exists
if [ -f "package.json" ]; then
  echo ""
  echo "--- Running frontend checks (pnpm) ---"
  pnpm lint || FAILED=1
  pnpm typecheck || FAILED=1
fi

echo ""
if [ "$FAILED" -eq 0 ]; then
  echo "=== All checks passed. Ready to commit! ==="
else
  echo "=== Some checks failed. Fix issues before committing. ==="
  exit 1
fi
