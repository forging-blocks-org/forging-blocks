#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/pipeline/commons.sh
source "$SCRIPT_DIR/commons.sh"

require_vars RELEASE_VERSION

[[ -z "$RELEASE_VERSION" ]] && fail "prepare_release.sh did not set version output"

semver_pattern='^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$'
[[ "$RELEASE_VERSION" =~ $semver_pattern ]] ||
  fail "Release version must be normalized SemVer (MAJOR.MINOR.PATCH): $RELEASE_VERSION"

log "Release version validated: $RELEASE_VERSION"
