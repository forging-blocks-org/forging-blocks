#!/usr/bin/env bash
#
# validate_publish_local.sh
#
# Runs the FULL validate-publish CI job locally, end-to-end:
#   1. Install dependencies
#   2. Build & validate artifacts with Twine
#   3. Check TestPyPI for existing version
#   4. OPTIONAL: Publish to TestPyPI (--publish flag)
#   5. OPTIONAL: Smoke test from TestPyPI (--smoke flag)
#
# Usage:
#   bash scripts/pipeline/validate_publish_local.sh              # dry-run (no publish)
#   bash scripts/pipeline/validate_publish_local.sh --publish    # also publish to TestPyPI
#   bash scripts/pipeline/validate_publish_local.sh --publish --smoke  # publish + smoke test
#
# Prerequisites:
#   - poetry (auto-installed if missing)
#   - TEST_PYPI_TOKEN env var must be set when using --publish
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# shellcheck source=scripts/pipeline/commons.sh
source "$SCRIPT_DIR/commons.sh"

# ── Parse flags ──────────────────────────────────────────────────────────────
DO_PUBLISH=false
DO_SMOKE=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --publish) DO_PUBLISH=true; shift ;;
    --smoke)   DO_SMOKE=true;   shift ;;
    --help|-h)
      echo "Usage: $0 [--publish] [--smoke]"
      echo ""
      echo "  (no flags)    Dry-run: build + validate + check TestPyPI only"
      echo "  --publish     Also publish to TestPyPI"
      echo "  --smoke       Also run smoke test (requires --publish or existing TestPyPI package)"
      exit 0
      ;;
    *) fail "Unknown flag: $1" ;;
  esac
done

if [[ "$DO_SMOKE" == true && "$DO_PUBLISH" == false ]]; then
  warn "--smoke used without --publish: will only smoke-test if package already exists on TestPyPI"
fi

# ── Step 0: Setup env vars ───────────────────────────────────────────────────
export PACKAGE_NAME="${PACKAGE_NAME:-$( (cd "$REPO_ROOT" && poetry version 2>/dev/null | cut -d' ' -f1) || true )}"
export IMPORT_NAME="${IMPORT_NAME:-${PACKAGE_NAME//-/_}}"
BASE_VERSION="${VERSION:-$( (cd "$REPO_ROOT" && poetry version -s 2>/dev/null) || true )}"

[[ -z "$PACKAGE_NAME" ]] && fail "PACKAGE_NAME could not be auto-detected"
[[ -z "$BASE_VERSION" ]] && fail "VERSION could not be auto-detected"

if [[ -n "${GITHUB_RUN_NUMBER:-}" ]]; then
  export PUBLISH_VERSION="${BASE_VERSION}.dev${GITHUB_RUN_NUMBER}"
else
  export PUBLISH_VERSION="$BASE_VERSION"
fi

log "=============================================="
log "LOCAL VALIDATE-PUBLISH PIPELINE"
log "=============================================="
log "  PACKAGE_NAME=${PACKAGE_NAME}"
log "  IMPORT_NAME=${IMPORT_NAME}"
log "  PUBLISH_VERSION=${PUBLISH_VERSION}"
log "  Publish to TestPyPI: ${DO_PUBLISH}"
log "  Smoke test:          ${DO_SMOKE}"
log "=============================================="

# ── Step 1: Install dependencies ─────────────────────────────────────────────
log ""
log "━━━ Step 1/5: Installing dependencies ━━━"
poetry install --no-interaction --with dev
pip install --quiet twine || fail "Failed to install twine"

# ── Step 2: Build & validate artifacts ───────────────────────────────────────
log ""
log "━━━ Step 2/5: Building & validating with Twine ━━━"
VERSION="$PUBLISH_VERSION" bash "$SCRIPT_DIR/validate_publish.sh"

# ── Step 3: Validate PUBLISH_VERSION ─────────────────────────────────────────
log ""
log "━━━ Step 3/5: Validating PUBLISH_VERSION ━━━"
bash "$SCRIPT_DIR/validate_publish_version.sh"

# ── Step 4: Check TestPyPI ───────────────────────────────────────────────────
log ""
log "━━━ Step 4/5: Checking TestPyPI ━━━"
bash "$SCRIPT_DIR/check_testpypi.sh"
ALREADY_EXISTS="${CHECK_ALREADY_EXISTS:-false}"

# ── Step 5a: Publish to TestPyPI (optional) ──────────────────────────────────
if [[ "$DO_PUBLISH" == true ]]; then
  if [[ "$ALREADY_EXISTS" == true ]]; then
    log ""
    log "━━━ Step 5a: Skipping TestPyPI publish (already exists) ━━━"
  else
    if [[ -z "${TEST_PYPI_TOKEN:-}" ]]; then
      fail "TEST_PYPI_TOKEN env var is not set. Required for publishing to TestPyPI."
    fi
    log ""
    log "━━━ Step 5a: Publishing to TestPyPI ━━━"
    poetry publish \
      --repository testpypi \
      --username __token__ \
      --password "$TEST_PYPI_TOKEN"
    log "Published ${PACKAGE_NAME}==${PUBLISH_VERSION} to TestPyPI"
  fi
fi

# ── Step 5b: Smoke test (optional) ───────────────────────────────────────────
if [[ "$DO_SMOKE" == true ]]; then
  log ""
  log "━━━ Step 5b: Smoke testing from TestPyPI ━━━"
  bash "$SCRIPT_DIR/smoke_test.sh"
fi

# ── Summary ──────────────────────────────────────────────────────────────────
log ""
log "=============================================="
log "PIPELINE COMPLETE"
log "  Package:   ${PACKAGE_NAME}==${PUBLISH_VERSION}"
log "  Published: ${DO_PUBLISH}"
log "  Smoke:     ${DO_SMOKE}"
log "  on TestPyPI already: ${ALREADY_EXISTS}"
log "=============================================="

if [[ "$DO_PUBLISH" == false ]]; then
  log ""
  log "💡 To publish and smoke-test, re-run with:"
  log "   TEST_PYPI_TOKEN=<token> bash scripts/pipeline/validate_publish_local.sh --publish --smoke"
fi
