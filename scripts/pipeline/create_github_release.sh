#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/pipeline/commons.sh
source "$SCRIPT_DIR/commons.sh"

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

validate_environment() {
  require_vars RELEASE_VERSION
  assert_changelog_exists
}

assert_changelog_exists() {
  if [[ ! -f "CHANGELOG.md" ]]; then
    fail "CHANGELOG.md not found. Cannot create GitHub Release without release notes."
  fi
}

assert_github_cli_available() {
  if ! command -v gh &> /dev/null; then
    fail "GitHub CLI (gh) is not available. Cannot create GitHub Release."
  fi
}

is_act_simulation() {
  [[ "${ACT:-}" == "true" ]]
}

is_dry_run() {
  [[ "$DRY_RUN" == "true" ]]
}

should_simulate() {
  is_act_simulation || is_dry_run
}

strip_v_prefix() {
  local version="$1"
  echo "${version#v}"
}

resolve_changelog_version() {
  local full_version="$1"
  strip_v_prefix "$full_version"
}

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

assert_release_notes_not_empty() {
  local notes="$1"
  if [[ -z "${notes// /}" ]]; then
    fail "Could not find release notes for version $RELEASE_VERSION in CHANGELOG.md"
  fi
}

collect_release_notes() {
  local changelog_version="$1"
  local changelog_file="CHANGELOG.md"

  log "Extracting release notes for version $RELEASE_VERSION from $changelog_file" >&2

  local version_escaped
  version_escaped="$(escape_version_for_regex "$changelog_version")"

  local notes
  notes="$(extract_release_notes "$version_escaped" "$changelog_file")"

  assert_release_notes_not_empty "$notes"

  log "Release notes extracted (${#notes} chars)" >&2

  echo "$notes"
}

resolve_draft_flag() {
  if [[ "$DRAFT" == "true" ]]; then
    echo "--draft"
  fi
}

simulate_github_release() {
  local version="$1"
  local notes="$2"

  local draft_label
  local draft_flag
  draft_flag="$(resolve_draft_flag)"
  if [[ "$DRAFT" == "true" ]]; then
    draft_label="draft"
  else
    draft_label="published"
  fi

  echo ""
  echo "═══════════════════════════════════════════════════════════"
  echo "  DRY RUN — the following would be executed:"
  echo "═══════════════════════════════════════════════════════════"
  echo ""
  echo "  gh release create \"$version\" \\"
  echo "    --title \"$version\" \\"
  echo "    --notes-file <temp-file> \\"
  echo "    $draft_flag"
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

create_github_release() {
  local version="$1"
  local notes="$2"

  local notes_file
  notes_file="$(mktemp)"
  # shellcheck disable=SC2064
  trap "rm -f '$notes_file'" EXIT

  echo "$notes" > "$notes_file"

  local draft_flag
  draft_flag="$(resolve_draft_flag)"
  local extra_args=()
  if [[ -n "$draft_flag" ]]; then
    extra_args+=("$draft_flag")
  fi

  log "Creating GitHub Release for tag $version (draft=$DRAFT)"

  gh release create "$version" \
    --title "$version" \
    --notes-file "$notes_file" \
    "${extra_args[@]}"

  log "GitHub Release $version created successfully"
}

handle_release() {
  local version="$1"
  local notes="$2"

  if should_simulate; then
    if is_act_simulation; then
      log "Local act simulation detected."
    fi
    simulate_github_release "$version" "$notes"
    return
  fi

  assert_github_cli_available
  create_github_release "$version" "$notes"
}

main() {
  parse_arguments "$@"
  validate_environment

  local changelog_version
  changelog_version="$(resolve_changelog_version "$RELEASE_VERSION")"

  local release_notes
  release_notes="$(collect_release_notes "$changelog_version")"

  handle_release "$RELEASE_VERSION" "$release_notes"
}

main "$@"
