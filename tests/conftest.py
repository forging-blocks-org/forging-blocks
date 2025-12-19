import os
import subprocess
from pathlib import Path
from typing import Iterator

import pytest


@pytest.fixture()
def git_repo(tmp_path: Path) -> Iterator[Path]:
    cwd = os.getcwd()
    try:
        os.chdir(tmp_path)

        subprocess.run(["git", "init", "-b", "main"], check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], check=True)

        (tmp_path / "README.md").write_text("# test repo\n")
        subprocess.run(["git", "add", "README.md"], check=True)
        subprocess.run(["git", "commit", "-m", "initial commit"], check=True)

        yield tmp_path
    finally:
        os.chdir(cwd)
