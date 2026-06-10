# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import subprocess
from unittest.mock import patch

import pytest
from scripts.release.infrastructure.commons.process import SubprocessCommandRunner


@pytest.mark.integration
class TestSubprocessCommandRunner:
    def test_run_when_command_succeeds_returns_output(self):
        runner = SubprocessCommandRunner()

        result = runner.run(["echo", "Hello, world!"])

        assert result.strip() == "Hello, world!"

    def test_run_when_command_fails_raises_runtime_error(self):
        runner = SubprocessCommandRunner()

        try:
            runner.run(["false"])
        except RuntimeError as e:
            assert "Command failed: false" in str(e)
        else:
            assert False, "Expected RuntimeError was not raised"

    def test_run_with_check_false_returns_output_even_on_failure(self):
        runner = SubprocessCommandRunner()

        result = runner.run(["false"], check=False)

        assert result == ""

    def test_run_with_suppress_error_log_still_raises_runtime_error(self):
        runner = SubprocessCommandRunner()

        try:
            runner.run(["false"], suppress_error_log=True)
        except RuntimeError as e:
            assert "Command failed: false" in str(e)
        else:
            assert False, "Expected RuntimeError was not raised"


@pytest.mark.unit
class TestSubprocessCommandRunnerErrorHandling:
    def test_get_git_error_context_commit_nothing_to_commit(self):
        runner = SubprocessCommandRunner()
        cmd = ["git", "commit", "-m", "test"]
        stderr = "nothing to commit, working tree clean"

        context = runner._get_git_error_context(cmd, stderr)

        assert context == "Nothing to commit - working tree clean"

    def test_get_git_error_context_commit_with_error(self):
        runner = SubprocessCommandRunner()
        cmd = ["git", "commit", "-m", "test"]
        stderr = "Author identity unknown"

        context = runner._get_git_error_context(cmd, stderr)

        assert context == "Commit failed: Author identity unknown"

    def test_get_git_error_context_push_rejected(self):
        runner = SubprocessCommandRunner()
        cmd = ["git", "push", "origin", "main"]
        stderr = "! [rejected] main -> main (non-fast-forward)"

        context = runner._get_git_error_context(cmd, stderr)

        assert context == "Push rejected: ! [rejected] main -> main (non-fast-forward)"

    def test_get_git_error_context_push_failed(self):
        runner = SubprocessCommandRunner()
        cmd = ["git", "push", "origin", "main"]
        stderr = "remote: Permission denied"

        context = runner._get_git_error_context(cmd, stderr)

        assert context == "Push failed: remote: Permission denied"

    def test_get_git_error_context_general_stderr(self):
        runner = SubprocessCommandRunner()
        cmd = ["git", "status"]
        stderr = "fatal: not a git repository"

        context = runner._get_git_error_context(cmd, stderr)

        assert context == "fatal: not a git repository"

    def test_get_git_error_context_no_stderr(self):
        runner = SubprocessCommandRunner()
        cmd = ["git", "status"]
        stderr = ""

        context = runner._get_git_error_context(cmd, stderr)

        assert context == "Git command failed with exit code ['git', 'status']"

    @patch("subprocess.run")
    def test_run_git_command_with_context_extraction(self, mock_run):
        runner = SubprocessCommandRunner()

        exc = subprocess.CalledProcessError(1, ["git", "commit"], stderr="nothing to commit")
        mock_run.side_effect = exc

        with pytest.raises(RuntimeError) as exc_info:
            runner.run(["git", "commit", "-m", "test"])

        error_msg = str(exc_info.value)
        assert "Command failed: git commit -m test" in error_msg
        assert "Nothing to commit - working tree clean" in error_msg

    @patch("subprocess.run")
    def test_run_non_git_command_with_error(self, mock_run):
        runner = SubprocessCommandRunner()

        exc = subprocess.CalledProcessError(127, ["nonexistent"], stderr="command not found")
        mock_run.side_effect = exc

        with pytest.raises(RuntimeError) as exc_info:
            runner.run(["nonexistent"])

        error_msg = str(exc_info.value)
        assert "Command failed: nonexistent" in error_msg
        assert "command not found" in error_msg
