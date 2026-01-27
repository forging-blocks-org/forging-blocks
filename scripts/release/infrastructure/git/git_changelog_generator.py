from __future__ import annotations

from scripts.release.infrastructure.commons.process import CommandRunner, SubprocessCommandRunner
from scripts.release.application.errors.change_log_generation_error import ChangelogGenerationError
from scripts.release.application.ports.outbound import (
    ChangelogGenerator,
    ChangelogRequest,
    ChangelogResponse,
)


class GitChangelogGenerator(ChangelogGenerator):
    """Adapter that generates changelogs from Git commit history."""

    def __init__(self, runner: CommandRunner = SubprocessCommandRunner()) -> None:
        self._runner = runner

    async def generate(self, request: ChangelogRequest) -> ChangelogResponse:
        range_expr = f"v{request.from_version}..HEAD"

        try:
            result = self._runner.run(
                [
                    "git",
                    "log",
                    range_expr,
                    "--pretty=format:- %s (%h)",
                ],
                check=True,
            )
        except RuntimeError as e:
            raise ChangelogGenerationError(f"Failed to generate changelog: {e}") from e

        entries = self._parse_git_output(result)

        return ChangelogResponse(entries=entries)

    def _parse_git_output(self, output: str) -> list[str]:
        """Parse git log output into changelog entries."""
        return [line.strip() for line in output.splitlines() if line.strip()]
