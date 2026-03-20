#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/commons.sh"

if ! command -v git &> /dev/null; then
  fail "git is not installed in the container. Please use the 'Medium' act image."
fi

VERSION="${HEAD_REF#release/}"

if [[ -z "$VERSION" || "$VERSION" == "$HEAD_REF" ]]; then
  fail "Could not extract version from branch: $HEAD_REF"
fi

log "Extracted version: $VERSION"
echo "version=$VERSION" >> "$GITHUB_OUTPUT"

git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"

if git ls-remote --tags origin "$VERSION" | grep -q .; then
  log "Tag $VERSION already exists on remote. Skipping creation."
else
  log "Creating tag $VERSION"
  git tag "$VERSION"

  if [[ "${ACT:-}" != "true" ]]; then
    git push origin "refs/tags/$VERSION"
  else
    log "Local simulation detected. Skipping git push."
  fi
fi
