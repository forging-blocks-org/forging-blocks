"""Integration tests for GitCliffChangelogGenerator.

The happy-path tests run against a real temporary git repository with real git
and git-cliff binaries, exercising the full adapter stack without mocking.
The missing-binary error case is simulated by mocking subprocess invocation.

Commit message assertions match cliff.toml rendering: git-cliff strips
conventional commit prefixes and capitalises the description, so
"feat: add feature after tag" is rendered as "Add feature after tag".
"""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, create_autospec, patch

import pytest
from scripts.release.application.ports.outbound import ChangelogRequest
from scripts.release.infrastructure.changelog.git_cliff_changelog_generator import (
    GitCliffChangelogGenerator,
)
from scripts.release.infrastructure.commons.process import CommandRunner, SubprocessCommandRunner
from tests.fixtures.git_test_repository import GitTestRepository

from scripts.release.application.errors import ChangelogGenerationError


def _make_generator(repo: GitTestRepository) -> GitCliffChangelogGenerator:
    return GitCliffChangelogGenerator(
        runner=repo.scoped_runner(),
        changelog_path=repo.path / "CHANGELOG.md",
    )


@pytest.mark.unit
class TestGitCliffChangelogGeneratorUnit:
    @pytest.fixture
    def runner_mock(self) -> MagicMock:
        return create_autospec(CommandRunner, instance=True)

    @pytest.fixture
    def changelog_path(self, tmp_path: Path) -> Path:
        return tmp_path / "CHANGELOG.md"

    @pytest.fixture
    def generator(
        self,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> GitCliffChangelogGenerator:
        return GitCliffChangelogGenerator(runner=runner_mock, changelog_path=changelog_path)

    # ------------------------------------------------------------------
    # Range resolution — driven through generate()
    # ------------------------------------------------------------------

    async def test_generate_uses_requested_tag_as_range_when_it_exists(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.side_effect = [
            "abc123",  # rev-parse succeeds → tag exists
            "## v1.0.0\n",  # git-cliff output
        ]

        await generator.generate(ChangelogRequest(from_version="1.0.0"))

        git_cliff_call = runner_mock.run.call_args_list[1]
        cmd = git_cliff_call[0][0]
        assert "--tag" in cmd
        assert "v1.0.0" in cmd
        assert "v1.0.0.." in cmd[-1]

    async def test_generate_falls_back_to_latest_tag_as_range_when_requested_tag_missing(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.side_effect = [
            RuntimeError("not found"),  # rev-parse fails → tag missing
            "v0.9.0",  # git describe → latest tag
            "## v1.1.0\n",  # git-cliff output
        ]

        await generator.generate(ChangelogRequest(from_version="1.1.0"))

        git_cliff_call = runner_mock.run.call_args_list[2]
        cmd = git_cliff_call[0][0]
        assert "v0.9.0.." in cmd[-1]
        assert "v1.1.0" in cmd

    async def test_generate_produces_full_history_when_no_tags_exist(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.side_effect = [
            RuntimeError("not found"),  # rev-parse fails
            RuntimeError("no tags"),  # git describe fails
            "## v0.1.0\n",  # git-cliff output
        ]

        await generator.generate(ChangelogRequest(from_version="0.1.0"))

        git_cliff_call = runner_mock.run.call_args_list[2]
        cmd = git_cliff_call[0][0]
        assert "--" not in cmd

    # ------------------------------------------------------------------
    # Response shape
    # ------------------------------------------------------------------

    async def test_generate_returns_parsed_entries(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.side_effect = [
            "abc123",
            "## v1.0.0\n- feat: something\n",
        ]

        result = await generator.generate(ChangelogRequest(from_version="1.0.0"))

        assert result.entries == ["## v1.0.0", "- feat: something"]

    async def test_generate_returns_empty_entries_for_blank_cliff_output(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.side_effect = [
            "abc123",
            "\n\n",
        ]

        result = await generator.generate(ChangelogRequest(from_version="1.0.0"))

        assert result.entries == []

    # ------------------------------------------------------------------
    # File writing
    # ------------------------------------------------------------------

    async def test_generate_writes_changelog_to_configured_path(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        runner_mock.run.side_effect = [
            "abc123",
            "## v1.0.0\n- feat: something\n",
        ]

        await generator.generate(ChangelogRequest(from_version="1.0.0"))

        assert changelog_path.exists()
        assert "## v1.0.0" in changelog_path.read_text(encoding="utf-8")

    async def test_generate_ensures_changelog_ends_with_newline_when_cliff_omits_it(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        runner_mock.run.side_effect = [
            "abc123",
            "## v1.0.0\n- feat: no trailing newline",
        ]

        await generator.generate(ChangelogRequest(from_version="1.0.0"))

        assert changelog_path.read_text(encoding="utf-8").endswith("\n")

    async def test_generate_does_not_double_newline_when_cliff_output_already_ends_with_one(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        runner_mock.run.side_effect = [
            "abc123",
            "## v1.0.0\n- feat: something\n",
        ]

        await generator.generate(ChangelogRequest(from_version="1.0.0"))

        assert not changelog_path.read_text(encoding="utf-8").endswith("\n\n")

    # ------------------------------------------------------------------
    # Error handling
    # ------------------------------------------------------------------

    async def test_generate_raises_changelog_generation_error_when_git_cliff_not_installed(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.side_effect = [
            "abc123",
            FileNotFoundError("git-cliff not found"),
        ]

        with pytest.raises(ChangelogGenerationError, match="not installed or not found"):
            await generator.generate(ChangelogRequest(from_version="1.0.0"))

    async def test_generate_raises_changelog_generation_error_when_git_cliff_fails(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.side_effect = [
            "abc123",
            RuntimeError("exit code 1"),
        ]

        with pytest.raises(ChangelogGenerationError, match="git-cliff failed"):
            await generator.generate(ChangelogRequest(from_version="1.0.0"))


@pytest.mark.integration
class TestGitCliffChangelogGenerator:
    async def test_generate_when_tag_exists_then_returns_entries_since_that_tag(
        self, git_repo: GitTestRepository
    ) -> None:
        """Tag exists — changelog contains only commits after it."""
        git_repo.write_file("a.txt", "a")
        git_repo.commit("feat: commit before tag")
        git_repo.create_tag("v1.0.0")
        git_repo.write_file("b.txt", "b")
        git_repo.commit("feat: add feature after tag")
        git_repo.write_file("c.txt", "c")
        git_repo.commit("fix: fix bug after tag")

        response = await _make_generator(git_repo).generate(ChangelogRequest(from_version="1.0.0"))

        full_output = "\n".join(response.entries)
        assert "Add feature after tag" in full_output
        assert "Fix bug after tag" in full_output
        assert "Commit before tag" not in full_output
        assert "[1.0.0]" in full_output
        assert "unreleased" not in full_output.lower()
        assert (git_repo.path / "CHANGELOG.md").exists()

    async def test_generate_when_tag_not_yet_created_then_uses_requested_version(
        self, git_repo: GitTestRepository
    ) -> None:
        """Requested tag doesn't exist in git yet — uses requested version in output."""
        git_repo.write_file("a.txt", "a")
        git_repo.commit("feat: commit before tag")
        git_repo.create_tag("v1.0.0")
        git_repo.write_file("b.txt", "b")
        git_repo.commit("feat: add feature after tag")

        response = await _make_generator(git_repo).generate(ChangelogRequest(from_version="1.1.0"))

        full_output = "\n".join(response.entries)
        assert "Add feature after tag" in full_output
        assert "[1.1.0]" in full_output
        assert "unreleased" not in full_output.lower()
        assert (git_repo.path / "CHANGELOG.md").exists()

    async def test_generate_when_tag_missing_but_other_tags_exist_then_returns_entries_since_latest_tag(
        self, git_repo: GitTestRepository
    ) -> None:
        """Requested tag doesn't exist — falls back to latest tag in repo."""
        git_repo.write_file("a.txt", "a")
        git_repo.commit("feat: base commit")
        git_repo.create_tag("v0.9.0")
        git_repo.write_file("b.txt", "b")
        git_repo.commit("feat: commit after latest tag")

        response = await _make_generator(git_repo).generate(ChangelogRequest(from_version="1.0.0"))

        full_output = "\n".join(response.entries)
        assert "Commit after latest tag" in full_output
        assert "Base commit" not in full_output
        assert (git_repo.path / "CHANGELOG.md").exists()

    async def test_generate_when_no_tags_exist_then_returns_full_history(
        self, git_repo: GitTestRepository
    ) -> None:
        """No tags at all — full commit history is returned."""
        git_repo.write_file("a.txt", "a")
        git_repo.commit("feat: first commit")
        git_repo.write_file("b.txt", "b")
        git_repo.commit("feat: second commit")

        response = await _make_generator(git_repo).generate(ChangelogRequest(from_version="1.0.0"))

        full_output = "\n".join(response.entries)
        assert "First commit" in full_output
        assert "Second commit" in full_output
        assert (git_repo.path / "CHANGELOG.md").exists()

    async def test_generate_when_not_a_git_repo_then_raises_changelog_generation_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """git-cliff fails when cwd is not a git repository."""
        monkeypatch.chdir(tmp_path)

        generator = GitCliffChangelogGenerator(
            runner=SubprocessCommandRunner(),
            changelog_path=tmp_path / "CHANGELOG.md",
        )

        with pytest.raises(ChangelogGenerationError, match="git-cliff failed"):
            await generator.generate(ChangelogRequest(from_version="1.0.0"))

    async def test_generate_when_file_not_found_then_changelog_generation_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """git-cliff raises FileNotFoundError when binary is not in PATH."""
        monkeypatch.chdir(tmp_path)

        generator = GitCliffChangelogGenerator(
            runner=SubprocessCommandRunner(),
            changelog_path=tmp_path / "CHANGELOG.md",
        )

        original_run = subprocess.run

        def mock_run(*args, **kwargs):
            if args[0][0] == "git-cliff":
                raise FileNotFoundError("[Errno 2] No such file or directory: 'git-cliff'")
            return original_run(*args, **kwargs)

        with patch("subprocess.run", side_effect=mock_run):
            with pytest.raises(
                ChangelogGenerationError, match="git-cliff is not installed or not found in PATH"
            ):
                await generator.generate(ChangelogRequest(from_version="1.0.0"))
