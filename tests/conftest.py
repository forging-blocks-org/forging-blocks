from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest


def _require_cli_tests() -> None:
    if os.getenv("RUN_CLI_TESTS") != "1":
        pytest.skip("CLI integration tests are disabled")


def _require_gh_auth() -> None:
    subprocess.run(["gh", "auth", "status"], check=True)


class _GitTestRepository:
    def __init__(self, path: Path) -> None:
        self._path = path

    @classmethod
    def init(cls, path: Path) -> _GitTestRepository:
        subprocess.run(["git", "init"], cwd=path, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=path, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=path, check=True)

        (path / "README.md").write_text("init")
        subprocess.run(["git", "add", "."], cwd=path, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=path, check=True)

        return cls(path)

    def write_file(self, name: str, content: str) -> None:
        (self._path / name).write_text(content)

    def commit(self, message: str) -> None:
        subprocess.run(["git", "add", "."], cwd=self._path, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=self._path, check=True)

    def last_commit_message(self) -> str:
        return subprocess.check_output(
            ["git", "log", "-1", "--pretty=%s"],
            cwd=self._path,
            text=True,
        ).strip()


@pytest.fixture
def git_repo(tmp_path: Path) -> _GitTestRepository:
    _require_cli_tests()
    return _GitTestRepository.init(tmp_path)


@pytest.fixture
def require_gh_auth() -> None:
    _require_cli_tests()
    _require_gh_auth()
