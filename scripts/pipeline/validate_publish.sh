#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# shellcheck source=scripts/pipeline/commons.sh
source "$SCRIPT_DIR/commons.sh"

# ── Auto-detect values from pyproject.toml when not provided ────────────────
if [[ -z "${PACKAGE_NAME:-}" ]]; then
  PACKAGE_NAME="$(cd "$REPO_ROOT" && poetry version 2>/dev/null | cut -d' ' -f1 || true)"
  if [[ -z "$PACKAGE_NAME" ]]; then
    fail "PACKAGE_NAME is not set and could not be auto-detected from pyproject.toml"
  fi
  log "PACKAGE_NAME auto-detected: $PACKAGE_NAME"
fi

if [[ -z "${VERSION:-}" ]]; then
  VERSION="$(cd "$REPO_ROOT" && poetry version -s 2>/dev/null || true)"
  if [[ -z "$VERSION" ]]; then
    fail "VERSION is not set and could not be auto-detected from pyproject.toml"
  fi
  log "VERSION auto-detected: $VERSION"
fi

if [[ -z "${IMPORT_NAME:-}" ]]; then
  IMPORT_NAME="${PACKAGE_NAME//-/_}"
  log "IMPORT_NAME auto-detected from PACKAGE_NAME: $IMPORT_NAME"
fi

BASE_VERSION="$VERSION"

if [[ -n "${GITHUB_RUN_NUMBER:-}" ]]; then
  VERSION="${BASE_VERSION}.dev${GITHUB_RUN_NUMBER}"
  log "CI detected → using dev version: $VERSION"
else
  VERSION="$BASE_VERSION"
  log "Local run → using version: $VERSION"
fi

export PUBLISH_VERSION="$VERSION"

# Export to GITHUB_ENV if running in CI; skip gracefully on local runs
if [[ -n "${GITHUB_ENV:-}" && -f "$GITHUB_ENV" ]]; then
  echo "PUBLISH_VERSION=$VERSION" >> "$GITHUB_ENV"
  log "PUBLISH_VERSION=$VERSION exported to GITHUB_ENV"
else
  log "GITHUB_ENV not set or not a file — skipping GITHUB_ENV export (local run)"
fi

log "Installing dependencies"
poetry install --no-interaction --with dev

log "Installing Twine (if not already present)"
pip install --quiet twine || fail "Failed to install twine"

log "Setting ephemeral version to $VERSION"
poetry version "$VERSION"

log "Cleaning and Building package"
rm -rf dist/
poetry build

log "Validating artifacts with Twine"
twine check dist/*

log "--- Pre-Publish Validation Complete ---"
log "  PACKAGE_NAME=${PACKAGE_NAME}"
log "  IMPORT_NAME=${IMPORT_NAME}"
log "  PUBLISH_VERSION=${PUBLISH_VERSION}"
