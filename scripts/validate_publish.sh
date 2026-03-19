#!/usr/bin/env bash

set -euo pipefail

#######################################
# Logging
#######################################
log()   { printf "\033[1;34m[INFO]\033[0m %s\n" "$1"; }
warn()  { printf "\033[1;33m[WARN]\033[0m %s\n" "$1"; }
error() { printf "\033[1;31m[ERROR]\033[0m %s\n" "$1" >&2; }
fail()  { error "$1"; exit 1; }

trap 'fail "Script failed at line $LINENO"' ERR

#######################################
# Config
#######################################
PACKAGE_NAME="${PACKAGE_NAME:-}"
IMPORT_NAME="${IMPORT_NAME:-}"
BASE_VERSION="${VERSION:-}"

TEST_PYPI_URL="https://test.pypi.org/simple"
PYPI_URL="https://pypi.org/simple"

#######################################
# Validate env
#######################################
[[ -z "$PACKAGE_NAME" ]] && fail "PACKAGE_NAME is not set"
[[ -z "$IMPORT_NAME" ]] && fail "IMPORT_NAME is not set"
[[ -z "$BASE_VERSION" ]] && fail "VERSION is not set"
[[ -z "${TEST_PYPI_TOKEN:-}" ]] && fail "TEST_PYPI_TOKEN is not set"

#######################################
# Derive CI version
#######################################
if [[ -n "${GITHUB_RUN_NUMBER:-}" ]]; then
  VERSION="${BASE_VERSION}.dev${GITHUB_RUN_NUMBER}"
  log "CI detected → using dev version: $VERSION"
else
  VERSION="$BASE_VERSION"
  log "Local run → using version: $VERSION"
fi

#######################################
# Install deps
#######################################
log "Installing dependencies"
poetry install --no-interaction --with dev

#######################################
# Set version (ephemeral)
#######################################
log "Setting version to $VERSION"
poetry version "$VERSION"

#######################################
# Build
#######################################
log "Cleaning dist/"
rm -rf dist/

log "Building package"
poetry build

#######################################
# Validate artifacts
#######################################
log "Validating artifacts"
twine check dist/*

#######################################
# Idempotency check
#######################################
log "Checking if version already exists on TestPyPI"

if pip index versions "$PACKAGE_NAME" \
  --index-url "$TEST_PYPI_URL" 2>/dev/null | grep -q "$VERSION"; then
  warn "Version $VERSION already exists → skipping publish"
  SKIP_PUBLISH=true
else
  SKIP_PUBLISH=false
fi

# expose to GitHub Actions + log
echo "SKIP_PUBLISH=$SKIP_PUBLISH" | tee -a "$GITHUB_ENV"

#######################################
# Publish
#######################################
if [[ "$SKIP_PUBLISH" == false ]]; then
  log "Publishing to TestPyPI"

  poetry publish \
    --repository testpypi \
    --username __token__ \
    --password "$TEST_PYPI_TOKEN"
else
  warn "Skipping publish (idempotent)"
fi

#######################################
# Install validation (with retry)
#######################################
log "Creating isolated environment"

TMP_VENV="$(mktemp -d)"
python3 -m venv "$TMP_VENV"

# shellcheck disable=SC1090
source "$TMP_VENV/bin/activate"

pip install --upgrade pip >/dev/null

log "Installing from TestPyPI (with retry)"

MAX_ATTEMPTS=10
SLEEP_SECONDS=5
SUCCESS=false

for i in $(seq 1 $MAX_ATTEMPTS); do
  if pip install \
    --index-url "$TEST_PYPI_URL" \
    --extra-index-url "$PYPI_URL" \
    "$PACKAGE_NAME==$VERSION"; then
    SUCCESS=true
    log "Install succeeded"
    break
  fi

  warn "Not available yet (attempt $i/$MAX_ATTEMPTS)"
  sleep $SLEEP_SECONDS
done

if [[ "$SUCCESS" == false ]]; then
  fail "Package not available after $MAX_ATTEMPTS attempts"
fi

#######################################
# Smoke test
#######################################
log "Running import test"

python - <<EOF
import $IMPORT_NAME
assert $IMPORT_NAME.__version__ == "$VERSION"
print("Version OK:", $IMPORT_NAME.__version__)
EOF

#######################################
# Optional CLI validation
#######################################
if command -v "$PACKAGE_NAME" >/dev/null 2>&1; then
  log "Running CLI check"
  "$PACKAGE_NAME" --help >/dev/null
else
  warn "CLI not found, skipping"
fi

deactivate
rm -rf "$TMP_VENV"

#######################################
# Final report
#######################################
log "----------------------------------------"
log "VALIDATION SUMMARY"
log "Base Version: $BASE_VERSION"
log "Published Version: $VERSION"
log "Publish skipped: $SKIP_PUBLISH"
log "----------------------------------------"
