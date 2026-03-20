#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/pipeline/commons.sh
source "$SCRIPT_DIR/commons.sh"

require_vars PACKAGE_NAME PUBLISH_VERSION GITHUB_OUTPUT

if curl --silent --fail --output /dev/null \
    "https://test.pypi.org/pypi/${PACKAGE_NAME}/${PUBLISH_VERSION}/json"; then
  log "${PACKAGE_NAME}==${PUBLISH_VERSION} already exists on TestPyPI — skipping upload and smoke test"
  echo "already_exists=true" >> "$GITHUB_OUTPUT"
else
  log "${PACKAGE_NAME}==${PUBLISH_VERSION} not found on TestPyPI — proceeding with upload"
  echo "already_exists=false" >> "$GITHUB_OUTPUT"
fi
