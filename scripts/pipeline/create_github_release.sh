#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/pipeline/commons.sh
source "$SCRIPT_DIR/commons.sh"

# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------

usage() {
  cat <<EOF
Usage: RELEASE_VERSION=<version> $0 [--dry-run] [--draft]

  --dry-run   Print what would happen without creating a release.
  --draft     Create the release as a draft (hidden until manually published).

Environment:
  RELEASE_VERSION   (required) The semantic version to release, e.g. "0.4.0".
  ACT               If set to "true", behaves like --dry-run (for local act simulation).
EOF
  exit 1
}

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

parse_arguments() {
  DRY_RUN=false
  DRAFT=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dry-run) DRY_RUN=true ;;
      --draft)   DRAFT=true ;;
      --help|-h) usage ;;
      *)         fail "Unknown argument: $1. Use --dry-run, --draft, or --help." ;;
    esac
    shift
  done
}

# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

escape_version_for_regex() {
  local version="$1"
  echo "${version//./\\.}"
}

extract_release_notes() {
  local version_escaped="$1"
  local changelog_file="$2"

  awk -v ver="$version_escaped" '
    BEGIN { found = 0 }
    $0 ~ "^## \\[" ver "\\]" {
      found = 1
      next
    }
    found && $0 ~ "^## \\[" {
      exit
    }
    found {
      print
    }
  ' "$changelog_file"
}

create_github_release() {
  local version="$1"
  local notes="$2"
  local draft="$3"

  local notes_file
  notes_file="$(mktemp)"
  # shellcheck disable=SC2064
  trap "rm -f '$notes_file'" EXIT

  echo "$notes" > "$notes_file"

  local draft_flag="--draft=false"
  if [[ "$draft" == "true" ]]; then
    draft_flag="--draft"
  fi

  log "Creating GitHub Release for tag $version (draft=$draft)"

  gh release create "$version" \
    --title "$version" \
    --notes-file "$notes_file" \
    "$draft_flag"

  log "GitHub Release $version created successfully"
}

simulate_github_release() {
  local version="$1"
  local notes="$2"
  local draft="$3"

  local draft_label="published"
  if [[ "$draft" == "true" ]]; then
    draft_label="draft"
  fi

  echo ""
  echo "═══════════════════════════════════════════════════════════"
  echo "  DRY RUN — the following would be executed:"
  echo "═══════════════════════════════════════════════════════════"
  echo ""
  echo "  gh release create \"$version\" \\"
  echo "    --title \"$version\" \\"
  echo "    --notes-file <temp-file> \\"
  echo "    --draft=$draft"
  echo ""
  echo "  Status:        $draft_label"
  echo "  Tag:           $version"
  echo "  Release notes: ${#notes} chars"
  echo ""
  echo "--- Release notes that would be published ---"
  echo "$notes"
  echo "--- End of release notes ---"
  echo ""
  echo "═══════════════════════════════════════════════════════════"
  echo "  Run without --dry-run to execute."
  echo "═══════════════════════════════════════════════════════════"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

main() {
  parse_arguments "$@"
  require_vars RELEASE_VERSION

  local changelog_file="CHANGELOG.md"

  if [[ ! -f "$changelog_file" ]]; then
    fail "CHANGELOG.md not found. Cannot create GitHub Release without release notes."
  fi

  log "Extracting release notes for version $RELEASE_VERSION from $changelog_file"

  local version_escaped
  version_escaped="$(escape_version_for_regex "$RELEASE_VERSION")"

  local release_notes
  release_notes="$(extract_release_notes "$version_escaped" "$changelog_file")"

  if [[ -z "${release_notes// /}" ]]; then
    fail "Could not find release notes for version $RELEASE_VERSION in $changelog_file"
  fi

  log "Release notes extracted (${#release_notes} chars)"

  # ACT simulation — same outcome as --dry-run
  if [[ "${ACT:-}" == "true" ]]; then
    log "Local act simulation detected."
    simulate_github_release "$RELEASE_VERSION" "$release_notes" "$DRAFT"
    exit 0
  fi

  # Local dry-run — preview without side effects
  if [[ "$DRY_RUN" == "true" ]]; then
    simulate_github_release "$RELEASE_VERSION" "$release_notes" "$DRAFT"
    exit 0
  fi

  if ! command -v gh &> /dev/null; then
    fail "GitHub CLI (gh) is not available. Cannot create GitHub Release."
  fi

  create_github_release "$RELEASE_VERSION" "$release_notes" "$DRAFT"
}

main "$@"
