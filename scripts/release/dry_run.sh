#!/usr/bin/env bash
set -euo pipefail

# shellcheck source=scripts/release/common.sh
# shellcheck source=scripts/release/common.sh
source "$(dirname "$0")/common.sh"

LEVEL="${1:?release level required (patch|minor|major)}"

NEXT_VERSION="$(poetry version "$LEVEL" --dry-run | awk '{print $NF}')"

log "DRY RUN"
echo "Next version : $NEXT_VERSION"
echo "Branch       : release/v$NEXT_VERSION"
echo "Tag          : v$NEXT_VERSION"
