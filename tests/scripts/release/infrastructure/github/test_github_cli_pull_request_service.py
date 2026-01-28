from __future__ import annotations

import os
import random
from unittest.mock import Mock, patch

import pytest
from scripts.release.infrastructure.github.github_cli_pull_request_service import (
    GitHubCliPullRequestService,
)

from scripts.release.domain.entities import ReleasePullRequest
from scripts.release.domain.value_objects import ReleaseBranchName


@pytest.mark.integration
class TestGitHubCliPullRequestServiceIntegration:
    @pytest.mark.skipif(
        not os.environ.get("RUN_GITHUB_CLI_TESTS"),
        reason="Requires RUN_GITHUB_CLI_TESTS=1 and authenticated GitHub CLI",
    )
    @patch(
        "scripts.release.infrastructure.github.github_cli_pull_request_service.SubprocessCommandRunner"
    )
    def test_open_when_called_then_pull_request_created(
        self,
        mock_runner_class: Mock,
    ) -> None:
        # Arrange - Mock the subprocess runner to avoid actual GitHub API calls
        mock_runner = Mock()
        mock_runner_class.return_value = mock_runner
        mock_runner.run.return_value = (
            "https://github.com/forging-blocks-org/forging-blocks/pull/123"
        )

        patch_version = random.randint(1000, 9999)
        branch = ReleaseBranchName(f"release/v0.0.{patch_version}")

        service = GitHubCliPullRequestService()
        pull_request = ReleasePullRequest(
            base="main",
            head=branch,
            title="CLI Integration Test",
            body="Automated infrastructure test",
        )

        # Act
        output = service.open(pull_request)

        # Assert
        assert (
            output.url
            == "https://github.com/forging-blocks-org/forging-blocks/pull/123"
        )
        assert output.pr_id == "123"

        # Verify the correct command was called
        mock_runner.run.assert_called_once_with(
            [
                "gh",
                "pr",
                "create",
                "--base",
                "main",
                "--head",
                f"release/v0.0.{patch_version}",
                "--title",
                "CLI Integration Test",
                "--body",
                "Automated infrastructure test",
            ]
        )
