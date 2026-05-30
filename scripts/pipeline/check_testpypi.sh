#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/pipeline/commons.sh
source "$SCRIPT_DIR/commons.sh"

require_vars PACKAGE_NAME PUBLISH_VERSION

BASE_VERSION="${PUBLISH_VERSION%%\.dev*}"

ALREADY_EXISTS="false"

if [[ "$BASE_VERSION" != "$PUBLISH_VERSION" ]]; then
  if curl --silent --fail --output /dev/null \
      "https://pypi.org/pypi/${PACKAGE_NAME}/${BASE_VERSION}/json"; then
    log "Stable version ${BASE_VERSION} is already published on PyPI — skipping upload and smoke test"
    ALREADY_EXISTS="true"
    export CHECK_ALREADY_EXISTS="$ALREADY_EXISTS"
    [[ -n "${GITHUB_OUTPUT:-}" ]] && echo "already_exists=true" >> "$GITHUB_OUTPUT"
    exit 0
  fi
fi

if curl --silent --fail --output /dev/null \
    "https://test.pypi.org/pypi/${PACKAGE_NAME}/${PUBLISH_VERSION}/json"; then
  log "${PACKAGE_NAME}==${PUBLISH_VERSION} already exists on TestPyPI — skipping upload and smoke test"
  ALREADY_EXISTS="true"
else
  log "${PACKAGE_NAME}==${PUBLISH_VERSION} not found on TestPyPI — proceeding with upload"
fi

export CHECK_ALREADY_EXISTS="$ALREADY_EXISTS"

if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
  echo "already_exists=${ALREADY_EXISTS}" >> "$GITHUB_OUTPUT"
fi
