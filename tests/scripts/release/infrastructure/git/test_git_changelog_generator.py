from __future__ import annotations

from typing import Protocol
from unittest.mock import MagicMock, call, create_autospec

import pytest
from scripts.release.application.errors.change_log_generation_error import (
    ChangelogGenerationError,
)
from scripts.release.infrastructure.commons.process import CommandRunner
from scripts.release.infrastructure.git.git_changelog_generator import (
    ChangelogRequest,
    GitChangelogGenerator,
)

from tests.fixtures.git_test_repository import GitTestRepository


@pytest.mark.unit
class TestGitChangelogGenerator:
    @pytest.fixture
    def command_runner_mock(self) -> MagicMock:
        return create_autospec(CommandRunner, instance=True)

    @pytest.fixture
    def generator(self, command_runner_mock: MagicMock) -> GitChangelogGenerator:
        return GitChangelogGenerator(command_runner_mock)

    @pytest.fixture
    def changelog_request(self) -> ChangelogRequest:
        return ChangelogRequest(from_version="1.0.0")

    def test_init_when_called_with_runner_then_sets_runner(
        self, command_runner_mock: MagicMock
    ) -> None:
        generator = GitChangelogGenerator(command_runner_mock)

        assert generator._runner == command_runner_mock

    def test_init_when_called_without_runner_then_uses_default(self) -> None:
        generator = GitChangelogGenerator()

        assert generator._runner is not None

    async def test_generate_when_successful_then_returns_parsed_entries(
        self,
        generator: GitChangelogGenerator,
        command_runner_mock: MagicMock,
        changelog_request: ChangelogRequest,
    ) -> None:
        mock_output = "- feat: new feature (abc123)\n- fix: bug fix (def456)\n\n"

        # Configure mock to handle both the tag check and the git log command
        command_runner_mock.run.side_effect = [
            "v1.0.0",  # Response to git rev-parse --verify v1.0.0 (tag exists)
            mock_output,  # Response to git log command
        ]

        result = await generator.generate(changelog_request)

        # Verify both calls were made
        expected_calls = [
            call(["git", "rev-parse", "--verify", "v1.0.0"], suppress_error_log=True),
            call(
                ["git", "log", "v1.0.0..HEAD", "--pretty=format:- %s (%h)"], check=True
            ),
        ]
        command_runner_mock.run.assert_has_calls(expected_calls)

        # Verify the parsed results
        assert len(result.entries) == 2
        assert "- feat: new feature (abc123)" in result.entries
        assert "- fix: bug fix (def456)" in result.entries

    async def test_generate_when_git_command_fails_then_raises_changelog_generation_error(
        self,
        generator: GitChangelogGenerator,
        command_runner_mock: MagicMock,
        changelog_request: ChangelogRequest,
    ) -> None:
        # Configure mock so tag check succeeds but git log fails
        git_log_error = RuntimeError("Failed to generate changelog: No such tag")
        command_runner_mock.run.side_effect = [
            "v1.0.0",  # Response to git rev-parse (tag exists)
            git_log_error,  # git log command fails
        ]

        with pytest.raises(ChangelogGenerationError) as exc_info:
            await generator.generate(changelog_request)

        assert "Failed to generate changelog" in str(exc_info.value)
        assert exc_info.value.__cause__ == git_log_error

    def test_parse_git_output_when_valid_output_then_returns_non_empty_lines(
        self, generator: GitChangelogGenerator
    ) -> None:
        output = "- feat: new feature (abc123)\n\n- fix: bug fix (def456)\n   \n"

        result = generator._parse_git_output(output)

        assert result == ["- feat: new feature (abc123)", "- fix: bug fix (def456)"]

    def test_parse_git_output_when_empty_output_then_returns_empty_list(
        self, generator: GitChangelogGenerator
    ) -> None:
        output = "\n\n   \n"

        result = generator._parse_git_output(output)

        assert result == []

    def test_parse_git_output_when_single_line_then_returns_single_entry(
        self, generator: GitChangelogGenerator
    ) -> None:
        output = "- feat: new feature (abc123)"

        result = generator._parse_git_output(output)

        assert result == ["- feat: new feature (abc123)"]

    async def test_generate_when_no_tags_exist_then_uses_head_range(
        self,
        generator: GitChangelogGenerator,
        command_runner_mock: MagicMock,
        changelog_request: ChangelogRequest,
    ) -> None:
        mock_output = "- feat: initial commit (abc123)\n"

        # Configure mock: both tag checks fail (requested tag and latest tag)
        command_runner_mock.run.side_effect = [
            RuntimeError("Tag doesn't exist"),  # git rev-parse --verify fails
            RuntimeError("No tags exist"),  # git describe --tags fails
            mock_output,  # git log HEAD succeeds
        ]

        result = await generator.generate(changelog_request)

        # Verify all calls were made correctly
        expected_calls = [
            call(["git", "rev-parse", "--verify", "v1.0.0"], suppress_error_log=True),
            call(["git", "describe", "--tags", "--abbrev=0"], suppress_error_log=True),
            call(["git", "log", "HEAD", "--pretty=format:- %s (%h)"], check=True),
        ]
        command_runner_mock.run.assert_has_calls(expected_calls)

        assert len(result.entries) == 1
        assert "- feat: initial commit (abc123)" in result.entries

    async def test_generate_when_requested_tag_missing_but_latest_exists_then_uses_latest(
        self,
        generator: GitChangelogGenerator,
        command_runner_mock: MagicMock,
        changelog_request: ChangelogRequest,
    ) -> None:
        mock_output = "- feat: new feature (abc123)\n"

        # Configure mock: requested tag fails but latest tag succeeds
        command_runner_mock.run.side_effect = [
            RuntimeError(
                "Requested tag doesn't exist"
            ),  # git rev-parse --verify v1.0.0 fails
            "v0.5.0",  # git describe --tags succeeds
            mock_output,  # git log with latest tag succeeds
        ]

        result = await generator.generate(changelog_request)

        # Verify the fallback to latest tag
        expected_calls = [
            call(["git", "rev-parse", "--verify", "v1.0.0"], suppress_error_log=True),
            call(["git", "describe", "--tags", "--abbrev=0"], suppress_error_log=True),
            call(
                ["git", "log", "v0.5.0..HEAD", "--pretty=format:- %s (%h)"], check=True
            ),
        ]
        command_runner_mock.run.assert_has_calls(expected_calls)

        assert len(result.entries) == 1
        assert "- feat: new feature (abc123)" in result.entries

    async def test_find_suitable_from_tag_when_requested_tag_exists_then_returns_requested(
        self,
        generator: GitChangelogGenerator,
        command_runner_mock: MagicMock,
    ) -> None:
        # Configure mock: requested tag exists
        command_runner_mock.run.return_value = ""

        result = await generator._find_suitable_from_tag("1.0.0")

        assert result == "v1.0.0"
        command_runner_mock.run.assert_called_once_with(
            ["git", "rev-parse", "--verify", "v1.0.0"], suppress_error_log=True
        )

    async def test_find_suitable_from_tag_when_requested_missing_but_latest_exists_then_returns_latest(  # noqa: E501
        self,
        generator: GitChangelogGenerator,
        command_runner_mock: MagicMock,
    ) -> None:
        # Configure mock: requested fails, latest succeeds
        command_runner_mock.run.side_effect = [
            RuntimeError("Tag doesn't exist"),
            "v0.5.0   ",  # with whitespace to test .strip()
        ]

        result = await generator._find_suitable_from_tag("1.0.0")

        assert result == "v0.5.0"
        expected_calls = [
            call(["git", "rev-parse", "--verify", "v1.0.0"], suppress_error_log=True),
            call(["git", "describe", "--tags", "--abbrev=0"], suppress_error_log=True),
        ]
        command_runner_mock.run.assert_has_calls(expected_calls)

    async def test_find_suitable_from_tag_when_no_tags_exist_then_returns_none(
        self,
        generator: GitChangelogGenerator,
        command_runner_mock: MagicMock,
    ) -> None:
        # Configure mock: both calls fail
        command_runner_mock.run.side_effect = [
            RuntimeError("Requested tag doesn't exist"),
            RuntimeError("No tags exist"),
        ]

        result = await generator._find_suitable_from_tag("1.0.0")

        assert result is None
        expected_calls = [
            call(["git", "rev-parse", "--verify", "v1.0.0"], suppress_error_log=True),
            call(["git", "describe", "--tags", "--abbrev=0"], suppress_error_log=True),
        ]
        command_runner_mock.run.assert_has_calls(expected_calls)


class GitRepository(Protocol):
    def write_file(self, name: str, content: str) -> None: ...

    def commit(self, message: str) -> None: ...

    def last_commit_message(self) -> str: ...


@pytest.mark.integration
class TestGitChangelogGeneratorIntegration:
    async def test_generate_when_commits_exist_then_entries_returned(
        self,
        git_repo: GitTestRepository,
    ) -> None:
        # Arrange
        # Create an initial tag
        git_repo.create_tag("v0.0.0")

        git_repo.write_file("file.txt", "x")
        git_repo.commit("feat: new feature")

        generator = GitChangelogGenerator(git_repo.scoped_runner())
        request = ChangelogRequest(from_version="0.0.0")

        # Act
        response = await generator.generate(request)

        # Assert
        assert any("feat: new feature" in entry for entry in response.entries)
