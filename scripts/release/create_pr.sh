#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/common.sh"

VERSION="$(poetry version -s)"
BRANCH="release/v$VERSION"

log "Creating PR for release $VERSION"

if command -v gh >/dev/null 2>&1; then
  gh pr create \
    --base main \
    --head "$BRANCH" \
    --title "release: $VERSION" \
    --body "Release $VERSION

This PR contains only:
- version bump
- generated changelog

Publishing happens when this PR is merged."
else
  echo "Create PR manually:"
  echo "https://github.com/forging-blocks-org/forging-blocks/compare/$BRANCH?expand=1"
fi
