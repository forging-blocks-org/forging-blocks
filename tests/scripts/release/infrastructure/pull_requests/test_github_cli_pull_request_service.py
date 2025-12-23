from unittest.mock import patch

from scripts.release.application.ports.outbound import OpenPullRequestInput
from scripts.release.infrastructure.pull_requests.github_cli_pull_request_service import (
    GitHubCliPullRequestService,
)
from scripts.release.domain.value_objects import (
    PullRequestBase,
    PullRequestHead,
    PullRequestTitle,
    PullRequestBody,
    ReleaseBranchName,
    ReleaseVersion,
)


class TestGitHubCliPullRequestService:
    @patch(
        "scripts.release.infrastructure.pull_requests.github_cli_pull_request_service.run"
    )
    def test_create_when_dry_run_then_no_command_executed(
        self,
        run_mock,
    ) -> None:
        input = OpenPullRequestInput(
            base=PullRequestBase("main"),
            head=PullRequestHead(
                ReleaseBranchName.from_version(ReleaseVersion(1, 2, 3))
            ),
            title=PullRequestTitle("Release v1.2.3"),
            body=PullRequestBody("Notes"),
            dry_run=True,
        )

        service = GitHubCliPullRequestService()

        output = service.create(input)

        assert output.pr_id is None
        assert output.url is None
        run_mock.assert_not_called()

    @patch(
        "scripts.release.infrastructure.pull_requests.github_cli_pull_request_service.run"
    )
    def test_create_when_valid_then_returns_pr_id_and_url(
        self,
        run_mock,
    ) -> None:
        run_mock.return_value = "https://github.com/org/repo/pull/42"

        input = OpenPullRequestInput(
            base=PullRequestBase("main"),
            head=PullRequestHead(ReleaseBranchName("release/v1.2.3")),
            title=PullRequestTitle("Release v1.2.3"),
            body=PullRequestBody("Notes"),
            dry_run=False,
        )
        service = GitHubCliPullRequestService()

        output = service.create(input)

        assert output.pr_id == "42"
        assert output.url
        assert output.url.endswith("/42")
