from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path

from scripts.release.infrastructure.commons.process import CommandRunner

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


class ScopedCommandRunner(CommandRunner):
    """Command runner that executes commands in a specific directory."""

    def __init__(self, working_directory: Path):
        self._cwd = working_directory

    def run(
        self,
        cmd: list[str],
        *,
        check: bool = True,
        suppress_error_log: bool = False,
    ) -> str:
        """Run a command in the specified working directory."""
        logging.debug(f"Running command in {self._cwd}: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                cwd=self._cwd,
                check=check,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=SANITIZED_ENV,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as exc:
            log_level = logging.DEBUG if suppress_error_log else logging.ERROR
            logging.log(log_level, f"Command failed: {' '.join(cmd)}\n{exc.stderr}")
            raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{exc.stderr}") from exc
