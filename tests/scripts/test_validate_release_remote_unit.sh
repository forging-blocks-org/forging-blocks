#!/usr/bin/env bash
# Unit tests for validate_release_remote.sh with mocked GitHub API responses
# Usage: bash tests/scripts/test_validate_release_remote_unit.sh

set -uo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

total=0
passed=0
failed=0

SCRIPT="scripts/validate_release_remote.sh"

run_test() {
    local test_name="$1"
    local json_data="$2"
    local expected_pattern="$3"

    local temp_dir
    temp_dir=$(mktemp -d)
    local json_file="$temp_dir/gh_output.json"
    local gh_mock="$temp_dir/gh"

    printf '%s' "$json_data" > "$json_file"

    cat > "$gh_mock" << MOCK
#!/usr/bin/env bash
cat "$json_file"
exit 0
MOCK
    chmod +x "$gh_mock"

    local output
    output=$(PATH="$temp_dir:$PATH" bash "$SCRIPT" 2>&1 || true)

    rm -rf "$temp_dir"

    # Strip ANSI color codes before checking
    local clean_output
    clean_output=$(echo "$output" | sed 's/\x1b\[[0-9;]*m//g')

    if echo "$clean_output" | grep -qE "$expected_pattern"; then
        echo -e "${GREEN}✓${NC} $test_name"
        ((passed++))
    else
        echo -e "${RED}✗${NC} $test_name"
        echo "  Expected pattern: $expected_pattern"
        echo "  Output:"
        echo "$clean_output" | head -15
        ((failed++))
    fi
    ((total++))
}

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ Unit Tests: validate_release_remote.sh                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo -e "${YELLOW}[1/4] Successful Release Workflow${NC}"
echo ""

json_success='[
  {"number": 100, "name": "Release Pipeline", "status": "completed", "conclusion": "success", "workflowName": "Release Pipeline", "headBranch": "release/v1.0.0", "createdAt": "2026-01-01T00:00:00Z", "event": "pull_request"},
  {"number": 99, "name": "CI", "status": "completed", "conclusion": "success", "workflowName": "CI", "headBranch": "release/v1.0.0", "createdAt": "2026-01-01T00:00:00Z", "event": "pull_request"}
]'

run_test "Detects successful release workflow" "$json_success" "Release validation passed"

echo ""
echo -e "${YELLOW}[2/4] Failed Release Workflow${NC}"
echo ""

json_failure='[
  {"number": 100, "name": "Release Pipeline", "status": "completed", "conclusion": "failure", "workflowName": "Release Pipeline", "headBranch": "release/v1.0.0", "createdAt": "2026-01-01T00:00:00Z", "event": "pull_request"}
]'

run_test "Detects failed release workflow" "$json_failure" "Release.*failed"

echo ""
echo -e "${YELLOW}[3/4] Skipped Release Workflow${NC}"
echo ""

json_skipped='[
  {"number": 100, "name": "Release Pipeline", "status": "completed", "conclusion": "skipped", "workflowName": "Release Pipeline", "headBranch": "release/v1.0.0", "createdAt": "2026-01-01T00:00:00Z", "event": "pull_request"},
  {"number": 99, "name": "CI", "status": "completed", "conclusion": "success", "workflowName": "CI", "headBranch": "release/v1.0.0", "createdAt": "2026-01-01T00:00:00Z", "event": "pull_request"}
]'

run_test "Detects skipped release workflow" "$json_skipped" "skipped"

echo ""
echo -e "${YELLOW}[4/4] No Release Workflow Found${NC}"
echo ""

json_none='[
  {"number": 99, "name": "CI", "status": "completed", "conclusion": "success", "workflowName": "CI", "headBranch": "main", "createdAt": "2026-01-01T00:00:00Z", "event": "push"}
]'

run_test "Handles missing release workflow" "$json_none" "No Release Pipeline"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ Test Summary                                               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Total:  $total"
echo -e "Passed: ${GREEN}$passed${NC}"
echo -e "Failed: ${RED}$failed${NC}"
echo ""

if [[ $failed -eq 0 ]]; then
    echo -e "${GREEN}✓ All unit tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ $failed test(s) failed${NC}"
    exit 1
fi
