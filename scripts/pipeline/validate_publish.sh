#!/usr/bin/env bash

# shellcheck source=scripts/pipeline/commons.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/commons.sh"

require_vars PACKAGE_NAME IMPORT_NAME VERSION GITHUB_ENV

BASE_VERSION="$VERSION"

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
