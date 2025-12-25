import logging
import subprocess

if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO)

def run(
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
