#!/usr/bin/env bash
# Deploy versioned documentation using mike.
#
# Usage:
#   ./scripts/deploy_versioned_docs.sh dev                      # Deploy dev version
#   ./scripts/deploy_versioned_docs.sh 0.4.0                    # Deploy release version as latest
#   ./scripts/deploy_versioned_docs.sh 0.4.0 --dry-run          # Preview without pushing
#   ./scripts/deploy_versioned_docs.sh dev --ignore-remote-status  # Deploy ignoring remote status
#
# Prerequisites:
#   - poetry environment with docs dependencies installed
#   - git configured with push access to origin
set -euo pipefail

VERSION=""
DRY_RUN=""
IGNORE_REMOTE_STATUS=""

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN="true" ;;
    --ignore-remote-status) IGNORE_REMOTE_STATUS="true" ;;
    *)
      if [[ -z "$VERSION" ]]; then
        VERSION="$arg"
      else
        echo "ERROR: Unexpected argument '$arg'" >&2
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$VERSION" ]]; then
  echo "Usage: $0 <version|dev> [--dry-run] [--ignore-remote-status]"
  echo ""
  echo "  version                Deploy a release version (e.g. 0.4.0) and alias it as 'latest'"
  echo "  dev                    Deploy the development version"
  echo "  --dry-run              Build and commit locally, do not push to gh-pages"
  echo "  --ignore-remote-status Ignore remote status check (useful in CI)"
  exit 1
fi

echo "==> Generating autodoc pages..."
poetry run python scripts/generate_autodoc_pages.py

MIKE_OPTS=""
if [[ -n "$IGNORE_REMOTE_STATUS" ]]; then
  MIKE_OPTS="--ignore-remote-status"
fi

if [[ "$VERSION" == "dev" ]]; then
  echo "==> Deploying dev docs..."
  if [[ -n "$DRY_RUN" ]]; then
    poetry run mike deploy $MIKE_OPTS dev
  else
    poetry run mike deploy --push $MIKE_OPTS dev
  fi
  echo "==> Setting default version to dev..."
  if [[ -n "$DRY_RUN" ]]; then
    poetry run mike set-default $MIKE_OPTS dev
  else
    poetry run mike set-default --push $MIKE_OPTS dev
  fi
else
  echo "==> Deploying version $VERSION as latest..."
  if [[ -n "$DRY_RUN" ]]; then
    poetry run mike deploy --update-aliases $MIKE_OPTS "$VERSION" latest
  else
    poetry run mike deploy --push --update-aliases $MIKE_OPTS "$VERSION" latest
  fi
  echo "==> Setting default version to latest..."
  if [[ -n "$DRY_RUN" ]]; then
    poetry run mike set-default $MIKE_OPTS latest
  else
    poetry run mike set-default --push $MIKE_OPTS latest
  fi
fi

echo "==> Done. View deployed versions with: poetry run mike list"
