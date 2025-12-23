import pytest
from unittest.mock import patch

from scripts.release.application.ports.outbound.changelog_generator import (
    ChangelogRequest,
)
from scripts.release.infrastructure.changelog.git_changelog_generator import (
    GitChangelogGenerator,
)


class TestGitChangelogGenerator:
    @pytest.mark.asyncio
    async def test_generate_when_git_returns_multiple_commits_then_entries_parsed_correctly(
        self,
    ) -> None:
        generator = GitChangelogGenerator()
        request = ChangelogRequest(from_version="1.2.3", to_version="HEAD")

        git_output = (
            "- Fix release bug (abc123)\n" "- Improve changelog formatting (def456)\n"
        )

        with patch(
            "scripts.release.infrastructure.changelog.git_changelog_generator.run",
            return_value=git_output,
        ) as run_mock:
            response = await generator.generate(request)

        run_mock.assert_called_once_with(
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
        self,
    ) -> None:
        generator = GitChangelogGenerator()
        request = ChangelogRequest(from_version="2.0.0", to_version="HEAD")

        with patch(
            "scripts.release.infrastructure.changelog.git_changelog_generator.run",
            return_value="",
        ):
            response = await generator.generate(request)

        assert response.entries == []

    @pytest.mark.asyncio
    async def test_generate_when_git_output_contains_blank_lines_then_blank_lines_ignored(
        self,
    ) -> None:
        generator = GitChangelogGenerator()
        request = ChangelogRequest(from_version="0.9.0", to_version="HEAD")

        git_output = "\n\n- Initial release (aaa111)\n\n"

        with patch(
            "scripts.release.infrastructure.changelog.git_changelog_generator.run",
            return_value=git_output,
        ):
            response = await generator.generate(request)

        assert response.entries == [
            "- Initial release (aaa111)",
        ]
