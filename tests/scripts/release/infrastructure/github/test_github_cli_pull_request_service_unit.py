# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest
from scripts.release.application.ports.outbound import OpenPullRequestOutput
from scripts.release.infrastructure.github.github_cli_pull_request_service import (
    GitHubCliPullRequestService,
)

from scripts.release.domain.entities import ReleasePullRequest
from scripts.release.domain.value_objects import ReleaseBranchName
from tests.fixtures.fake_command_runner import FakeCommandRunner


@pytest.mark.unit
class TestGitHubCliPullRequestService:
    @pytest.fixture
    def runner(self) -> FakeCommandRunner:
        return FakeCommandRunner()

    @pytest.fixture
    def sample_pull_request(self) -> ReleasePullRequest:
        return ReleasePullRequest(
            base="main",
            head=ReleaseBranchName("release/v1.2.3"),
            title="Release v1.2.3",
            body="Automated release for version 1.2.3",
        )

    def test_init_with_provided_runner_uses_provided_runner(
        self, runner: FakeCommandRunner
    ) -> None:
        service = GitHubCliPullRequestService(runner=runner)
        assert service._runner is runner

    def test_init_with_none_runner_creates_subprocess_runner(self) -> None:
        service = GitHubCliPullRequestService(runner=None)
        assert service._runner is not None

    def test_init_without_runner_parameter_creates_default_runner(self) -> None:
        service = GitHubCliPullRequestService()
        assert service._runner is not None

    def test_open_calls_gh_pr_create_with_correct_parameters(
        self,
        runner: FakeCommandRunner,
        sample_pull_request: ReleasePullRequest,
    ) -> None:
        expected_url = "https://github.com/owner/repo/pull/123"
        runner.configured_outputs = [expected_url]

        expected_cmd = [
            "gh",
            "pr",
            "create",
            "--base",
            "main",
            "--head",
            "release/v1.2.3",
            "--title",
            "Release v1.2.3",
            "--body",
            "Automated release for version 1.2.3",
        ]

        service = GitHubCliPullRequestService(runner=runner)
        service.open(sample_pull_request)

        assert len(runner.calls) == 1
        assert runner.calls[0][0] == expected_cmd

    def test_open_extracts_pr_id_from_url(
        self,
        runner: FakeCommandRunner,
        sample_pull_request: ReleasePullRequest,
    ) -> None:
        expected_url = "https://github.com/owner/repo/pull/456/"
        runner.configured_outputs = [expected_url]

        service = GitHubCliPullRequestService(runner=runner)
        result = service.open(sample_pull_request)

        assert result.pr_id == "456"
        assert result.url == expected_url

    def test_open_handles_url_without_trailing_slash(
        self,
        runner: FakeCommandRunner,
        sample_pull_request: ReleasePullRequest,
    ) -> None:
        expected_url = "https://github.com/owner/repo/pull/789"
        runner.configured_outputs = [expected_url]

        service = GitHubCliPullRequestService(runner=runner)
        result = service.open(sample_pull_request)

        assert result.pr_id == "789"
        assert result.url == expected_url

    def test_open_returns_open_pull_request_output(
        self,
        runner: FakeCommandRunner,
        sample_pull_request: ReleasePullRequest,
    ) -> None:
        expected_url = "https://github.com/owner/repo/pull/1"
        runner.configured_outputs = [expected_url]

        service = GitHubCliPullRequestService(runner=runner)
        result = service.open(sample_pull_request)

        assert isinstance(result, OpenPullRequestOutput)
        assert result.pr_id == "1"
        assert result.url == expected_url

    def test_open_handles_alternative_url_format(
        self,
        runner: FakeCommandRunner,
        sample_pull_request: ReleasePullRequest,
    ) -> None:
        expected_url = "https://github.com/forging-blocks-org/forging-blocks/pull/42"
        runner.configured_outputs = [expected_url]

        service = GitHubCliPullRequestService(runner=runner)
        result = service.open(sample_pull_request)

        assert result.pr_id == "42"
        assert result.url == expected_url

    def test_open_with_different_pull_request_data(
        self,
        runner: FakeCommandRunner,
    ) -> None:
        pr = ReleasePullRequest(
            base="main",
            head=ReleaseBranchName("release/v2.0.1"),
            title="Release v2.0.1 - Pre-release",
            body="This is a pre-release with breaking changes.\n\nSee CHANGELOG.md for details.",
        )

        expected_url = "https://github.com/org/repo/pull/100"
        runner.configured_outputs = [expected_url]

        expected_cmd = [
            "gh",
            "pr",
            "create",
            "--base",
            "main",
            "--head",
            "release/v2.0.1",
            "--title",
            "Release v2.0.1 - Pre-release",
            "--body",
            "This is a pre-release with breaking changes.\n\nSee CHANGELOG.md for details.",
        ]

        service = GitHubCliPullRequestService(runner=runner)
        result = service.open(pr)

        assert len(runner.calls) == 1
        assert runner.calls[0][0] == expected_cmd
        assert result.pr_id == "100"
        assert result.url == expected_url

    def test_open_uses_release_branch_name_value(
        self,
        runner: FakeCommandRunner,
    ) -> None:
        branch_name = ReleaseBranchName("release/v3.1.4")
        pr = ReleasePullRequest(
            base="main",
            head=branch_name,
            title="Test Release",
            body="Test Body",
        )

        runner.configured_outputs = ["https://github.com/test/repo/pull/1"]

        service = GitHubCliPullRequestService(runner=runner)
        service.open(pr)

        call_args = runner.calls[0][0]
        head_index = call_args.index("--head") + 1
        assert call_args[head_index] == "release/v3.1.4"

    def test_open_with_special_characters_in_title_and_body(
        self,
        runner: FakeCommandRunner,
    ) -> None:
        pr = ReleasePullRequest(
            base="main",
            head=ReleaseBranchName("release/v1.0.0"),
            title='Release v1.0.0: Major Update with "Quotes" & Symbols',
            body="Release notes:\n- Feature A\n- Bug fix for issue #123\n- Update dependencies",
        )

        expected_url = "https://github.com/test/repo/pull/42"
        runner.configured_outputs = [expected_url]

        service = GitHubCliPullRequestService(runner=runner)
        result = service.open(pr)

        call_args = runner.calls[0][0]
        title_index = call_args.index("--title") + 1
        body_index = call_args.index("--body") + 1

        assert call_args[title_index] == 'Release v1.0.0: Major Update with "Quotes" & Symbols'
        assert call_args[body_index] == (
            "Release notes:\n- Feature A\n- Bug fix for issue #123\n- Update dependencies"
        )
        assert result.pr_id == "42"
        assert result.url == expected_url

    def test_open_command_structure_is_correct(
        self,
        runner: FakeCommandRunner,
        sample_pull_request: ReleasePullRequest,
    ) -> None:
        runner.configured_outputs = ["https://github.com/test/repo/pull/1"]

        service = GitHubCliPullRequestService(runner=runner)
        service.open(sample_pull_request)

        call_args = runner.calls[0][0]

        assert call_args[0] == "gh"
        assert call_args[1] == "pr"
        assert call_args[2] == "create"

        assert "--base" in call_args
        assert "--head" in call_args
        assert "--title" in call_args
        assert "--body" in call_args

        base_index = call_args.index("--base")
        head_index = call_args.index("--head")
        title_index = call_args.index("--title")
        body_index = call_args.index("--body")

        assert call_args[base_index + 1] == "main"
        assert call_args[head_index + 1] == "release/v1.2.3"
        assert call_args[title_index + 1] == "Release v1.2.3"
        assert call_args[body_index + 1] == "Automated release for version 1.2.3"
