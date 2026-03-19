#!/usr/bin/env bash

set -euo pipefail

#######################################
# Logging
#######################################
log() {
  printf "\033[1;34m[INFO]\033[0m %s\n" "$1"
}

warn() {
  printf "\033[1;33m[WARN]\033[0m %s\n" "$1"
}

error() {
  printf "\033[1;31m[ERROR]\033[0m %s\n" "$1" >&2
}

fail() {
  error "$1"
  exit 1
}

#######################################
# Config
#######################################
ROOT_DIR="$(git rev-parse --show-toplevel)"
cd "$ROOT_DIR"

PACKAGE_NAME="${PACKAGE_NAME:-}"
IMPORT_NAME="${IMPORT_NAME:-}"
VERSION="${VERSION:-}"

TEST_PYPI_URL="https://test.pypi.org/simple"
PYPI_URL="https://pypi.org/simple"

#######################################
# Preconditions
#######################################
require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Missing required command: $1"
}

log "Checking required tools"
require_cmd git
require_cmd poetry
require_cmd python3
require_cmd pip

#######################################
# Validate env vars
#######################################
log "Validating environment variables"

[[ -z "$PACKAGE_NAME" ]] && fail "PACKAGE_NAME is not set"
[[ -z "$IMPORT_NAME" ]] && fail "IMPORT_NAME is not set"
[[ -z "$VERSION" ]] && fail "VERSION is not set"

if [[ -z "${TEST_PYPI_TOKEN:-}" ]]; then
  fail "TEST_PYPI_TOKEN is not set"
fi

#######################################
# Ensure clean state
#######################################
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

if [[ "$CURRENT_BRANCH" != "main" ]]; then
  warn "You are not on main (current: $CURRENT_BRANCH)"
fi

log "Ensuring working tree is clean"
git diff --quiet || fail "Working tree is dirty"
git diff --cached --quiet || fail "Staged changes detected"

#######################################
# Create temporary release branch
#######################################
RELEASE_BRANCH="release/v$VERSION"

log "Creating temporary release branch: $RELEASE_BRANCH"
git checkout -b "$RELEASE_BRANCH"

#######################################
# Sync version
#######################################
log "Setting version in pyproject.toml"
poetry version "$VERSION"

git add pyproject.toml
git commit -m "chore(release): v$VERSION"

#######################################
# Clean previous builds
#######################################
log "Cleaning dist/"
rm -rf dist/

#######################################
# Install deps
#######################################
log "Installing dependencies"
poetry install --no-interaction

#######################################
# Run checks
#######################################
log "Running CI checks"
poetry run poe ci:check

log "Running tests"
poetry run poe test

#######################################
# Build
#######################################
log "Building package"
poetry build

#######################################
# Validate artifacts
#######################################
log "Validating artifacts"
pip install --quiet twine
twine check dist/*

#######################################
# Inspect artifacts
#######################################
log "Inspecting artifacts"
tar -tf dist/*.tar.gz >/dev/null
unzip -l dist/*.whl >/dev/null

#######################################
# Publish to TestPyPI ONLY
#######################################
log "Publishing to TestPyPI"
poetry publish -r testpypi \
  --username __token__ \
  --password "$TEST_PYPI_TOKEN"

#######################################
# Install from TestPyPI
#######################################
log "Creating isolated virtualenv"
TMP_VENV="$(mktemp -d)"
python3 -m venv "$TMP_VENV"

# shellcheck disable=SC1090
source "$TMP_VENV/bin/activate"

pip install --upgrade pip >/dev/null

log "Installing package from TestPyPI"
pip install \
  --index-url "$TEST_PYPI_URL" \
  --extra-index-url "$PYPI_URL" \
  "$PACKAGE_NAME"

#######################################
# Smoke test
#######################################
log "Running import test"
python -c "import $IMPORT_NAME; print($IMPORT_NAME.__version__)"

#######################################
# CLI validation (optional)
#######################################
if command -v "$PACKAGE_NAME" >/dev/null 2>&1; then
  log "Running CLI check"
  "$PACKAGE_NAME" --help >/dev/null || fail "CLI check failed"
else
  warn "CLI not found, skipping"
fi

deactivate
rm -rf "$TMP_VENV"

#######################################
# Final report
#######################################
log "----------------------------------------"
log "Publish Validation Report"
log "----------------------------------------"
log "Version: $VERSION"
log "Branch (temp): $RELEASE_BRANCH"
log "Package: $PACKAGE_NAME"
log "Import: $IMPORT_NAME"
log "TestPyPI publish: SUCCESS"
log "Install test: SUCCESS"
log "----------------------------------------"

#######################################
# Cleanup (always rollback)
#######################################
log "Cleaning up temporary branch"

git checkout "$CURRENT_BRANCH"
git branch -D "$RELEASE_BRANCH"

log "Validation completed successfully"
