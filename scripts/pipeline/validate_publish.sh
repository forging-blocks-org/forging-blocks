#!/usr/bin/env bash

set -euo pipefail

log()   { printf "\033[1;34m[INFO]\033[0m %s\n" "$1"; }
warn()  { printf "\033[1;33m[WARN]\033[0m %s\n" "$1"; }
error() { printf "\033[1;31m[ERROR]\033[0m %s\n" "$1" >&2; }
fail()  { error "$1"; exit 1; }

trap 'fail "Script failed at line $LINENO"' ERR

PACKAGE_NAME="${PACKAGE_NAME:-}"
IMPORT_NAME="${IMPORT_NAME:-}"
BASE_VERSION="${VERSION:-}"

[[ -z "$PACKAGE_NAME" ]] && fail "PACKAGE_NAME is not set"
[[ -z "$IMPORT_NAME" ]] && fail "IMPORT_NAME is not set"
[[ -z "$BASE_VERSION" ]] && fail "VERSION is not set"
[[ -z "${GITHUB_ENV:-}" ]] && fail "GITHUB_ENV is not set — cannot export PUBLISH_VERSION to workflow"

# Derive CI version
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
