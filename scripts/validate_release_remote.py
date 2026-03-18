#!/usr/bin/env python3
"""Validate that the release workflow passed on the remote CI/CD."""

import json
import subprocess
import sys


def main() -> int:
    result = subprocess.run(
        [
            "gh",
            "run",
            "list",
            "--event",
            "pull_request",
            "--limit",
            "20",
            "--json",
            "name,status,conclusion,workflowName,headBranch",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"ERROR: Failed to fetch workflow runs: {result.stderr}")
        return 1

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON: {e}")
        return 1

    release_workflow_run = None
    for run in data:
        workflow_name = run.get("workflowName", "")
        if "release pipeline" in workflow_name.lower():
            if run.get("status") == "completed" and run.get("conclusion") != "skipped":
                release_workflow_run = run
                break

    if not release_workflow_run:
        print("ERROR: No release workflow run found")
        return 1

    status = release_workflow_run.get("status", "")
    conclusion = release_workflow_run.get("conclusion", "")
    head_branch = release_workflow_run.get("headBranch", "")

    if status == "completed":
        if conclusion == "success":
            print(f"OK: Release workflow passed (branch: {head_branch}, conclusion: {conclusion})")
            return 0
        else:
            print(
                f"ERROR: Release workflow failed (branch: {head_branch}, conclusion: {conclusion})"
            )
            return 1
    else:
        print(f"ERROR: Release workflow not completed yet (status: {status})")
        return 1


if __name__ == "__main__":
    sys.exit(main())
