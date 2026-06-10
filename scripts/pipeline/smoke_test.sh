#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/commons.sh"

require_vars PACKAGE_NAME IMPORT_NAME PUBLISH_VERSION

MAX_WAIT=180
INTERVAL=5
ELAPSED=0
CONSECUTIVE_SUCCESS=0
REQUIRED_SUCCESSES=2

log "Waiting for ${PACKAGE_NAME}==${PUBLISH_VERSION} to appear on TestPyPI..."

until [[ "$CONSECUTIVE_SUCCESS" -ge "$REQUIRED_SUCCESSES" ]]; do

  if [[ "$ELAPSED" -ge "$MAX_WAIT" ]]; then
    fail "Timed out after ${MAX_WAIT}s waiting for ${PACKAGE_NAME}==${PUBLISH_VERSION} on TestPyPI"
  fi

  # Check JSON API endpoint
  if curl --silent --fail --output /dev/null \
      --max-time 10 \
      "https://test.pypi.org/pypi/${PACKAGE_NAME}/${PUBLISH_VERSION}/json"; then
    CONSECUTIVE_SUCCESS=$(( CONSECUTIVE_SUCCESS + 1 ))
    log "Found package (success ${CONSECUTIVE_SUCCESS}/${REQUIRED_SUCCESSES})"
  else
    CONSECUTIVE_SUCCESS=0
    log "Not available yet — retrying in ${INTERVAL}s (${ELAPSED}s elapsed)"
  fi

  if [[ "$CONSECUTIVE_SUCCESS" -lt "$REQUIRED_SUCCESSES" ]]; then
    sleep "$INTERVAL"
    ELAPSED=$(( ELAPSED + INTERVAL ))
  fi
done

log "${PACKAGE_NAME}==${PUBLISH_VERSION} is available — installing"

TMP_VENV=$(mktemp -d)
trap "rm -rf $TMP_VENV" EXIT

python3 -m venv "$TMP_VENV"
# shellcheck disable=SC1091
source "$TMP_VENV/bin/activate"

# Use longer timeout for pip install (CDN + index queries)
pip install --quiet --no-cache-dir \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  "${PACKAGE_NAME}==${PUBLISH_VERSION}"

log "Verifying installed version"

python3 - <<EOF
import ${IMPORT_NAME}
from importlib.metadata import version

v = version("${PACKAGE_NAME}")
print(f"Detected Version: {v}")
assert v == "${PUBLISH_VERSION}", f"Expected ${PUBLISH_VERSION}, got {v}"
print("Version verification passed")
EOF

log "Smoke test passed"
