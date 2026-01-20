from __future__ import annotations

import uuid

from release.domain.value_objects.pull_request_base import PullRequestBase
from release.domain.value_objects.pull_request_head import PullRequestHead
from scripts.release.infrastructure.github.github_cli_pull_request_service import (
    GitHubCliPullRequestService,
)
from scripts.release.application.ports.outbound import (
    OpenPullRequestInput,
)
from scripts.release.domain.value_objects import (
    ReleaseBranchName,
    PullRequestTitle,
    PullRequestBody,
)



class TestGitHubCliPullRequestServiceIntegration:
    def test_open_when_called_then_pull_request_created(
        self,
        require_gh_auth: None,
    ) -> None:
        # Arrange
        branch = f"test-pr-{uuid.uuid4().hex[:8]}"

        service = GitHubCliPullRequestService()
        input = OpenPullRequestInput(
            base=PullRequestBase("main"),
            head=PullRequestHead(ReleaseBranchName(branch)),
            title=PullRequestTitle("CLI Integration Test"),
            body=PullRequestBody("Automated infrastructure test"),
        )

        # Act
        output = service.open(input)

        # Assert
        assert output.url
        assert output.pr_id
        assert output.url.startswith("https://")
