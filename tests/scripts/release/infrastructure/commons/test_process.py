import subprocess
from unittest.mock import MagicMock, patch

import pytest

from scripts.release.infrastructure.commons.process import run


class TestProcessRun:
    @patch("subprocess.run")
    def test_run_when_command_succeeds_then_returns_stdout(
        self,
        run_mock: MagicMock,
    ) -> None:
        completed = subprocess.CompletedProcess(
            args=["echo", "ok"],
            returncode=0,
            stdout="ok\n",
            stderr="",
        )
        run_mock.return_value = completed

        result = run(["echo", "ok"])

        assert result == "ok"
        run_mock.assert_called_once_with(
            ["echo", "ok"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    @patch("logging.info")
    def test_run_when_command_succeeds_then_logs_running_command(
        self,
        logging_mock: MagicMock
    ) -> None:
        completed = subprocess.CompletedProcess(
            args=["echo", "ok"],
            returncode=0,
            stdout="ok\n",
            stderr="",
        )
        logging_mock.return_value = completed

        result = run(["echo", "ok"])

        assert result == "ok"
        logging_mock.assert_called_once_with("Running command: echo ok")

    @patch("logging.error")
    @patch("subprocess.run")
    def test_run_when_command_raises_error_then_logs_command_failed(
        self,
        subprocess_run_mock: MagicMock,
        logging_mock: MagicMock
    ) -> None:
        # Setup the subprocess.CalledProcessError exception
        exc: subprocess.CalledProcessError = subprocess.CalledProcessError(
            returncode=1,
            cmd=["git", "status"],
            stderr="fatal: not a git repository",
        )
        subprocess_run_mock.side_effect = exc

        # Check that RuntimeError is raised
        with pytest.raises(RuntimeError, match=r"Command failed: git status\nfatal: not a git repository") as err:
            run(["git", "status"])

        # Assert that logging.error was called once with the exact message
        logging_mock.assert_called_once_with("Command failed: git status\nfatal: not a git repository")

    @patch("subprocess.run")
    def test_run_when_command_fails_then_raises_runtime_error(
        self,
        subprocess_run_mock: MagicMock
    ) -> None:
        exc = subprocess.CalledProcessError(
            returncode=1,
            cmd=["git", "status"],
            stderr="fatal: not a git repository",
        )
        subprocess_run_mock.side_effect = exc

        with pytest.raises(RuntimeError) as err:
            run(["git", "status"])

        message = str(err.value)
        assert "git status" in message
        assert "fatal: not a git repository" in message

    @patch("subprocess.run")
    def test_run_when_check_is_false_then_does_not_raise(
        self,
        subprocess_run_mock: MagicMock
    ) -> None:
        completed = subprocess.CompletedProcess(
            args=["false"],
            returncode=1,
            stdout="some output\n",
            stderr="some error",
        )
        subprocess_run_mock.return_value = completed

        result = run(["false"], check=False)

        assert result == "some output"
        subprocess_run_mock.assert_called_once()
