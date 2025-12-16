#!/usr/bin/env bash
set -euo pipefail

# shellcheck source=scripts/release/common.sh
source "$(dirname "$0")/common.sh"

LEVEL="${1:?release level required (patch|minor|major)}"

log "Preparing release ($LEVEL)"

# ---------- helpers ----------

compute_next_version() {
  poetry version "$LEVEL" --dry-run | awk '{print $NF}'
}

has_remote_origin() {
  git remote get-url origin >/dev/null 2>&1
}

fetch_tags_if_possible() {
  if has_remote_origin; then
    git fetch origin --tags
  else
    log "No remote 'origin' configured — skipping fetch"
  fi
}

tag_exists() {
  git rev-parse "v$1" >/dev/null 2>&1
}

branch_exists() {
  git show-ref --verify --quiet "refs/heads/release/v$1"
}

checkout_or_create_branch() {
  local version="$1"

  if branch_exists "$version"; then
    log "Release branch already exists — resuming release/v$version"
    git checkout "release/v$version"
    return 1
  else
    git checkout -b "release/v$version"
    return 0
  fi
}

commit_if_needed() {
  git add pyproject.toml poetry.lock || true
  [ -f CHANGELOG.md ] && git add CHANGELOG.md

  if git diff --cached --quiet; then
    log "No changes to commit — skipping commit"
  else
    git commit -m "release: $VERSION - version bump and changelog"
  fi
}

push_if_possible() {
  if has_remote_origin; then
    git push origin "release/v$VERSION" --tags
  else
    log "No remote 'origin' configured — skipping push"
  fi
}

# ---------- main ----------

NEXT_VERSION="$(compute_next_version)"
VERSION="$NEXT_VERSION"

fetch_tags_if_possible

# HARD INVARIANT: tag is final
if tag_exists "$VERSION"; then
  echo "ERROR: tag already exists: v$VERSION"
  exit 1
fi

BRANCH_CREATED=true
if ! checkout_or_create_branch "$VERSION"; then
  BRANCH_CREATED=false
fi

if [ "$BRANCH_CREATED" = true ]; then
  poetry version "$LEVEL"
fi

git tag "v$VERSION"

commit_if_needed
push_if_possible

log "Release $VERSION prepared successfully"
