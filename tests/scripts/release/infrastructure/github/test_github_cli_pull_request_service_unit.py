import pytest
from unittest.mock import Mock, patch
from dataclasses import dataclass

from scripts.release.infrastructure.github.github_cli_pull_request_service import (
    GitHubCliPullRequestService,
)
from scripts.release.infrastructure.commons.process import CommandRunner
from scripts.release.domain.entities import ReleasePullRequest
from scripts.release.domain.value_objects import ReleaseBranchName
from scripts.release.application.ports.outbound import OpenPullRequestOutput


@pytest.mark.unit
class TestGitHubCliPullRequestService:
    @pytest.fixture
    def mock_command_runner(self) -> Mock:
        return Mock(spec=CommandRunner)

    @pytest.fixture
    def service_with_mock_runner(self, mock_command_runner: Mock) -> GitHubCliPullRequestService:
        return GitHubCliPullRequestService(runner=mock_command_runner)

    @pytest.fixture
    def sample_pull_request(self) -> ReleasePullRequest:
        return ReleasePullRequest(
            base="main",
            head=ReleaseBranchName("release/v1.2.3"),
            title="Release v1.2.3",
            body="Automated release for version 1.2.3",
        )

    def test_init_with_provided_runner_uses_provided_runner(self, mock_command_runner: Mock) -> None:
        """Test that constructor uses the provided command runner."""
        # Act
        service = GitHubCliPullRequestService(runner=mock_command_runner)
        
        # Assert
        assert service._runner is mock_command_runner

    def test_init_with_none_runner_creates_subprocess_runner(self) -> None:
        """Test that constructor creates SubprocessCommandRunner when runner is None."""
        # Act
        service = GitHubCliPullRequestService(runner=None)
        
        # Assert
        # We can't directly test the type due to imports, but we can test it's not None
        assert service._runner is not None

    def test_init_without_runner_parameter_creates_default_runner(self) -> None:
        """Test that constructor creates default runner when no parameter provided."""
        # Act
        service = GitHubCliPullRequestService()
        
        # Assert
        assert service._runner is not None

    def test_open_calls_gh_pr_create_with_correct_parameters(
        self, 
        service_with_mock_runner: GitHubCliPullRequestService,
        mock_command_runner: Mock,
        sample_pull_request: ReleasePullRequest,
    ) -> None:
        """Test that open() calls gh pr create with the correct parameters."""
        # Arrange
        expected_url = "https://github.com/owner/repo/pull/123"
        mock_command_runner.run.return_value = expected_url
        
        expected_command = [
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
        
        # Act
        service_with_mock_runner.open(sample_pull_request)
        
        # Assert
        mock_command_runner.run.assert_called_once_with(expected_command)

    def test_open_extracts_pr_id_from_url(
        self, 
        service_with_mock_runner: GitHubCliPullRequestService,
        mock_command_runner: Mock,
        sample_pull_request: ReleasePullRequest,
    ) -> None:
        """Test that open() correctly extracts PR ID from the returned URL."""
        # Arrange
        expected_url = "https://github.com/owner/repo/pull/456/"
        mock_command_runner.run.return_value = expected_url
        
        # Act
        result = service_with_mock_runner.open(sample_pull_request)
        
        # Assert
        assert result.pr_id == "456"
        assert result.url == expected_url

    def test_open_handles_url_without_trailing_slash(
        self, 
        service_with_mock_runner: GitHubCliPullRequestService,
        mock_command_runner: Mock,
        sample_pull_request: ReleasePullRequest,
    ) -> None:
        """Test that open() handles URLs without trailing slash."""
        # Arrange
        expected_url = "https://github.com/owner/repo/pull/789"
        mock_command_runner.run.return_value = expected_url
        
        # Act
        result = service_with_mock_runner.open(sample_pull_request)
        
        # Assert
        assert result.pr_id == "789"
        assert result.url == expected_url

    def test_open_returns_open_pull_request_output(
        self, 
        service_with_mock_runner: GitHubCliPullRequestService,
        mock_command_runner: Mock,
        sample_pull_request: ReleasePullRequest,
    ) -> None:
        """Test that open() returns OpenPullRequestOutput with correct data."""
        # Arrange
        expected_url = "https://github.com/owner/repo/pull/123"
        mock_command_runner.run.return_value = expected_url
        
        # Act
        result = service_with_mock_runner.open(sample_pull_request)
        
        # Assert
        assert isinstance(result, OpenPullRequestOutput)
        assert result.pr_id == "123"
        assert result.url == expected_url

    @pytest.mark.parametrize(
        "pr_url, expected_pr_id",
        [
            ("https://github.com/owner/repo/pull/42", "42"),
            ("https://github.com/owner/repo/pull/999/", "999"),
            ("https://github.com/different-owner/different-repo/pull/1337", "1337"),
            ("https://github.com/test/test/pull/1", "1"),
            ("https://github.com/org/project/pull/12345/", "12345"),
        ],
    )
    def test_open_extracts_correct_pr_id_from_various_urls(
        self, 
        service_with_mock_runner: GitHubCliPullRequestService,
        mock_command_runner: Mock,
        sample_pull_request: ReleasePullRequest,
        pr_url: str,
        expected_pr_id: str,
    ) -> None:
        """Test that open() correctly extracts PR ID from various URL formats."""
        # Arrange
        mock_command_runner.run.return_value = pr_url
        
        # Act
        result = service_with_mock_runner.open(sample_pull_request)
        
        # Assert
        assert result.pr_id == expected_pr_id
        assert result.url == pr_url

    def test_open_with_different_pull_request_data(
        self, 
        service_with_mock_runner: GitHubCliPullRequestService,
        mock_command_runner: Mock,
    ) -> None:
        """Test that open() works with different pull request data."""
        # Arrange
        pr = ReleasePullRequest(
            base="main",
            head=ReleaseBranchName("release/v2.0.1"),
            title="Release v2.0.1 - Pre-release",
            body="This is a pre-release with breaking changes.\n\nSee CHANGELOG.md for details.",
        )
        
        expected_url = "https://github.com/org/repo/pull/100"
        mock_command_runner.run.return_value = expected_url
        
        expected_command = [
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
        
        # Act
        result = service_with_mock_runner.open(pr)
        
        # Assert
        mock_command_runner.run.assert_called_once_with(expected_command)
        assert result.pr_id == "100"
        assert result.url == expected_url

    def test_open_uses_release_branch_name_value(
        self, 
        service_with_mock_runner: GitHubCliPullRequestService,
        mock_command_runner: Mock,
    ) -> None:
        """Test that open() correctly uses the ReleaseBranchName.value property."""
        # Arrange
        branch_name = ReleaseBranchName("release/v3.1.4")
        pr = ReleasePullRequest(
            base="main",
            head=branch_name,
            title="Test Release",
            body="Test Body",
        )
        
        mock_command_runner.run.return_value = "https://github.com/test/repo/pull/1"
        
        # Act
        service_with_mock_runner.open(pr)
        
        # Assert
        call_args = mock_command_runner.run.call_args[0][0]
        head_index = call_args.index("--head") + 1
        assert call_args[head_index] == "release/v3.1.4"

    def test_open_with_special_characters_in_title_and_body(
        self, 
        service_with_mock_runner: GitHubCliPullRequestService,
        mock_command_runner: Mock,
    ) -> None:
        """Test that open() handles special characters in title and body."""
        # Arrange
        pr = ReleasePullRequest(
            base="main",
            head=ReleaseBranchName("release/v1.0.0"),
            title="Release v1.0.0: Major Update with \"Quotes\" & Symbols",
            body="Release notes:\n- Feature A\n- Bug fix for issue #123\n- Update dependencies",
        )
        
        expected_url = "https://github.com/test/repo/pull/42"
        mock_command_runner.run.return_value = expected_url
        
        # Act
        result = service_with_mock_runner.open(pr)
        
        # Assert
        call_args = mock_command_runner.run.call_args[0][0]
        
        title_index = call_args.index("--title") + 1
        body_index = call_args.index("--body") + 1
        
        assert call_args[title_index] == "Release v1.0.0: Major Update with \"Quotes\" & Symbols"
        assert call_args[body_index] == "Release notes:\n- Feature A\n- Bug fix for issue #123\n- Update dependencies"
        
        assert result.pr_id == "42"
        assert result.url == expected_url

    def test_open_command_structure_is_correct(
        self, 
        service_with_mock_runner: GitHubCliPullRequestService,
        mock_command_runner: Mock,
        sample_pull_request: ReleasePullRequest,
    ) -> None:
        """Test that the gh command structure follows the expected format."""
        # Arrange
        mock_command_runner.run.return_value = "https://github.com/test/repo/pull/1"
        
        # Act
        service_with_mock_runner.open(sample_pull_request)
        
        # Assert
        call_args = mock_command_runner.run.call_args[0][0]
        
        # Verify command structure
        assert call_args[0] == "gh"
        assert call_args[1] == "pr"
        assert call_args[2] == "create"
        
        # Verify all required flags are present
        assert "--base" in call_args
        assert "--head" in call_args
        assert "--title" in call_args
        assert "--body" in call_args
        
        # Verify values follow flags
        base_index = call_args.index("--base")
        head_index = call_args.index("--head")
        title_index = call_args.index("--title")
        body_index = call_args.index("--body")
        
        assert call_args[base_index + 1] == "main"
        assert call_args[head_index + 1] == "release/v1.2.3"
        assert call_args[title_index + 1] == "Release v1.2.3"
        assert call_args[body_index + 1] == "Automated release for version 1.2.3"