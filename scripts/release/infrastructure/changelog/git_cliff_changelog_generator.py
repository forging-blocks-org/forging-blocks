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

        return ChangelogResponse(entries=entries, raw=raw)

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

        When the requested tag doesn't exist yet (i.e. a new release), we
        return ``None`` for the range so that git-cliff produces the full
        history across all existing tags — ensuring the released version
        section is populated and the ``[Unreleased]`` block is replaced.
        """
        if tag_exists:
            return requested_tag, requested_tag
        return None, requested_tag

    def _run_git_cliff(
        self, from_tag: str | None, version_tag: str | None, *, dry_run: bool = False
    ) -> str:
        cmd = ["git-cliff", "--output", "-"]

        if version_tag:
            cmd += ["--tag", version_tag]

        if from_tag:
            cmd += ["--", f"{from_tag}.."]

        try:
            new_entries = self._runner.run(cmd, check=True)
            if not dry_run:
                self._write_changelog(new_entries)
            return new_entries
        except FileNotFoundError as exc:
            raise ChangelogGenerationError(
                "git-cliff is not installed or not found in PATH"
            ) from exc
        except RuntimeError as exc:
            raise ChangelogGenerationError(f"git-cliff failed: {exc}") from exc

    def _write_changelog(self, new_entries: str) -> None:
        """Prepend *new_entries* to the existing changelog file.

        If the file already exists the new section is inserted at the top;
        otherwise the file is created with only the new content.

        When the new entries contain a versioned section (e.g. ``## [0.4.0]``),
        the ``## [Unreleased]`` block from the existing content is merged
        into the new versioned section so that unreleased changes are not lost.
        """
        existing = ""
        if self._changelog_path.exists():
            existing = self._changelog_path.read_text(encoding="utf-8")

        new_block = new_entries.rstrip("\n")

        is_versioned = re.search(r"^## \[\d+\.\d+", new_block, re.MULTILINE)
        if is_versioned and existing:
            unreleased_content = self._extract_unreleased(existing)
            existing = self._strip_unreleased(existing)

            if unreleased_content:
                new_block = self._merge_unreleased_into_versioned(
                    new_block, unreleased_content
                )

        if existing.strip():
            combined = new_block + "\n\n" + existing
        else:
            combined = new_block + "\n"

        self._changelog_path.write_text(combined, encoding="utf-8")

    def _extract_unreleased(self, changelog: str) -> str:
        match = re.search(
            r"^## \[Unreleased\]\s*\n(.*?)(?=^## \[|\Z)",
            changelog,
            re.MULTILINE | re.DOTALL,
        )
        return match.group(1).strip() if match else ""

    def _strip_unreleased(self, changelog: str) -> str:
        return re.sub(
            r"^## \[Unreleased\].*?(?=^## \[|\Z)",
            "",
            changelog,
            flags=re.MULTILINE | re.DOTALL,
        ).lstrip("\n")

    def _merge_unreleased_into_versioned(
        self, versioned_block: str, unreleased_content: str
    ) -> str:
        first_section_end = re.search(r"^## \[", versioned_block[2:], re.MULTILINE)
        section_end = first_section_end.start() + 2 if first_section_end else len(versioned_block)
        first_section = versioned_block[:section_end]
        rest = versioned_block[section_end:]

        for group_match in re.finditer(
            r"(### \w[^\n]*\n)(.*?)(?=### |\Z)", unreleased_content, re.DOTALL
        ):
            group_header = group_match.group(1).strip()
            group_entries = group_match.group(2).strip()
            if not group_entries:
                continue

            existing_pattern = (
                re.escape(group_header)
                + r"\n(.*?)(?=### |\Z)"
            )
            existing_match = re.search(existing_pattern, first_section, re.DOTALL)

            if existing_match:
                existing_entries = existing_match.group(1)
                existing_normalized = {
                    self._normalize_entry(line.strip())
                    for line in existing_entries.strip().splitlines()
                    if line.strip().startswith("- ")
                }
                new_lines = [
                    line
                    for line in group_entries.splitlines()
                    if line.strip().startswith("- ")
                    and self._normalize_entry(line.strip())
                    not in existing_normalized
                ]
                if new_lines:
                    merged_entries = (
                        existing_entries.rstrip("\n")
                        + "\n\n"
                        + "\n\n".join(new_lines)
                        + "\n\n"
                    )
                    replacement = group_header + "\n" + merged_entries
                    first_section = (
                        first_section[: existing_match.start()]
                        + replacement
                        + first_section[existing_match.end() :]
                    )
            else:
                insert_pos = re.search(r"^## \[", first_section[2:], re.MULTILINE)
                if insert_pos:
                    pos = insert_pos.start() + 2
                    remaining = first_section[pos:].lstrip("\n")
                    first_section = (
                        first_section[:pos]
                        + "\n\n"
                        + group_header
                        + "\n\n"
                        + group_entries
                        + "\n\n"
                        + remaining
                    )
                else:
                    first_section += (
                        "\n" + group_header + "\n\n" + group_entries + "\n\n"
                    )

        return first_section + rest

    def _parse_output(self, raw: str) -> list[str]:
        return [line.strip() for line in raw.splitlines() if line.strip()]

    def _normalize_entry(self, entry: str) -> str:
        normalized = re.sub(r"^\- \*\*\w+\*\*:?\s*", "- ", entry)
        return normalized.lower().strip()
