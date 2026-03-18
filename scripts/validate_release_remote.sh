#!/usr/bin/env bash
# Validate that the release workflow and all required checks passed on the remote CI/CD.
# This ensures the DX for contributors is solid by verifying the complete release pipeline.

set -euo pipefail

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Fetch latest release branch
get_latest_release_branch() {
    # First, try to determine the latest local release branch.
    local branch
    branch=$(git for-each-ref --sort=-version:refname --format='%(refname:short)' refs/heads/release/ | head -1 || true)

    if [[ -n "${branch:-}" ]]; then
        echo "$branch"
        return 0
    fi

    # Fallback: derive the latest release branch from the newest "Release Pipeline" run.
    if command -v gh >/dev/null 2>&1; then
        local runs
        runs=$(fetch_workflow_runs 50)
        branch=$(echo "$runs" | jq -r '.[] | select(.workflowName == "Release Pipeline" and (.headBranch | startswith("release/"))) | .headBranch' | head -1)

        if [[ -n "${branch:-}" && "$branch" != "null" ]]; then
            echo "$branch"
            return 0
        fi
    fi

    # If no branch could be determined, return empty string to preserve existing behavior.
    echo ""
}

# Fetch workflow runs and return JSON
fetch_workflow_runs() {
    local limit="${1:-50}"
    local output

    if ! output=$(GH_PAGER=cat gh run list --limit "$limit" --json number,name,status,conclusion,workflowName,headBranch,createdAt,event 2>&1); then
        echo -e "${RED}ERROR: Failed to fetch workflow runs from GitHub CLI${NC}" >&2
        echo "$output" >&2
        return 1
    fi

    echo "$output"
}

# Find the most recent Release Pipeline run (from any release branch)
find_latest_release_pipeline_run() {
    local runs="$1"

    echo "$runs" | jq -r ".[] | select(.workflowName == \"Release Pipeline\" and (.headBranch | startswith(\"release/\"))) | @base64" | head -1
}

# Find Release Pipeline run for a specific branch
find_release_pipeline_run_for_branch() {
    local branch="$1"
    local runs="$2"

    echo "$runs" | jq -r ".[] | select(.workflowName == \"Release Pipeline\" and .headBranch == \"$branch\") | @base64" | head -1
}

# Find the most recent CI run for a given branch
find_ci_run() {
    local branch="$1"
    local runs="$2"

    echo "$runs" | jq -r ".[] | select(.workflowName == \"CI\" and .headBranch == \"$branch\") | @base64" | head -1
}

# Check if a workflow run passed
validate_workflow_run() {
    local run_b64="$1"
    local workflow_type="$2"

    if [[ -z "$run_b64" ]]; then
        echo -e "${RED}✗${NC} No $workflow_type workflow run found"
        return 1
    fi

    local run
    run=$(echo "$run_b64" | base64 -d)

    local status
    local conclusion
    local number
    local head_branch

    status=$(echo "$run" | jq -r '.status')
    conclusion=$(echo "$run" | jq -r '.conclusion')
    number=$(echo "$run" | jq -r '.number')
    head_branch=$(echo "$run" | jq -r '.headBranch')

    if [[ "$status" != "completed" ]]; then
        echo -e "${YELLOW}◐${NC} $workflow_type workflow still running (status: $status, #$number, branch: $head_branch)"
        return 1
    fi

    if [[ "$conclusion" == "skipped" ]]; then
        echo -e "${YELLOW}◐${NC} $workflow_type workflow was skipped (#$number, branch: $head_branch)"
        return 0
    fi

    if [[ "$conclusion" == "success" ]]; then
        echo -e "${GREEN}✓${NC} $workflow_type workflow passed (#$number, branch: $head_branch)"
        return 0
    fi

    echo -e "${RED}✗${NC} $workflow_type workflow failed (conclusion: $conclusion, #$number, branch: $head_branch)"
    return 1
}

# Extract run details for logging
extract_run_details() {
    local run_b64="$1"
    echo "$run_b64" | base64 -d | jq -r '{number, status, conclusion, headBranch, createdAt, event}'
}

# Main validation logic
main() {
    echo "Validating remote CI/CD for latest release..."

    # Get the latest release branch
    local release_branch
    release_branch=$(get_latest_release_branch)

    if [[ -z "$release_branch" ]]; then
        echo -e "${RED}ERROR: No release branches found${NC}"
        return 1
    fi

    echo "Latest release branch: $release_branch"

    # Fetch workflow runs
    local runs
    runs=$(fetch_workflow_runs 50)

    if [[ -z "$runs" || "$runs" == "[]" ]]; then
        echo -e "${RED}ERROR: Failed to fetch workflow runs${NC}"
        return 1
    fi

    # Try to find Release Pipeline run for this specific branch
    local release_run
    release_run=$(find_release_pipeline_run_for_branch "$release_branch" "$runs")

    if [[ -z "$release_run" ]]; then
        echo -e "${RED}✗${NC} No Release Pipeline run found for $release_branch"
        echo -e "${YELLOW}ℹ${NC} The release branch must be merged into main to trigger the Release Pipeline"
        return 1
    fi

    if ! validate_workflow_run "$release_run" "Release Pipeline"; then
        if [[ -n "$release_run" ]]; then
            echo ""
            echo "Details:"
            extract_run_details "$release_run" | jq .
        fi
        return 1
    fi

    # Validate CI workflow on the release branch
    echo ""
    echo "Validating CI workflow for $release_branch..."
    local ci_run
    ci_run=$(find_ci_run "$release_branch" "$runs")

    if ! validate_workflow_run "$ci_run" "CI"; then
        if [[ -n "$ci_run" ]]; then
            echo ""
            echo "Details:"
            extract_run_details "$ci_run" | jq .
        fi
        return 1
    fi

    echo ""
    echo -e "${GREEN}✓ Release validation passed${NC}"
    return 0
}

main "$@"
