from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from tests.fixtures.git_test_repository import GitTestRepository


def _require_gh_auth() -> None:
    if os.getenv("RUN_CLI_TESTS") != "1":
        pytest.skip("CLI integration tests are disabled")
    subprocess.run(["gh", "auth", "status"], check=True)

@pytest.fixture
def git_repo(tmp_path: Path) -> GitTestRepository:
    # Git repository tests should always run - they're self-contained
    return GitTestRepository.init(tmp_path)


@pytest.fixture
def require_gh_auth() -> None:
    _require_gh_auth()
