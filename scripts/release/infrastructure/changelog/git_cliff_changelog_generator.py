from __future__ import annotations

from scripts.release.application.errors.change_log_generation_error import ChangelogGenerationError
from scripts.release.application.ports.outbound import (
    ChangelogRequest,
    ChangelogResponse,
)
from scripts.release.infrastructure.commons.process import CommandRunner, SubprocessCommandRunner

from release.application.ports.outbound.changelog_generator import ChangelogGenerator


class GitCliffChangelogGenerator(ChangelogGenerator):
    """Adapter that generates changelogs using git-cliff."""

    def __init__(self, runner: CommandRunner | None = None) -> None:
        self._runner = runner or SubprocessCommandRunner()

    async def generate(self, request: ChangelogRequest) -> ChangelogResponse:
        from_tag = f"v{request.from_version}"
        tag_exists = self._tag_exists(from_tag)
        latest_tag = self._latest_tag() if not tag_exists else None

        range_arg = self._resolve_range(
            requested_tag=from_tag,
            tag_exists=tag_exists,
            latest_tag=latest_tag,
        )

        raw = self._run_git_cliff(range_arg)
        entries = self._parse_output(raw)

        return ChangelogResponse(entries=entries)

    def _tag_exists(self, tag: str) -> bool:
        try:
            self._runner.run(
                ["git", "rev-parse", "--verify", tag],
                suppress_error_log=True,
            )
            return True
        except RuntimeError:
            return False

    def _latest_tag(self) -> str | None:
        try:
            result = self._runner.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                suppress_error_log=True,
            )
            return result.strip() or None
        except RuntimeError:
            return None

    def _resolve_range(
        self,
        *,
        requested_tag: str,
        tag_exists: bool,
        latest_tag: str | None,
    ) -> str | None:
        """Return a git-cliff --tag-pattern / range string, or None for full history."""
        if tag_exists:
            return requested_tag
        return latest_tag  # None signals "no range — use full history"

    def _run_git_cliff(self, from_tag: str | None) -> str:
        cmd = ["git-cliff", "--output", "-", "--format", "{message} ({id:.7})"]

        if from_tag:
            cmd += ["--tag", from_tag]

        try:
            return self._runner.run(cmd, check=True)
        except RuntimeError as exc:
            raise ChangelogGenerationError(f"git-cliff failed: {exc}") from exc

    def _parse_output(self, raw: str) -> list[str]:
        return [line.strip() for line in raw.splitlines() if line.strip()]
