#!/usr/bin/env bash

set -euo pipefail

log()   { printf "\033[1;34m[INFO]\033[0m %s\n" "$1"; }
warn()  { printf "\033[1;33m[WARN]\033[0m %s\n" "$1"; }
error() { printf "\033[1;31m[ERROR]\033[0m %s\n" "$1" >&2; }
fail()  { error "$1"; exit 1; }

trap 'fail "Script failed at line $LINENO"' ERR

require_vars() {
  local missing=()
  for var in "$@"; do
    if [[ -z "${!var:-}" ]]; then
      missing+=("$var")
    fi
  done
  if [[ "${#missing[@]}" -gt 0 ]]; then
    error "The following required env vars are not set:"
    for var in "${missing[@]}"; do
      error "  - $var"
    done
    exit 1
  fi
}
