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

        raw = self._run_git_cliff(range_arg, version_tag)
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

        When the requested tag doesn't exist yet (i.e. a new release), we
        return ``None`` for the range so that git-cliff produces the full
        history across all existing tags — ensuring the released version
        section is populated and the ``[Unreleased]`` block is replaced.
        """
        if tag_exists:
            return requested_tag, requested_tag
        return None, requested_tag

    def _run_git_cliff(self, from_tag: str | None, version_tag: str | None) -> str:
        cmd = ["git-cliff", "--output", "-"]

        if version_tag:
            cmd += ["--tag", version_tag]

        if from_tag:
            cmd += ["--", f"{from_tag}.."]

        try:
            new_entries = self._runner.run(cmd, check=True)
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
        for group_match in re.finditer(
            r"(### \w[^\n]*\n)(.*?)(?=### |\Z)", unreleased_content, re.DOTALL
        ):
            group_header = group_match.group(1).strip()
            group_entries = group_match.group(2).strip()
            if not group_entries:
                continue

            if re.search(re.escape(group_header), versioned_block):
                existing_group = re.search(
                    re.escape(group_header) + r"\n(.*?)(?=### |\Z)",
                    versioned_block,
                    re.DOTALL,
                )
                merged_entries = (
                    (existing_group.group(1) if existing_group else "")
                    + group_entries
                    + "\n"
                )
                versioned_block = re.sub(
                    re.escape(group_header),
                    group_header + "\n" + merged_entries,
                    versioned_block,
                )
            else:
                insert_pos = versioned_block.find("\n\n## [")
                if insert_pos == -1:
                    versioned_block += "\n\n" + group_header + "\n" + group_entries + "\n"
                else:
                    versioned_block = (
                        versioned_block[:insert_pos]
                        + "\n\n"
                        + group_header
                        + "\n"
                        + group_entries
                        + "\n"
                        + versioned_block[insert_pos:]
                    )

        return versioned_block

    def _parse_output(self, raw: str) -> list[str]:
        return [line.strip() for line in raw.splitlines() if line.strip()]
