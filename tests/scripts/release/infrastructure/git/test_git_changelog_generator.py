from __future__ import annotations

import pytest
import subprocess
from typing import Protocol
from unittest.mock import MagicMock, create_autospec

from scripts.release.infrastructure.git.git_changelog_generator import (
    GitChangelogGenerator, ChangelogRequest
)
from scripts.release.infrastructure.commons.process import CommandRunner
from scripts.release.application.errors.change_log_generation_error import ChangelogGenerationError


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

    def test_init_when_called_with_runner_then_sets_runner(self, command_runner_mock: MagicMock) -> None:
        generator = GitChangelogGenerator(command_runner_mock)
        
        assert generator._runner == command_runner_mock

    def test_init_when_called_without_runner_then_uses_default(self) -> None:
        generator = GitChangelogGenerator()
        
        assert generator._runner is not None

    async def test_generate_when_successful_then_returns_parsed_entries(
        self, generator: GitChangelogGenerator, command_runner_mock: MagicMock, changelog_request: ChangelogRequest
    ) -> None:
        mock_result = MagicMock()
        mock_result.stdout = "- feat: new feature (abc123)\n- fix: bug fix (def456)\n\n"
        command_runner_mock.run.return_value = mock_result
        
        result = await generator.generate(changelog_request)
        
        expected_command = [
            "git", "log", "v1.0.0..HEAD", "--pretty=format:- %s (%h)"
        ]
        command_runner_mock.run.assert_called_once_with(expected_command, check=True)
        assert len(result.entries) == 2
        assert "- feat: new feature (abc123)" in result.entries
        assert "- fix: bug fix (def456)" in result.entries

    async def test_generate_when_git_command_fails_then_raises_changelog_generation_error(
        self, generator: GitChangelogGenerator, command_runner_mock: MagicMock, changelog_request: ChangelogRequest
    ) -> None:
        error = subprocess.CalledProcessError(1, "git", stderr="No such tag")
        command_runner_mock.run.side_effect = error
        
        with pytest.raises(ChangelogGenerationError) as exc_info:
            await generator.generate(changelog_request)
        
        assert "Failed to generate changelog: No such tag" in str(exc_info.value)
        assert exc_info.value.__cause__ == error

    def test_parse_git_output_when_valid_output_then_returns_non_empty_lines(self, generator: GitChangelogGenerator) -> None:
        output = "- feat: new feature (abc123)\n\n- fix: bug fix (def456)\n   \n"
        
        result = generator._parse_git_output(output)
        
        assert result == [
            "- feat: new feature (abc123)",
            "- fix: bug fix (def456)"
        ]

    def test_parse_git_output_when_empty_output_then_returns_empty_list(self, generator: GitChangelogGenerator) -> None:
        output = "\n\n   \n"
        
        result = generator._parse_git_output(output)
        
        assert result == []

    def test_parse_git_output_when_single_line_then_returns_single_entry(self, generator: GitChangelogGenerator) -> None:
        output = "- feat: new feature (abc123)"
        
        result = generator._parse_git_output(output)
        
        assert result == ["- feat: new feature (abc123)"]


class GitRepository(Protocol):
    def write_file(self, name: str, content: str) -> None:
        ...

    def  commit(self, message: str) -> None:
        ...

    def last_commit_message(self) -> str:
        ...


class TestGitChangelogGeneratorIntegration:
    async def test_generate_when_commits_exist_then_entries_returned(
        self,
        git_repo: GitRepository,
    ) -> None:
        # Arrange
        git_repo.write_file("file.txt", "x")
        git_repo.commit("feat: new feature")

        generator = GitChangelogGenerator()
        request = ChangelogRequest(from_version="0.0.0")

        # Act
        response = await generator.generate(request)

        # Assert
        assert any("feat: new feature" in entry for entry in response.entries)
