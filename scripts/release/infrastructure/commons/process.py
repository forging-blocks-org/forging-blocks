import logging
import subprocess
from abc import ABC, abstractmethod

if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO)


class CommandRunner(ABC):
    """Abstraction for running system commands."""

    @abstractmethod
    def run(
        self,
        cmd: list[str],
        *,
        check: bool = True,
        suppress_error_log: bool = False,
    ) -> str:
        """Run a shell command and return its output.

        Args:
            cmd: The command and its arguments as a list of strings.
            check: Whether to raise an error on non-zero exit codes.

        Returns:
            The standard output of the command as a string.

        Raises:
            RuntimeError: If the command fails and check is True.
        """
        pass


class SubprocessCommandRunner(CommandRunner):
    def run(
        self,
        cmd: list[str],
        *,
        check: bool = True,
        suppress_error_log: bool = False,
    ) -> str:
        """Run a command and return stdout.

        Raises RuntimeError on failure.
        """
        logging.debug(f"Running command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                check=check,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            return result.stdout.strip()
        except subprocess.CalledProcessError as exc:
            # Log as debug if it's an expected failure, error if unexpected
            log_level = logging.DEBUG if suppress_error_log else logging.ERROR

            # Create a more user-friendly error message
            command_str = " ".join(cmd)

            # Extract meaningful error information
            stderr_output = exc.stderr.strip() if exc.stderr else ""

            # For git commands, provide more context
            if cmd[0] == "git":
                error_context = self._get_git_error_context(cmd, stderr_output)
            else:
                error_context = stderr_output or f"Command exited with code {exc.returncode}"

            error_msg = f"Command failed: {command_str}"
            if error_context:
                error_msg += f"\n{error_context}"

            logging.log(log_level, error_msg)
            raise RuntimeError(error_msg) from exc

    def _get_git_error_context(self, cmd: list[str], stderr: str) -> str:
        """Extract meaningful context from git command errors."""
        if "commit" in cmd and "nothing to commit" in stderr:
            return "Nothing to commit - working tree clean"
        elif "commit" in cmd and stderr:
            return f"Commit failed: {stderr}"
        elif "push" in cmd and "rejected" in stderr:
            return f"Push rejected: {stderr}"
        elif "push" in cmd and stderr:
            return f"Push failed: {stderr}"
        elif stderr:
            return stderr
        else:
            return f"Git command failed with exit code {cmd}"
