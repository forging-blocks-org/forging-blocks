from __future__ import annotations

import os
from pathlib import Path
from subprocess import check_output as subprocess_check_output
from subprocess import run as subprocess_run

from .scoped_command_runner import ScopedCommandRunner

# When running inside a git hook (e.g. pre-push via pre-commit), GIT_DIR and
# related env vars point at the main repository.  These leak into test fixtures
# that create ephemeral git repos in temp directories and break git operations.
# We remove them from the subprocess environment so that git uses the cwd-based
# repo discovery instead.
SANITIZED_ENV = {
    k: v
    for k, v in os.environ.items()
    if k
    not in {
        "GIT_DIR",
        "GIT_WORK_TREE",
        "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    }
}


class GitTestRepository:
    def __init__(self, path: Path) -> None:
        self._path = path

    @classmethod
    def init(cls, path: Path) -> GitTestRepository:
        subprocess_run(["git", "init"], cwd=path, check=True, env=SANITIZED_ENV)
        subprocess_run(
            ["git", "config", "user.name", "Test"], cwd=path, check=True, env=SANITIZED_ENV
        )
        subprocess_run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=path,
            check=True,
            env=SANITIZED_ENV,
        )

        (path / "README.md").write_text("init")
        subprocess_run(["git", "add", "."], cwd=path, check=True, env=SANITIZED_ENV)
        subprocess_run(["git", "commit", "-m", "init"], cwd=path, check=True, env=SANITIZED_ENV)

        # Rename default branch to 'main' to ensure consistency across environments
        subprocess_run(["git", "branch", "-M", "main"], cwd=path, check=True, env=SANITIZED_ENV)

        return cls(path)

    @property
    def path(self) -> Path:
        """Get the path to the test repository."""
        return self._path

    @property
    def tags(self) -> list[str]:
        tags_output = subprocess_check_output(
            ["git", "tag"],
            cwd=self._path,
            text=True,
            env=SANITIZED_ENV,
        )
        return tags_output.strip().splitlines()

    def create_tag(self, tag: str) -> None:
        subprocess_run(["git", "tag", tag], cwd=self._path, check=True, env=SANITIZED_ENV)

    def commit(self, message: str) -> None:
        subprocess_run(["git", "add", "."], cwd=self._path, check=True, env=SANITIZED_ENV)
        subprocess_run(
            ["git", "commit", "-m", message], cwd=self._path, check=True, env=SANITIZED_ENV
        )

    def write_file(self, name: str, content: str) -> None:
        (self._path / name).write_text(content)

    def last_commit_message(self) -> str:
        return subprocess_check_output(
            ["git", "log", "-1", "--pretty=%s"],
            cwd=self._path,
            text=True,
            env=SANITIZED_ENV,
        ).strip()

    def run_git_command(self, cmd: list[str]) -> str:
        """Run a git command in this repository's context."""
        return subprocess_check_output(cmd, cwd=self._path, text=True, env=SANITIZED_ENV).strip()

    def scoped_runner(self) -> ScopedCommandRunner:
        """Get a command runner scoped to this repository."""
        return ScopedCommandRunner(self._path)
