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
    ) -> str:
        """
        Run a shell command and return its ouput.

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
    ) -> str:
        """
        Run a command and return stdout.

        Raises RuntimeError on failure.
        """
        logging.info(f"Running command: {' '.join(cmd)}")

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
            logging.error(f"Command failed: {' '.join(cmd)}\n{exc.stderr}")
            raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{exc.stderr}") from exc
