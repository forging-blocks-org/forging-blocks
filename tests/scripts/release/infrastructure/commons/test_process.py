import subprocess
from unittest.mock import patch

import pytest

from scripts.release.infrastructure.commons.process import run


class TestProcessRun:
    def test_run_when_command_succeeds_then_returns_stdout(self) -> None:
        completed = subprocess.CompletedProcess(
            args=["echo", "ok"],
            returncode=0,
            stdout="ok\n",
            stderr="",
        )

        with patch("subprocess.run", return_value=completed) as run_mock:
            result = run(["echo", "ok"])

        assert result == "ok"
        run_mock.assert_called_once_with(
            ["echo", "ok"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_run_when_command_fails_then_raises_runtime_error(self) -> None:
        exc = subprocess.CalledProcessError(
            returncode=1,
            cmd=["git", "status"],
            stderr="fatal: not a git repository",
        )

        with patch("subprocess.run", side_effect=exc):
            with pytest.raises(RuntimeError) as err:
                run(["git", "status"])

        message = str(err.value)
        assert "git status" in message
        assert "fatal: not a git repository" in message

    def test_run_when_check_is_false_then_does_not_raise(self) -> None:
        completed = subprocess.CompletedProcess(
            args=["false"],
            returncode=1,
            stdout="some output\n",
            stderr="some error",
        )

        with patch("subprocess.run", return_value=completed) as run_mock:
            result = run(["false"], check=False)

        assert result == "some output"
        run_mock.assert_called_once()
