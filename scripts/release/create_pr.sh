#!/usr/bin/env bash
set -euo pipefail

# shellcheck source=scripts/release/common.sh
source "$(dirname "$0")/common.sh"

VERSION="$(poetry version -s)"
BRANCH="release/v$VERSION"
BASE="main"

log "Preparing Pull Request for $BRANCH → $BASE"

# --- Ensure branch exists locally ---
if ! git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  echo "ERROR: release branch does not exist locally: $BRANCH"
  echo "Run prepare.sh first."
  exit 1
fi

# --- Ensure branch is pushed ---
if ! git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null 2>&1; then
  log "Pushing branch $BRANCH to origin"
  git push origin "$BRANCH"
fi

# --- GitHub CLI availability ---
if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) not installed."
  echo "Create PR manually:"
  echo "https://github.com/forging-blocks-org/forging-blocks/compare/$BRANCH?expand=1"
  exit 0
fi

# --- Authentication check ---
if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI is not authenticated."
  echo "Run: gh auth login"
  echo "Then re-run this command."
  exit 1
fi

# --- Check if PR already exists ---
if gh pr view "$BRANCH" --repo forging-blocks-org/forging-blocks >/dev/null 2>&1; then
  log "Pull Request already exists for $BRANCH"
  gh pr view "$BRANCH" --repo forging-blocks-org/forging-blocks
  exit 0
fi

# --- Create PR ---
log "Creating Pull Request"

gh pr create \
  --base "$BASE" \
  --head "$BRANCH" \
  --title "release: $VERSION" \
  --body "Release $VERSION

This PR contains:
- version bump
- generated changelog
- release metadata

Publishing to PyPI and docs deployment will occur automatically when this PR is merged."

log "Pull Request created successfully"
