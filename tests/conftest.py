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
