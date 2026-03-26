#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/pipeline/commons.sh
source "$SCRIPT_DIR/commons.sh"

require_vars ACTIONS_ID_TOKEN_REQUEST_TOKEN ACTIONS_ID_TOKEN_REQUEST_URL

FAILED=0

check_oidc_token() {
  local name="$1"
  local audience="$2"

  local token
  token=$(curl --silent --fail \
    -H "Authorization: bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" \
    "${ACTIONS_ID_TOKEN_REQUEST_URL}&audience=${audience}" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['value'])" 2>/dev/null)

  if [[ -z "$token" ]]; then
    error "$name: failed to obtain OIDC token for audience '$audience'"
    FAILED=1
    return
  fi

  log "$name: OIDC token obtained for audience '$audience' (${token:0:10}...)"
}

log "Validating OIDC token availability"
check_oidc_token "PyPI"     "pypi"
check_oidc_token "TestPyPI" "pypi"

if [[ "$FAILED" -eq 1 ]]; then
  fail "One or more OIDC token requests failed"
fi

log "All OIDC tokens validated successfully"
