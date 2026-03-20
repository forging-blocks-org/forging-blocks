#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/commons.sh"

PACKAGE_NAME="${PACKAGE_NAME:-}"
IMPORT_NAME="${IMPORT_NAME:-}"
BASE_VERSION="${VERSION:-}"

[[ -z "$PACKAGE_NAME" ]] && fail "PACKAGE_NAME is not set"
[[ -z "$IMPORT_NAME" ]]  && fail "IMPORT_NAME is not set"
[[ -z "$BASE_VERSION" ]] && fail "VERSION is not set"
[[ -z "${GITHUB_ENV:-}" ]] && fail "GITHUB_ENV is not set — cannot export PUBLISH_VERSION to workflow"

if [[ -n "${GITHUB_RUN_NUMBER:-}" ]]; then
  VERSION="${BASE_VERSION}.dev${GITHUB_RUN_NUMBER}"
  log "CI detected → using dev version: $VERSION"
else
  VERSION="$BASE_VERSION"
  log "Local run → using version: $VERSION"
fi

echo "PUBLISH_VERSION=$VERSION" >> "$GITHUB_ENV"
log "PUBLISH_VERSION=$VERSION exported to GITHUB_ENV"

log "Installing dependencies"
poetry install --no-interaction --with dev --sync

log "Setting ephemeral version to $VERSION"
poetry version "$VERSION"

log "Cleaning and Building package"
rm -rf dist/
poetry build

log "Validating artifacts with Twine"
twine check dist/*

log "--- Pre-Publish Validation Complete ---"
