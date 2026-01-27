from abc import ABC, abstractmethod
import logging
import subprocess


if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO)


class CommandRunner(ABC):
    """
    Abstraction for running system commands.
    """
    @abstractmethod
    def run(
        self,
        cmd: list[str],
        *,
        check: bool = True,
        suppress_error_log: bool = False,
    ) -> str:
        """
        Run a shell command and return its output.

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
        """
        Run a command and return stdout.

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
            logging.log(log_level, f"Command failed: {' '.join(cmd)}\n{exc.stderr}")
            raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{exc.stderr}") from exc
