#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/pipeline/commons.sh
source "$SCRIPT_DIR/commons.sh"

require_vars PYPI_TOKEN TEST_PYPI_TOKEN

FAILED=0

check_token_auth() {
  local name="$1"
  local token="$2"
  local url="$3"

  local http_status
  http_status=$(curl --silent --output /dev/null --write-out "%{http_code}" \
    --header "Authorization: Bearer $token" \
    "$url")

  if [[ "$http_status" == "200" ]]; then
    log "$name is valid (HTTP $http_status)"
  elif [[ "$http_status" == "401" ]]; then
    error "$name is invalid or expired (HTTP $http_status)"
    FAILED=1
  else
    error "$name returned unexpected HTTP $http_status from $url"
    FAILED=1
  fi
}

log "Validating token authentication"
check_token_auth "PYPI_TOKEN"      "$PYPI_TOKEN"      "https://pypi.org/pypi"
check_token_auth "TEST_PYPI_TOKEN" "$TEST_PYPI_TOKEN" "https://test.pypi.org/pypi"

if [[ "$FAILED" -eq 1 ]]; then
  fail "One or more tokens failed authentication"
fi

log "All tokens validated successfully"
