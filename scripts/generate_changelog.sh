#!/usr/bin/env bash
set -euo pipefail

CURRENT_VERSION="$(poetry version -s)"
CURRENT_TAG="v$CURRENT_VERSION"

PREVIOUS_TAG="$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo '')"

DATE="$(date +%Y-%m-%d)"

echo "## $CURRENT_TAG – $DATE"
echo

declare -A SECTIONS=(
  ["feat"]="🚀 Features"
  ["fix"]="🐛 Fixes"
  ["docs"]="📚 Documentation"
  ["refactor"]="♻️ Refactors"
  ["perf"]="⚡ Performance"
  ["test"]="🧪 Tests"
  ["chore"]="🛠️ Chores"
  ["breaking"]="⚠️ Breaking Changes"
)

for TYPE in "${!SECTIONS[@]}"; do
  COMMITS="$(git log ${PREVIOUS_TAG:+$PREVIOUS_TAG..HEAD} \
    --pretty=format:'%s' | grep "^$TYPE" || true)"

  if [[ -n "$COMMITS" ]]; then
    echo "### ${SECTIONS[$TYPE]}"
    echo "$COMMITS" | sed -E 's/^[a-z]+(\([^)]+\))?: /- /'
    echo
  fi
done
