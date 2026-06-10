import subprocess
from pathlib import Path

import pytest

from tests.fixtures.git_cliff_scenarios import (
    Scenario,
    scenario_changelog_with_unreleased,
    scenario_empty_repo,
    scenario_existing_changelog_no_unreleased,
    scenario_repo_with_multiple_tags,
    scenario_repo_with_single_tag,
)
from tests.fixtures.git_test_repository import GitTestRepository

__all__ = [
    "Scenario",
    "scenario_changelog_with_unreleased",
    "scenario_empty_repo",
    "scenario_existing_changelog_no_unreleased",
    "scenario_repo_with_multiple_tags",
    "scenario_repo_with_single_tag",
]


@pytest.fixture
def git_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> GitTestRepository:
    """Provides a temporary, fully initialised git repository."""
    repo = GitTestRepository.init(tmp_path)
    monkeypatch.chdir(tmp_path)
    return repo


@pytest.fixture
def pyproject_toml(git_repo: GitTestRepository) -> GitTestRepository:
    """Injects a minimal pyproject.toml (version 0.0.0) into the repo and commits it."""
    content = """\
[tool.poetry]
name = "test-project"
version = "0.0.0"
description = "Test project"
authors = ["Test <test@test.com>"]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
    (git_repo.path / "pyproject.toml").write_text(content, encoding="utf-8")
    git_repo.commit("chore: add pyproject.toml")
    return git_repo


@pytest.fixture
def git_repo_with_remote(
    git_repo: GitTestRepository, tmp_path_factory: pytest.TempPathFactory
) -> GitTestRepository:
    """Adds a bare git remote (origin) to the repo and pushes main.

    The bare remote is created in a separate temp directory (via
    ``tmp_path_factory``) so it lives *outside* the repository working
    tree.  This avoids staging/committing the remote's internal objects
    when helpers call ``git add .``, keeping tests deterministic and fast.
    """
    remote_path = tmp_path_factory.mktemp("remote")
    subprocess.run(["git", "init", "--bare", str(remote_path)], check=True)
    subprocess.run(
        ["git", "remote", "add", "origin", str(remote_path)],
        cwd=git_repo.path,
        check=True,
    )
    subprocess.run(
        ["git", "push", "-u", "origin", "main"],
        cwd=git_repo.path,
        check=True,
    )
    return git_repo
