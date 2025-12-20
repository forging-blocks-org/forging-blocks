import subprocess


def run(
    cmd: list[str],
    *,
    check: bool = True,
) -> str:
    """
    Run a command and return stdout.

    Raises RuntimeError on failure.
    """
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
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{exc.stderr}") from exc
