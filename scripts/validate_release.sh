#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel)"
cd "$ROOT_DIR"

#######################################
# Configuration (override via env vars)
#######################################
PACKAGE_NAME="${PACKAGE_NAME:-your-package}"
IMPORT_NAME="${IMPORT_NAME:-your_package}"
TEST_PYPI_URL="https://test.pypi.org/simple"
PYPI_URL="https://pypi.org/simple"

#######################################
# Helpers
#######################################
fail() {
  echo "ERROR: $1" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Missing required command: $1"
}

#######################################
# Preconditions
#######################################
require_cmd git
require_cmd poetry
require_cmd python3
require_cmd pip

BRANCH="$(git rev-parse --abbrev-ref HEAD)"

if [[ ! "$BRANCH" =~ ^release/v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  fail "Branch must follow release/vX.Y.Z. Current: $BRANCH"
fi

VERSION_FROM_BRANCH="${BRANCH#release/v}"

PYPROJECT_VERSION="$(poetry version -s)"

if [[ "$VERSION_FROM_BRANCH" != "$PYPROJECT_VERSION" ]]; then
  fail "Version mismatch: branch=$VERSION_FROM_BRANCH pyproject=$PYPROJECT_VERSION"
fi

#######################################
# Clean previous builds
#######################################
echo "Cleaning dist/"
rm -rf dist/

#######################################
# Install deps
#######################################
echo "Installing dependencies"
poetry install --no-interaction

#######################################
# Run checks
#######################################
echo "Running CI checks"
poetry run poe ci:check

echo "Running tests"
poetry run poe test

#######################################
# Build
#######################################
echo "Building package"
poetry build

#######################################
# Validate artifacts
#######################################
echo "Validating artifacts"
pip install --quiet twine
twine check dist/*

#######################################
# Optional: inspect artifacts
#######################################
echo "Inspecting artifacts"
tar -tf dist/*.tar.gz >/dev/null
unzip -l dist/*.whl >/dev/null

#######################################
# Publish to TestPyPI
#######################################
if [[ -z "${TEST_PYPI_TOKEN:-}" ]]; then
  fail "TEST_PYPI_TOKEN is not set"
fi

echo "Publishing to TestPyPI"
poetry publish -r testpypi \
  --username __token__ \
  --password "$TEST_PYPI_TOKEN"

#######################################
# Install from TestPyPI
#######################################
echo "Creating isolated venv for install test"
TMP_VENV="$(mktemp -d)"
python3 -m venv "$TMP_VENV"

source "$TMP_VENV/bin/activate"

pip install --upgrade pip >/dev/null

echo "Installing from TestPyPI"
pip install \
  --index-url "$TEST_PYPI_URL" \
  --extra-index-url "$PYPI_URL" \
  "$PACKAGE_NAME"

#######################################
# Smoke test
#######################################
echo "Running import test"
python -c "import $IMPORT_NAME"

#######################################
# Optional CLI check
#######################################
if command -v "$PACKAGE_NAME" >/dev/null 2>&1; then
  "$PACKAGE_NAME" --help >/dev/null || fail "CLI check failed"
fi

deactivate
rm -rf "$TMP_VENV"

#######################################
# Done
#######################################
echo "Release validation succeeded for version $VERSION_FROM_BRANCH"
