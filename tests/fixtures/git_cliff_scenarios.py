from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from tests.fixtures.git_test_repository import GitTestRepository


_CLIFF_TOML = Path(__file__).resolve().parents[2] / "cliff.toml"


def _install_cliff_config(repo: GitTestRepository) -> None:
    dest = repo.path / "cliff.toml"
    shutil.copy2(_CLIFF_TOML, dest)
    repo.commit("chore(cliff): add cliff config")


class Scenario:
    def __init__(
        self,
        repo: GitTestRepository,
        *,
        from_version: str,
    ) -> None:
        self.repo = repo
        self.from_version = from_version

    @property
    def changelog_path(self) -> Path:
        return self.repo.path / "CHANGELOG.md"


@pytest.fixture
def scenario_empty_repo(git_repo: GitTestRepository) -> Scenario:
    _install_cliff_config(git_repo)
    return Scenario(git_repo, from_version="0.1.0")


@pytest.fixture
def scenario_repo_with_single_tag(git_repo: GitTestRepository) -> Scenario:
    _install_cliff_config(git_repo)

    git_repo.write_file("feature.py", "def hello(): ...")
    git_repo.commit("feat: add hello function")
    git_repo.create_tag("v0.1.0")

    git_repo.write_file("bugfix.py", "# bugfix")
    git_repo.commit("fix: resolve off-by-one error")
    git_repo.write_file("docs.md", "# docs")
    git_repo.commit("docs: update README")

    return Scenario(git_repo, from_version="0.1.0")


@pytest.fixture
def scenario_repo_with_multiple_tags(git_repo: GitTestRepository) -> Scenario:
    _install_cliff_config(git_repo)

    git_repo.write_file("a.txt", "a")
    git_repo.commit("feat: initial scaffold")
    git_repo.create_tag("v0.1.0")

    git_repo.write_file("b.txt", "b")
    git_repo.commit("feat: add user registration")
    git_repo.write_file("c.txt", "c")
    git_repo.commit("fix: prevent duplicate emails")
    git_repo.create_tag("v0.2.0")

    git_repo.write_file("d.txt", "d")
    git_repo.commit("feat: add password reset")
    git_repo.write_file("e.txt", "e")
    git_repo.commit("fix: handle expired tokens")

    return Scenario(git_repo, from_version="0.3.0")


@pytest.fixture
def scenario_changelog_with_unreleased(
    git_repo: GitTestRepository,
    scenario_repo_with_multiple_tags: Scenario,
) -> Scenario:
    repo = scenario_repo_with_multiple_tags.repo

    changelog = repo.path / "CHANGELOG.md"
    changelog.write_text(
        "## [Unreleased]\n"
        "\n"
        "### Features\n"
        "\n"
        "- **auth**: add password reset\n"
        "\n"
        "### Bug Fixes\n"
        "\n"
        "- **auth**: handle expired tokens\n"
        "\n"
        "## [0.2.0] - 2026-01-15\n"
        "\n"
        "### Features\n"
        "\n"
        "- **core**: add user registration\n"
        "\n"
        "### Bug Fixes\n"
        "\n"
        "- **core**: prevent duplicate emails\n"
        "\n"
        "## [0.1.0] - 2026-01-01\n"
        "\n"
        "### Features\n"
        "\n"
        "- **core**: initial scaffold\n",
        encoding="utf-8",
    )
    repo.commit("docs: add initial CHANGELOG.md")

    return Scenario(repo, from_version="0.3.0")


@pytest.fixture
def scenario_existing_changelog_no_unreleased(
    git_repo: GitTestRepository,
    scenario_repo_with_multiple_tags: Scenario,
) -> Scenario:
    repo = scenario_repo_with_multiple_tags.repo

    changelog = repo.path / "CHANGELOG.md"
    changelog.write_text(
        "## [0.2.0] - 2026-01-15\n"
        "\n"
        "### Features\n"
        "\n"
        "- **core**: add user registration\n"
        "\n"
        "### Bug Fixes\n"
        "\n"
        "- **core**: prevent duplicate emails\n"
        "\n"
        "## [0.1.0] - 2026-01-01\n"
        "\n"
        "### Features\n"
        "\n"
        "- **core**: initial scaffold\n",
        encoding="utf-8",
    )
    repo.commit("docs: add CHANGELOG.md without unreleased")

    return Scenario(repo, from_version="0.3.0")
