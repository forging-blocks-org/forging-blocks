from __future__ import annotations

from scripts.release.application.errors.change_log_generation_error import ChangelogGenerationError
from scripts.release.application.ports.outbound import (
    ChangelogGenerator,
    ChangelogRequest,
    ChangelogResponse,
)
from scripts.release.infrastructure.commons.process import CommandRunner, SubprocessCommandRunner


class GitChangelogGenerator(ChangelogGenerator):
    """Adapter that generates changelogs from Git commit history."""

    def __init__(self, runner: CommandRunner = SubprocessCommandRunner()) -> None:
        self._runner = runner

    async def generate(self, request: ChangelogRequest) -> ChangelogResponse:
        # First, try to find the actual latest tag if the requested version doesn't exist
        from_tag = await self._find_suitable_from_tag(request.from_version)

        if from_tag:
            range_expr = f"{from_tag}..HEAD"
        else:
            # If no tags exist, get all commits
            range_expr = "HEAD"

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

    async def _find_suitable_from_tag(self, requested_version: str) -> str | None:
        """Find a suitable tag to use as the 'from' reference for changelog generation."""
        requested_tag = f"v{requested_version}"

        # First, check if the requested tag exists
        try:
            self._runner.run(
                ["git", "rev-parse", "--verify", requested_tag], suppress_error_log=True
            )
            return requested_tag
        except RuntimeError:
            pass  # Tag doesn't exist, try to find the latest tag

        # Get the latest tag if the requested one doesn't exist
        try:
            latest_tag = self._runner.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                suppress_error_log=True
            )
            return latest_tag.strip()
        except RuntimeError:
            # No tags exist at all
            return None

    def _parse_git_output(self, output: str) -> list[str]:
        """Parse git log output into changelog entries."""
        return [line.strip() for line in output.splitlines() if line.strip()]
