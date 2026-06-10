#!/usr/bin/env bash
# Deploy versioned documentation using mike.
#
# Usage:
#   ./scripts/deploy_versioned_docs.sh dev            # Deploy dev version
#   ./scripts/deploy_versioned_docs.sh 0.4.0          # Deploy release version as latest
#   ./scripts/deploy_versioned_docs.sh 0.4.0 --dry-run # Preview without pushing
#
# Prerequisites:
#   - poetry environment with docs dependencies installed
#   - git configured with push access to origin
set -euo pipefail

VERSION="${1:-}"
DRY_RUN=""
if [[ "${2:-}" == "--dry-run" ]]; then
  DRY_RUN="true"
fi

if [[ -z "$VERSION" ]]; then
  echo "Usage: $0 <version|dev> [--dry-run]"
  echo ""
  echo "  version   Deploy a release version (e.g. 0.4.0) and alias it as 'latest'"
  echo "  dev       Deploy the development version"
  echo "  --dry-run Build and commit locally, do not push to gh-pages"
  exit 1
fi

echo "==> Generating autodoc pages..."
poetry run python scripts/generate_autodoc_pages.py

if [[ "$VERSION" == "dev" ]]; then
  echo "==> Deploying dev docs..."
  if [[ -n "$DRY_RUN" ]]; then
    poetry run mike deploy dev
  else
    poetry run mike deploy --push dev
  fi
else
  echo "==> Deploying version $VERSION as latest..."
  if [[ -n "$DRY_RUN" ]]; then
    poetry run mike deploy --update-aliases "$VERSION" latest
  else
    poetry run mike deploy --push --update-aliases "$VERSION" latest
  fi
fi

echo "==> Done. View deployed versions with: poetry run mike list"
