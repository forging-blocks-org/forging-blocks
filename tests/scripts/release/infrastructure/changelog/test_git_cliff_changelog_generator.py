from __future__ import annotations

from unittest.mock import MagicMock, call, create_autospec

import pytest
from scripts.release.application.ports.outbound import ChangelogRequest
from scripts.release.infrastructure.changelog.git_cliff_changelog_generator import (
    GitCliffChangelogGenerator,
)
from scripts.release.infrastructure.commons.process import CommandRunner

from scripts.release.application.errors import ChangelogGenerationError


@pytest.mark.integration
class TestGitCliffChangelogGenerator:
    @pytest.fixture
    def runner_mock(self) -> MagicMock:
        return create_autospec(CommandRunner, instance=True)

    @pytest.fixture
    def generator(self, runner_mock: MagicMock) -> GitCliffChangelogGenerator:
        return GitCliffChangelogGenerator(runner=runner_mock)

    @pytest.fixture
    def request_v1(self) -> ChangelogRequest:
        return ChangelogRequest(from_version="1.0.0")

    @pytest.fixture
    def tag_exists(self) -> str:
        """Runner response when the requested tag is found in git."""
        return ""

    @pytest.fixture
    def tag_not_found(self) -> RuntimeError:
        """Runner response when the requested tag does not exist."""
        return RuntimeError("Tag not found")

    @pytest.fixture
    def no_tags_in_repo(self) -> RuntimeError:
        """Runner response when no tags at all exist in the repository."""
        return RuntimeError("No tags found")

    @pytest.fixture
    def git_cliff_not_installed(self) -> FileNotFoundError:
        """Runner response when the git-cliff binary is not in PATH."""
        return FileNotFoundError("[Errno 2] No such file or directory: 'git-cliff'")

    @pytest.fixture
    def git_cliff_runtime_failure(self) -> RuntimeError:
        """Runner response when git-cliff exits with a non-zero code."""
        return RuntimeError("git-cliff process failed with exit code 1")

    async def test_generate_with_existing_tag(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        request_v1: ChangelogRequest,
        tag_exists: str,
    ) -> None:
        runner_mock.run.side_effect = [
            tag_exists,
            "feat: Add new feature\nfix: Bug fix\n",
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
        tag_not_found: RuntimeError,
        no_tags_in_repo: RuntimeError,
    ) -> None:
        runner_mock.run.side_effect = [
            tag_not_found,
            no_tags_in_repo,
            "feat: Initial commit\n",
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
        tag_not_found: RuntimeError,
    ) -> None:
        runner_mock.run.side_effect = [
            tag_not_found,
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

    async def test_generate_when_git_cliff_not_installed_then_change_log_generation_error_is_raised(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        request_v1: ChangelogRequest,
        tag_exists: str,
        git_cliff_not_installed: FileNotFoundError,
    ) -> None:
        runner_mock.run.side_effect = [
            tag_exists,
            git_cliff_not_installed,
        ]

        with pytest.raises(
            ChangelogGenerationError,
            match="git-cliff is not installed or not found in PATH",
        ):
            await generator.generate(request_v1)

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

    async def test_generate_when_git_cliff_fails_then_change_log_generation_error_is_raised(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        request_v1: ChangelogRequest,
        tag_exists: str,
        git_cliff_runtime_failure: RuntimeError,
    ) -> None:
        runner_mock.run.side_effect = [
            tag_exists,
            git_cliff_runtime_failure,
        ]

        with pytest.raises(ChangelogGenerationError, match="git-cliff failed"):
            await generator.generate(request_v1)

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
