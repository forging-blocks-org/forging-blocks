#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/common.sh"

LEVEL="${1:?release level required (patch|minor|major)}"

log "Preparing release ($LEVEL)"

poetry version "$LEVEL"

VERSION="$(poetry version -s)"
BRANCH="release/v$VERSION"
TAG="v$VERSION"

git fetch origin --tags

git show-ref --verify --quiet "refs/heads/$BRANCH" && {
  echo "ERROR: release branch already exists: $BRANCH"
  exit 1
}

git rev-parse "$TAG" >/dev/null 2>&1 && {
  echo "ERROR: tag already exists: $TAG"
  exit 1
}

git checkout -b "$BRANCH"
git add pyproject.toml poetry.lock
[ -f CHANGELOG.md ] && git add CHANGELOG.md
git commit -m "release: $VERSION - version bump and changelog"
git tag "$TAG"
git push origin "$BRANCH" --tags

log "Release $VERSION prepared"
