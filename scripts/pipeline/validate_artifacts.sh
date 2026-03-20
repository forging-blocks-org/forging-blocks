#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/commons.sh"

log "Building package"
poetry build

log "Installing Twine"
pip install --quiet twine

log "Validating artifacts"
twine check dist/*
