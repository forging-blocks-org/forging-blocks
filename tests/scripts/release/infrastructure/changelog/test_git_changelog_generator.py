import pytest
from unittest.mock import MagicMock, create_autospec

from scripts.release.application.ports.outbound.changelog_generator import (
    ChangelogRequest,
)
from scripts.release.infrastructure.changelog.git_changelog_generator import (
    GitChangelogGenerator,
)
from scripts.release.infrastructure.commons.process import CommandRunner


class TestGitChangelogGenerator:
    @pytest.fixture
    def runner_mock(self) -> MagicMock:
        """Fixture to mock the CommandRunner."""
        return create_autospec(spec=CommandRunner, instance=True)

    @pytest.mark.asyncio
    async def test_generate_when_git_returns_multiple_commits_then_entries_parsed_correctly(
        self, runner_mock: MagicMock
    ) -> None:
        # Arrange: Set up mock output of `git log`
        git_output = (
            "- Fix release bug (abc123)\n"
            "- Improve changelog formatting (def456)\n"
        )
        runner_mock.run.return_value = git_output
        generator = GitChangelogGenerator(runner_mock)
        request = ChangelogRequest(from_version="1.2.3", to_version="HEAD")

        # Act: Call the generator
        response = await generator.generate(request)

        # Assert: Verify generator behavior and output
        runner_mock.run.assert_called_once_with(
            [
                "git",
                "log",
                "v1.2.3..HEAD",
                "--pretty=format:- %s (%h)",
            ]
        )
        assert response.entries == [
            "- Fix release bug (abc123)",
            "- Improve changelog formatting (def456)",
        ]

    @pytest.mark.asyncio
    async def test_generate_when_git_returns_empty_output_then_entries_is_empty(
        self, runner_mock: MagicMock
    ) -> None:
        # Arrange: Empty git log output
        git_output = ""
        runner_mock.run.return_value = git_output
        generator = GitChangelogGenerator(runner_mock)
        request = ChangelogRequest(from_version="2.0.0", to_version="HEAD")

        # Act: Call the generator
        response = await generator.generate(request)

        # Assert: Ensure the changelog is empty
        assert response.entries == []

    @pytest.mark.asyncio
    async def test_generate_when_git_output_contains_blank_lines_then_blank_lines_ignored(
        self, runner_mock: MagicMock
    ) -> None:
        # Arrange: Git log output with blank lines
        git_output = "\n\n- Initial release (aaa111)\n\n"
        runner_mock.run.return_value = git_output
        generator = GitChangelogGenerator(runner_mock)
        request = ChangelogRequest(from_version="0.9.0", to_version="HEAD")

        # Act: Call the generator
        response = await generator.generate(request)

        # Assert: Blank lines are ignored
        assert response.entries == [
            "- Initial release (aaa111)",
        ]
