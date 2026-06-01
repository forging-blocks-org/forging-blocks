from __future__ import annotations

import re
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
    - requested tag missing → generate full history (no range argument)
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

        range_arg, version_tag = self._resolve_range_and_version(
            requested_tag=from_tag,
            tag_exists=tag_exists,
        )

        raw = self._run_git_cliff(range_arg, version_tag, dry_run=request.dry_run)
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

    def _resolve_range_and_version(
        self,
        *,
        requested_tag: str,
        tag_exists: bool,
    ) -> tuple[str | None, str | None]:
        """Return the starting tag for the range and version tag for git-cliff.

        The version_tag tells git-cliff what version to display in the changelog,
        even if the tag doesn't exist yet in git.
        """
        if tag_exists:
            return requested_tag, requested_tag
        return None, requested_tag

    def _run_git_cliff(
        self,
        from_tag: str | None,
        version_tag: str | None,
        *,
        dry_run: bool = False,
    ) -> str:
        cmd = ["git-cliff", "--output", "-"]

        if version_tag:
            cmd += ["--tag", version_tag]

        if from_tag:
            cmd += ["--", f"{from_tag}.."]
        else:
            cmd += ["--unreleased"]

        try:
            output = self._runner.run(cmd, check=True)
            if not dry_run:
                merged = self._merge_with_existing(output)
                self._changelog_path.write_text(
                    merged if merged.endswith("\n") else merged + "\n", encoding="utf-8"
                )
            return output
        except FileNotFoundError as exc:
            raise ChangelogGenerationError(
                "git-cliff is not installed or not found in PATH"
            ) from exc
        except RuntimeError as exc:
            raise ChangelogGenerationError(f"git-cliff failed: {exc}") from exc

    def _merge_with_existing(self, new_content: str) -> str:
        if not self._changelog_path.exists():
            return new_content

        existing = self._changelog_path.read_text(encoding="utf-8")

        unreleased_match = re.search(
            r"## \[Unreleased\]\s*\n\n(.*?)(?=\n## \[|\Z)",
            existing,
            re.DOTALL,
        )
        if not unreleased_match:
            version_header, _ = self._parse_version_section(new_content)
            bracket = re.search(r"\[([^\]]+)\]", version_header)
            if bracket and f"## [{bracket.group(1)}]" in existing:
                return existing
            return new_content.rstrip("\n") + "\n\n" + existing

        unreleased_body = unreleased_match.group(1).strip()
        existing_without_unreleased = (
            existing[: unreleased_match.start()] + existing[unreleased_match.end() :]
        ).lstrip("\n")

        if not unreleased_body:
            return new_content.rstrip("\n") + "\n\n" + existing_without_unreleased

        unreleased_groups = self._parse_groups(unreleased_body)
        version_header, new_groups = self._parse_version_section(new_content)

        merged_by_header = dict(new_groups)
        orphan_groups: list[tuple[str, str]] = []

        for header, entries in unreleased_groups:
            if header in merged_by_header:
                merged_by_header[header] = merged_by_header[header] + "\n\n" + entries
            else:
                orphan_groups.append((header, entries))

        merged_new_groups = list(merged_by_header.items())

        parts = [version_header, ""]
        for header, entries in merged_new_groups:
            parts.extend([header, "", entries, ""])
        for header, entries in orphan_groups:
            parts.extend([header, "", entries, ""])

        merged_new = "\n".join(parts)
        if not merged_new.endswith("\n\n"):
            merged_new = merged_new.rstrip("\n") + "\n\n"

        return merged_new + existing_without_unreleased

    def _parse_version_section(
        self, content: str
    ) -> tuple[str, list[tuple[str, str]]]:
        lines = content.split("\n")
        header_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("## "):
                header_idx = i
                break

        version_header = lines[header_idx]

        # Truncate at any subsequent version header to avoid merging
        # sections when git-cliff produces duplicate `## [...]` blocks.
        body_lines = lines[header_idx + 1 :]
        truncate_at = len(body_lines)
        for i, line in enumerate(body_lines):
            if line.startswith("## "):
                truncate_at = i
                break
        body = "\n".join(body_lines[:truncate_at]).strip()

        groups = self._parse_groups(body) if body else []
        return version_header, groups

    def _parse_groups(self, body: str) -> list[tuple[str, str]]:
        parts = re.split(r"(?=^### )", body, flags=re.MULTILINE)
        groups: list[tuple[str, str]] = []
        for part in parts:
            part = part.strip()
            if not part:
                continue
            lines = part.split("\n")
            header = lines[0]
            entries = "\n".join(lines[1:]).strip()
            groups.append((header, entries))
        return groups

    def _parse_output(self, raw: str) -> list[str]:
        return [line.strip() for line in raw.splitlines() if line.strip()]
