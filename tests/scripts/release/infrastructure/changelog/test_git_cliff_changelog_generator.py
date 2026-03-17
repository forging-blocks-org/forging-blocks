"""Integration tests for GitCliffChangelogGenerator.

The happy-path tests run against a real temporary git repository with real git
and git-cliff binaries, exercising the full adapter stack without mocking.
The missing-binary error case is simulated by mocking subprocess invocation.

Commit message assertions match cliff.toml rendering: git-cliff strips
conventional commit prefixes and capitalises the description, so
"feat: add feature after tag" is rendered as "Add feature after tag".
"""

from pathlib import Path
from unittest.mock import patch

import pytest
from scripts.release.application.ports.outbound import ChangelogRequest
from scripts.release.infrastructure.changelog.git_cliff_changelog_generator import (
    GitCliffChangelogGenerator,
)
from scripts.release.infrastructure.commons.process import SubprocessCommandRunner
from tests.fixtures.git_test_repository import GitTestRepository

from scripts.release.application.errors import ChangelogGenerationError


def _make_generator(repo: GitTestRepository) -> GitCliffChangelogGenerator:
    return GitCliffChangelogGenerator(
        runner=repo.scoped_runner(),
        changelog_path=repo.path / "CHANGELOG.md",
    )


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

        def mock_run(*args, **kwargs):
            if args[0][0] == "git-cliff":
                raise FileNotFoundError("[Errno 2] No such file or directory: 'git-cliff'")
            return __import__("subprocess").run(*args, **kwargs)

        with patch("subprocess.run", side_effect=mock_run):
            with pytest.raises(
                ChangelogGenerationError, match="git-cliff is not installed or not found in PATH"
            ):
                await generator.generate(ChangelogRequest(from_version="1.0.0"))
