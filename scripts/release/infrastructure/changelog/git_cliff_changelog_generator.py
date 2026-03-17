from __future__ import annotations

from pathlib import Path

from scripts.release.application.ports.outbound import (
    ChangelogGenerator,
    ChangelogRequest,
    ChangelogResponse,
)
from scripts.release.infrastructure.commons.process import CommandRunner

from scripts.release.application.errors import ChangelogGenerationError

_DEFAULT_CHANGELOG_PATH = Path("CHANGELOG.md")


class GitCliffChangelogGenerator(ChangelogGenerator):
    """Adapter that generates changelogs using git-cliff.

    Delegates all formatting to cliff.toml. The adapter is responsible
    only for resolving the correct commit range and invoking the binary.

    Range resolution strategy:
    - requested tag exists  → generate from that tag: `<tag>..`
    - requested tag missing, other tags exist → generate from latest tag: `<latest>..`
    - no tags at all → generate full history (no range argument)
    """

    def __init__(
        self,
        runner: CommandRunner,
        changelog_path: Path = _DEFAULT_CHANGELOG_PATH,
    ) -> None:
        self._runner = runner
        self._changelog_path = changelog_path

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
        """Return the starting tag for the range, or None for full history."""
        if tag_exists:
            return requested_tag
        return latest_tag  # None signals "no range — use full history"

    def _run_git_cliff(self, from_tag: str | None) -> str:
        cmd = ["git-cliff", "--output", "-"]

        if from_tag:
            cmd += ["--", f"{from_tag}.."]

        try:
            output = self._runner.run(cmd, check=True)
            self._changelog_path.write_text(output)
            return output
        except FileNotFoundError as exc:
            raise ChangelogGenerationError(
                "git-cliff is not installed or not found in PATH"
            ) from exc
        except RuntimeError as exc:
            raise ChangelogGenerationError(f"git-cliff failed: {exc}") from exc

    def _parse_output(self, raw: str) -> list[str]:
        return [line.strip() for line in raw.splitlines() if line.strip()]
