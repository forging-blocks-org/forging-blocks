from __future__ import annotations

import logging
import subprocess
from pathlib import Path


class ScopedCommandRunner:
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
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as exc:
            log_level = logging.DEBUG if suppress_error_log else logging.ERROR
            logging.log(log_level, f"Command failed: {' '.join(cmd)}\n{exc.stderr}")
            raise RuntimeError(
                f"Command failed: {' '.join(cmd)}\n{exc.stderr}"
            ) from exc
