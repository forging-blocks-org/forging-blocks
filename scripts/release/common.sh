#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RELEASE_SCRIPTS_VERSION="$(cat "$SCRIPT_DIR/VERSION")"

log() {
  echo "[release-scripts v$RELEASE_SCRIPTS_VERSION] $*"
}
