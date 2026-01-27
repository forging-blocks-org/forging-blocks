from __future__ import annotations

import pytest
import uuid

from scripts.release.infrastructure.github.github_cli_pull_request_service import (
    GitHubCliPullRequestService,
)
from scripts.release.domain.entities import ReleasePullRequest
from scripts.release.domain.value_objects import ReleaseBranchName


@pytest.mark.integration
class TestGitHubCliPullRequestServiceIntegration:
    @pytest.mark.skip(reason="Requires actual GitHub repo with branches - integration test for real environments only")
    def test_open_when_called_then_pull_request_created(
        self,
        require_gh_auth: None,
    ) -> None:
        # Arrange
        import random
        patch_version = random.randint(1000, 9999)  # Use numeric patch version
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
        assert output.url
        assert output.pr_id
        assert output.url.startswith("https://")
