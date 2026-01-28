from __future__ import annotations

from pathlib import Path

import pytest

from tests.fixtures.git_test_repository import GitTestRepository


@pytest.fixture
def git_repo(tmp_path: Path) -> GitTestRepository:
    # Git repository tests should always run - they're self-contained
    return GitTestRepository.init(tmp_path)
