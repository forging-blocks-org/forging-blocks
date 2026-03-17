from pathlib import Path

import pytest

from tests.fixtures.git_test_repository import GitTestRepository


@pytest.fixture
def git_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> GitTestRepository:
    """Provides a temporary, fully initialised git repository.

    - Initialises a git repo via GitTestRepository.init()
    - Renames default branch to 'main' for consistency across environments
    - Changes the working directory to the repo root for the test duration
      so git-cliff and git commands resolve the repo from cwd
    - Directory is cleaned up automatically after each test
    """
    repo = GitTestRepository.init(tmp_path)
    monkeypatch.chdir(tmp_path)
    return repo
