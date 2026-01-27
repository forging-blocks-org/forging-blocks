from __future__ import annotations

from pathlib import Path
from subprocess import run as subprocess_run, check_output as subprocess_check_output


class GitTestRepository:
    def __init__(self, path: Path) -> None:
        self._path = path

    @classmethod
    def init(cls, path: Path) -> GitTestRepository:
        subprocess_run(["git", "init"], cwd=path, check=True)
        subprocess_run(["git", "config", "user.name", "Test"], cwd=path, check=True)
        subprocess_run(
            ["git", "config", "user.email", "test@example.com"], cwd=path, check=True
        )

        (path / "README.md").write_text("init")
        subprocess_run(["git", "add", "."], cwd=path, check=True)
        subprocess_run(["git", "commit", "-m", "init"], cwd=path, check=True)

        # Rename default branch to 'main' to ensure consistency across environments
        subprocess_run(["git", "branch", "-M", "main"], cwd=path, check=True)

        return cls(path)

    @property
    def tags(self) -> list[str]:
        tags_output = subprocess_check_output(
            ["git", "tag"],
            cwd=self._path,
            text=True,
        )
        return tags_output.strip().splitlines()

    def create_tag(self, tag: str) -> None:
        subprocess_run(["git", "tag", tag], cwd=self._path, check=True)

    def commit(self, message: str) -> None:
        subprocess_run(["git", "add", "."], cwd=self._path, check=True)
        subprocess_run(["git", "commit", "-m", message], cwd=self._path, check=True)

    def write_file(self, name: str, content: str) -> None:
        (self._path / name).write_text(content)

    def last_commit_message(self) -> str:
        return subprocess_check_output(
            ["git", "log", "-1", "--pretty=%s"],
            cwd=self._path,
            text=True,
        ).strip()
