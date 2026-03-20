#!/usr/bin/env bash

# shellcheck source=scripts/pipeline/commons.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/commons.sh"

require_vars PACKAGE_NAME IMPORT_NAME PUBLISH_VERSION

MAX_WAIT=120
INTERVAL=10
ELAPSED=0

log "Waiting for ${PACKAGE_NAME}==${PUBLISH_VERSION} to appear on TestPyPI..."

until pip index versions \
        --index-url https://test.pypi.org/simple/ \
        --extra-index-url https://pypi.org/simple/ \
        "$PACKAGE_NAME" 2>/dev/null | grep -q "$PUBLISH_VERSION"; do

  if [[ "$ELAPSED" -ge "$MAX_WAIT" ]]; then
    fail "Timed out after ${MAX_WAIT}s waiting for ${PACKAGE_NAME}==${PUBLISH_VERSION} on TestPyPI"
  fi

  log "Not available yet — retrying in ${INTERVAL}s (${ELAPSED}s elapsed)"
  sleep "$INTERVAL"
  ELAPSED=$(( ELAPSED + INTERVAL ))
done

log "${PACKAGE_NAME}==${PUBLISH_VERSION} is available — installing"

TMP_VENV=$(mktemp -d)
python3 -m venv "$TMP_VENV"
# shellcheck disable=SC1091
source "$TMP_VENV/bin/activate"

pip install --quiet \
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
EOF

log "Smoke test passed"
