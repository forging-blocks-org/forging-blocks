from __future__ import annotations

from unittest.mock import MagicMock, call, create_autospec

import pytest
from scripts.release.application.ports.outbound import ChangelogRequest
from scripts.release.infrastructure.changelog.git_cliff_changelog_generator import (
    GitCliffChangelogGenerator,
)
from scripts.release.infrastructure.commons.process import CommandRunner


@pytest.mark.integration
class TestGitCliffChangelogGenerator:
    @pytest.fixture
    def runner_mock(self) -> MagicMock:
        return create_autospec(CommandRunner)

    @pytest.fixture
    def generator(self, runner_mock: MagicMock) -> GitCliffChangelogGenerator:
        return GitCliffChangelogGenerator(runner=runner_mock)

    @pytest.fixture
    def request_v1(self) -> ChangelogRequest:
        return ChangelogRequest(from_version="1.0.0")

    async def test_generate_with_existing_tag(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        request_v1: ChangelogRequest,
    ) -> None:
        # Setup the mock to indicate the tag exists and return a changelog
        runner_mock.run.side_effect = [
            "",  # _tag_exists returns True
            "feat: Add new feature\nfix: Bug fix\n",  # _run_git_cliff output
        ]

        response = await generator.generate(request_v1)

        assert response.entries == ["feat: Add new feature", "fix: Bug fix"]
        runner_mock.run.assert_has_calls(
            [
                call(["git", "rev-parse", "--verify", "v1.0.0"], suppress_error_log=True),
                call(
                    [
                        "git-cliff",
                        "--output",
                        "-",
                        "--format",
                        "{message} ({id:.7})",
                        "--tag",
                        "v1.0.0",
                    ],
                    check=True,
                ),
            ]
        )

    async def test_generate_with_nonexistent_tag_and_no_tags(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        request_v1: ChangelogRequest,
    ) -> None:
        # Setup the mock to indicate the tag does not exist and no tags are present
        runner_mock.run.side_effect = [
            RuntimeError("Tag not found"),  # _tag_exists returns False
            RuntimeError("No tags found"),  # _latest_tag returns None
            "feat: Initial commit\n",  # _run_git_cliff output
        ]

        response = await generator.generate(request_v1)

        assert response.entries == ["feat: Initial commit"]
        runner_mock.run.assert_has_calls(
            [
                call(["git", "rev-parse", "--verify", "v1.0.0"], suppress_error_log=True),
                call(["git", "describe", "--tags", "--abbrev=0"], suppress_error_log=True),
                call(["git-cliff", "--output", "-", "--format", "{message} ({id:.7})"], check=True),
            ]
        )

    async def test_generate_with_nonexistent_tag_and_existing_tags(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        request_v1: ChangelogRequest,
    ) -> None:
        runner_mock.run.side_effect = [
            RuntimeError("Tag not found"),
            "v0.9.0\n",
            "feat: Add feature since last tag",
        ]

        response = await generator.generate(request_v1)

        assert response.entries == ["feat: Add feature since last tag"]
        runner_mock.run.assert_has_calls(
            [
                call(["git", "rev-parse", "--verify", "v1.0.0"], suppress_error_log=True),
                call(["git", "describe", "--tags", "--abbrev=0"], suppress_error_log=True),
                call(
                    [
                        "git-cliff",
                        "--output",
                        "-",
                        "--format",
                        "{message} ({id:.7})",
                        "--tag",
                        "v0.9.0",
                    ],
                    check=True,
                ),
            ]
        )
