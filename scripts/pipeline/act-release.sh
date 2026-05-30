#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

VERSION="${1:-}"

if [[ -z "$VERSION" ]]; then
  CURRENT_BRANCH=$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)
  if [[ "$CURRENT_BRANCH" == release/v* ]]; then
    VERSION="${CURRENT_BRANCH#release/}"
  else
    echo "Usage: $0 <version>  (e.g. $0 v0.3.22)" >&2
    echo "Or run from a release/v* branch to auto-detect." >&2
    exit 1
  fi
fi

EVENT_FILE=$(mktemp /tmp/release_event_XXXXXX.json)
trap 'rm -f "$EVENT_FILE"' EXIT

cat > "$EVENT_FILE" <<EOF
{
  "pull_request": {
    "merged": true,
    "base": {
      "ref": "main"
    },
    "head": {
      "ref": "release/${VERSION}"
    }
  }
}
EOF

echo "Using head.ref: release/${VERSION}"

act pull_request \
  -j release \
  -W "$REPO_ROOT/.github/workflows/release.yml" \
  --container-daemon-socket "$XDG_RUNTIME_DIR/podman/podman.sock" \
  --secret-file "$REPO_ROOT/.secrets.act" \
  -e "$EVENT_FILE"
