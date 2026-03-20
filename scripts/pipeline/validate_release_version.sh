#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/pipeline/commons.sh
source "$SCRIPT_DIR/commons.sh"

require_vars RELEASE_VERSION

[[ -z "$RELEASE_VERSION" ]] && fail "prepare_release.sh did not set version output"

log "Release version validated: $RELEASE_VERSION"
