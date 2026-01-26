from __future__ import annotations

import uuid

from scripts.release.infrastructure.github.github_cli_pull_request_service import (
    GitHubCliPullRequestService,
)
from scripts.release.domain.entities import ReleasePullRequest
from scripts.release.domain.value_objects import ReleaseBranchName


class TestGitHubCliPullRequestServiceIntegration:
    def test_open_when_called_then_pull_request_created(
        self,
        require_gh_auth: None,
    ) -> None:
        # Arrange
        branch = ReleaseBranchName(f"release/v0.0.{uuid.uuid4().hex[:8]}")

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
        assert output.url
        assert output.pr_id
        assert output.url.startswith("https://")
