from __future__ import annotations

import re
from pathlib import Path
from unittest.mock import MagicMock, create_autospec

import pytest
from scripts.release.application.ports.outbound import ChangelogRequest
from scripts.release.infrastructure.changelog.git_cliff_changelog_generator import (
    GitCliffChangelogGenerator,
)
from scripts.release.infrastructure.commons.process import CommandRunner, SubprocessCommandRunner
from tests.fixtures.git_cliff_scenarios import Scenario
from tests.fixtures.git_test_repository import GitTestRepository

from scripts.release.application.errors import ChangelogGenerationError


def _make_generator(repo: GitTestRepository) -> GitCliffChangelogGenerator:
    return GitCliffChangelogGenerator(
        runner=repo.scoped_runner(),
        changelog_path=repo.path / "CHANGELOG.md",
    )


def _read_changelog(scenario: Scenario) -> str:
    return scenario.changelog_path.read_text(encoding="utf-8")


@pytest.mark.integration
class TestGitCliffChangelogGeneratorUnit:
    @pytest.fixture
    def runner_mock(self) -> MagicMock:
        return create_autospec(CommandRunner, instance=True)

    @pytest.fixture
    def changelog_path(self, tmp_path: Path) -> Path:
        return tmp_path / "CHANGELOG.md"

    @pytest.fixture
    def generator(
        self,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> GitCliffChangelogGenerator:
        return GitCliffChangelogGenerator(runner=runner_mock, changelog_path=changelog_path)

    async def test_generate_uses_requested_tag_as_range_when_it_exists(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        changelog_path.write_text("## v0.9.0\n- old entry\n", encoding="utf-8")
        runner_mock.run.side_effect = [
            "abc123",
            "## v1.0.0\n- new entry\n",
        ]

        await generator.generate(ChangelogRequest(from_version="1.0.0"))

        git_cliff_call = runner_mock.run.call_args_list[1]
        cmd = git_cliff_call[0][0]
        assert "--output" in cmd
        assert "-" in cmd
        assert "--tag" in cmd
        assert "v1.0.0" in cmd
        assert "v1.0.0.." in cmd[-1]

    async def test_generate_uses_full_history_when_requested_tag_missing(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        changelog_path.write_text("## v0.9.0\n- old entry\n", encoding="utf-8")
        runner_mock.run.side_effect = [
            RuntimeError("not found"),
            "## v1.1.0\n- new entry\n",
        ]

        await generator.generate(ChangelogRequest(from_version="1.1.0"))

        git_cliff_call = runner_mock.run.call_args_list[1]
        cmd = git_cliff_call[0][0]
        assert "--unreleased" in cmd
        assert "v1.1.0" in cmd

    async def test_generate_produces_full_history_when_no_tags_exist(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        changelog_path.write_text("## v0.1.0\n- old entry\n", encoding="utf-8")
        runner_mock.run.side_effect = [
            RuntimeError("not found"),
            "## v0.1.0\n- full history\n",
        ]

        await generator.generate(ChangelogRequest(from_version="0.1.0"))

        git_cliff_call = runner_mock.run.call_args_list[1]
        cmd = git_cliff_call[0][0]
        assert "--unreleased" in cmd

    async def test_generate_returns_parsed_entries(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        changelog_path.write_text("", encoding="utf-8")
        runner_mock.run.side_effect = [
            "abc123",
            "## v1.0.0\n- feat: something\n",
        ]

        result = await generator.generate(ChangelogRequest(from_version="1.0.0"))

        assert result.entries == ["## v1.0.0", "- feat: something"]

    async def test_generate_returns_empty_entries_for_blank_cliff_output(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        changelog_path.write_text("", encoding="utf-8")
        runner_mock.run.side_effect = [
            "abc123",
            "\n\n",
        ]

        result = await generator.generate(ChangelogRequest(from_version="1.0.0"))

        assert result.entries == []

    async def test_generate_prepends_new_entries_to_existing_changelog(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        changelog_path.write_text("## v0.9.0\n- old entry\n", encoding="utf-8")
        runner_mock.run.side_effect = [
            "abc123",
            "## v1.0.0\n- feat: something\n",
        ]

        await generator.generate(ChangelogRequest(from_version="1.0.0"))

        content = changelog_path.read_text(encoding="utf-8")
        assert "## v1.0.0" in content
        assert "- feat: something" in content
        assert "## v0.9.0" in content
        assert "- old entry" in content
        assert content.index("## v1.0.0") < content.index("## v0.9.0")

    async def test_generate_creates_file_when_no_existing_changelog(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        runner_mock.run.side_effect = [
            "abc123",
            "## v1.0.0\n- feat: new\n",
        ]

        await generator.generate(ChangelogRequest(from_version="1.0.0"))

        assert changelog_path.exists()
        content = changelog_path.read_text(encoding="utf-8")
        assert "## v1.0.0" in content
        assert "- feat: new" in content

    async def test_generate_ensures_changelog_ends_with_newline(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        runner_mock.run.side_effect = [
            "abc123",
            "## v1.0.0\n- feat: no trailing newline",
        ]

        await generator.generate(ChangelogRequest(from_version="1.0.0"))

        assert changelog_path.read_text(encoding="utf-8").endswith("\n")

    async def test_generate_removes_unreleased_section_when_versioned_entries_prepended(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        changelog_path.write_text(
            "## [Unreleased]\n\n### Features\n- feature1\n\n## [0.3.22]\n- old entry\n",
            encoding="utf-8",
        )
        runner_mock.run.side_effect = [
            "abc123",
            "## [0.4.0] - 2026-05-28\n\n### Features\n- new feature\n",
        ]

        await generator.generate(ChangelogRequest(from_version="0.4.0"))

        content = changelog_path.read_text(encoding="utf-8")
        assert "## [0.4.0]" in content
        assert "## [Unreleased]" not in content
        assert "## [0.3.22]" in content

    async def test_generate_raises_changelog_generation_error_when_git_cliff_not_installed(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.side_effect = [
            "abc123",
            FileNotFoundError("git-cliff not found"),
        ]

        with pytest.raises(ChangelogGenerationError, match="not installed or not found"):
            await generator.generate(ChangelogRequest(from_version="1.0.0"))

    async def test_generate_raises_changelog_generation_error_when_git_cliff_fails(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.side_effect = [
            "abc123",
            RuntimeError("exit code 1"),
        ]

        with pytest.raises(ChangelogGenerationError, match="git-cliff failed"):
            await generator.generate(ChangelogRequest(from_version="1.0.0"))

    async def test_merge_preserves_blank_line_between_existing_and_new_entries(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        changelog_path.write_text(
            "## [Unreleased]\n\n"
            "### Features\n\n"
            "- **auth**: add password reset\n\n"
            "## [0.3.0] - 2026-03-24\n",
            encoding="utf-8",
        )
        runner_mock.run.side_effect = [
            "abc123",
            "## [0.4.0] - 2026-05-28\n\n### Features\n\n- **auth**: new feature\n\n",
        ]

        await generator.generate(ChangelogRequest(from_version="0.4.0"))

        content = changelog_path.read_text(encoding="utf-8")
        features_block = content.split("## [0.3.0]")[0]
        assert re.search(
            r"- \*\*auth\*\*: new feature\n\n- \*\*auth\*\*: add password reset\n\n",
            features_block,
        ), "Blank line missing between existing and new entries"

    async def test_inserted_group_has_blank_line_after_header(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        changelog_path.write_text(
            "## [Unreleased]\n\n"
            "### Documentation\n\n"
            "- **docs**: update README\n\n"
            "## [0.3.0] - 2026-03-24\n",
            encoding="utf-8",
        )
        runner_mock.run.side_effect = [
            "abc123",
            "## [0.4.0] - 2026-05-28\n\n### Features\n\n- **auth**: new feature\n\n",
        ]

        await generator.generate(ChangelogRequest(from_version="0.4.0"))

        content = changelog_path.read_text(encoding="utf-8")
        assert re.search(r"### Documentation\n\n", content), (
            "Blank line missing between ### Documentation and entries"
        )

    async def test_inserted_group_has_blank_line_before_next_section(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        changelog_path.write_text(
            "## [Unreleased]\n\n"
            "### Documentation\n\n"
            "- **docs**: update README\n\n"
            "## [0.3.0] - 2026-03-24\n",
            encoding="utf-8",
        )
        runner_mock.run.side_effect = [
            "abc123",
            "## [0.4.0] - 2026-05-28\n\n### Features\n\n- **auth**: new feature\n\n",
        ]

        await generator.generate(ChangelogRequest(from_version="0.4.0"))

        content = changelog_path.read_text(encoding="utf-8")
        assert re.search(r"- \*\*docs\*\*: update README\n\n+## \[0\.3\.0\]", content), (
            "Blank line missing between inserted group and next version header"
        )

    async def test_unreleased_group_not_in_versioned_inserted_correctly(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        changelog_path.write_text(
            "## [Unreleased]\n\n"
            "### Features\n\n"
            "- **auth**: add password reset\n\n"
            "### Documentation\n\n"
            "- **docs**: update README\n\n"
            "- **docs**: add contributing guide\n\n"
            "## [0.3.0] - 2026-03-24\n",
            encoding="utf-8",
        )
        runner_mock.run.side_effect = [
            "abc123",
            "## [0.4.0] - 2026-05-28\n\n"
            "### Features\n\n"
            "- **auth**: new feature\n\n"
            "### Bug Fixes\n\n"
            "- **auth**: fix bug\n\n",
        ]

        await generator.generate(ChangelogRequest(from_version="0.4.0"))

        content = changelog_path.read_text(encoding="utf-8")
        assert "### Documentation" in content
        assert "**docs**: update README" in content
        assert "**docs**: add contributing guide" in content
        assert "## [0.3.0]" in content

    async def test_unreleased_group_inserted_after_existing_groups(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        changelog_path.write_text(
            "## [Unreleased]\n\n"
            "### Documentation\n\n"
            "- **docs**: update README\n\n"
            "## [0.3.0] - 2026-03-24\n",
            encoding="utf-8",
        )
        runner_mock.run.side_effect = [
            "abc123",
            "## [0.4.0] - 2026-05-28\n\n"
            "### Features\n\n"
            "- **auth**: new feature\n\n"
            "### Bug Fixes\n\n"
            "- **auth**: fix bug\n\n",
        ]

        await generator.generate(ChangelogRequest(from_version="0.4.0"))

        content = changelog_path.read_text(encoding="utf-8")
        features_pos = content.index("### Features")
        bugfixes_pos = content.index("### Bug Fixes")
        doc_pos = content.index("### Documentation")
        assert features_pos < bugfixes_pos < doc_pos

    async def test_multiple_unreleased_groups_not_in_versioned_all_inserted(
        self,
        generator: GitCliffChangelogGenerator,
        runner_mock: MagicMock,
        changelog_path: Path,
    ) -> None:
        changelog_path.write_text(
            "## [Unreleased]\n\n"
            "### Features\n\n"
            "- **auth**: add password reset\n\n"
            "### Documentation\n\n"
            "- **docs**: update README\n\n"
            "### Testing\n\n"
            "- **test**: add tests\n\n"
            "## [0.3.0] - 2026-03-24\n",
            encoding="utf-8",
        )
        runner_mock.run.side_effect = [
            "abc123",
            "## [0.4.0] - 2026-05-28\n\n### Features\n\n- **auth**: new feature\n\n",
        ]

        await generator.generate(ChangelogRequest(from_version="0.4.0"))

        content = changelog_path.read_text(encoding="utf-8")
        assert "### Documentation" in content
        assert "### Testing" in content
        assert "**docs**: update README" in content
        assert "**test**: add tests" in content


@pytest.mark.integration
class TestGitCliffChangelogGeneratorIntegration:
    async def test_empty_repo_generates_versioned_section(
        self, scenario_empty_repo: Scenario
    ) -> None:
        scenario = scenario_empty_repo
        response = await _make_generator(scenario.repo).generate(
            ChangelogRequest(from_version=scenario.from_version),
        )

        full = "\n".join(response.entries)
        assert "[0.1.0]" in full
        assert scenario.changelog_path.exists()

    async def test_existing_tag_returns_only_commits_after_it(
        self, scenario_repo_with_single_tag: Scenario
    ) -> None:
        scenario = scenario_repo_with_single_tag
        response = await _make_generator(scenario.repo).generate(
            ChangelogRequest(from_version=scenario.from_version),
        )

        full = "\n".join(response.entries)
        assert "Resolve off-by-one error" in full
        assert "Update README" in full
        assert "Add hello function" not in full
        assert "[0.1.0]" in full
        assert "unreleased" not in full.lower()
        assert scenario.changelog_path.exists()

    async def test_future_version_returns_unreleased_commits(
        self, scenario_repo_with_multiple_tags: Scenario
    ) -> None:
        scenario = scenario_repo_with_multiple_tags
        response = await _make_generator(scenario.repo).generate(
            ChangelogRequest(from_version=scenario.from_version),
        )

        full = "\n".join(response.entries)
        assert "Add password reset" in full
        assert "Handle expired tokens" in full
        assert "[0.3.0]" in full
        assert "Initial scaffold" not in full
        assert "Add user registration" not in full
        assert scenario.changelog_path.exists()

    async def test_replaces_unreleased_block_with_versioned_section(
        self, scenario_changelog_with_unreleased: Scenario
    ) -> None:
        scenario = scenario_changelog_with_unreleased

        content_before = _read_changelog(scenario)
        assert "## [Unreleased]" in content_before

        await _make_generator(scenario.repo).generate(
            ChangelogRequest(from_version=scenario.from_version),
        )

        content_after = _read_changelog(scenario)
        assert "## [0.3.0]" in content_after
        assert "## [Unreleased]" not in content_after
        assert "## [0.2.0]" in content_after
        assert "## [0.1.0]" in content_after

    async def test_release_merges_unreleased_content_into_versioned_section(
        self, scenario_changelog_with_unreleased: Scenario
    ) -> None:
        scenario = scenario_changelog_with_unreleased

        content_before = _read_changelog(scenario)
        assert "add password reset" in content_before
        assert "handle expired tokens" in content_before

        await _make_generator(scenario.repo).generate(
            ChangelogRequest(from_version=scenario.from_version),
        )

        content_after = _read_changelog(scenario)
        assert "## [Unreleased]" not in content_after
        assert "## [0.3.0]" in content_after

        section_030 = content_after.split("## [0.2.0]")[0].lower()
        section_020_and_below = content_after.split("## [0.2.0]")[1].lower()

        assert "password reset" in section_030
        assert "expired tokens" in section_030
        assert "oauth2" in section_030
        assert "rate limiting" in section_030
        assert section_020_and_below.count("password reset") == 0
        assert section_020_and_below.count("expired tokens") == 0
        assert section_020_and_below.count("oauth2") == 0
        assert section_020_and_below.count("rate limiting") == 0
        assert "## [0.2.0]" in content_after
        assert "## [0.1.0]" in content_after

    async def test_prepends_to_existing_changelog_without_unreleased(
        self, scenario_existing_changelog_no_unreleased: Scenario
    ) -> None:
        scenario = scenario_existing_changelog_no_unreleased

        content_before = _read_changelog(scenario)
        assert "## [Unreleased]" not in content_before

        await _make_generator(scenario.repo).generate(
            ChangelogRequest(from_version=scenario.from_version),
        )

        content_after = _read_changelog(scenario)
        assert "## [0.3.0]" in content_after
        assert "## [Unreleased]" not in content_after
        assert "## [0.2.0]" in content_after
        assert "## [0.1.0]" in content_after
        assert content_after.index("## [0.3.0]") < content_after.index("## [0.2.0]")

    async def test_creates_changelog_when_file_does_not_exist(
        self, scenario_repo_with_single_tag: Scenario
    ) -> None:
        scenario = scenario_repo_with_single_tag
        assert not scenario.changelog_path.exists()

        await _make_generator(scenario.repo).generate(
            ChangelogRequest(from_version=scenario.from_version),
        )

        assert scenario.changelog_path.exists()
        content = _read_changelog(scenario)
        assert "## [0.1.0]" in content
        assert content.endswith("\n")

    async def test_conventional_commits_grouped_correctly(
        self, scenario_repo_with_multiple_tags: Scenario
    ) -> None:
        scenario = scenario_repo_with_multiple_tags

        response = await _make_generator(scenario.repo).generate(
            ChangelogRequest(from_version=scenario.from_version),
        )

        full = "\n".join(response.entries)
        assert "### Features" in full
        assert "### Bug Fixes" in full

    async def test_not_a_git_repo_raises_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)

        generator = GitCliffChangelogGenerator(
            runner=SubprocessCommandRunner(),
            changelog_path=tmp_path / "CHANGELOG.md",
        )

        with pytest.raises(ChangelogGenerationError, match="git-cliff failed"):
            await generator.generate(ChangelogRequest(from_version="1.0.0"))

    async def test_generate_when_dry_run_false_then_mutates_changelog(
        self, scenario_changelog_with_unreleased: Scenario
    ) -> None:
        scenario = scenario_changelog_with_unreleased
        content_before = _read_changelog(scenario)

        response = await _make_generator(scenario.repo).generate(
            ChangelogRequest(from_version=scenario.from_version, dry_run=False),
        )

        assert response.entries
        full = "\n".join(response.entries)
        assert "[0.3.0]" in full

        content_after = _read_changelog(scenario)
        assert content_after != content_before
        assert "## [Unreleased]" not in content_after
        assert "## [0.3.0]" in content_after

    async def test_generate_when_dry_run_true_then_does_not_mutate_changelog(
        self, scenario_changelog_with_unreleased: Scenario
    ) -> None:
        scenario = scenario_changelog_with_unreleased
        content_before = _read_changelog(scenario)

        response = await _make_generator(scenario.repo).generate(
            ChangelogRequest(from_version=scenario.from_version, dry_run=True),
        )

        assert response.entries
        full = "\n".join(response.entries)
        assert "[0.3.0]" in full

        content_after = _read_changelog(scenario)
        assert content_after == content_before
        assert "## [Unreleased]" in content_after

    async def test_generate_when_called_twice_with_same_version_then_does_not_duplicate_sections(
        self, scenario_changelog_with_unreleased: Scenario
    ) -> None:
        scenario = scenario_changelog_with_unreleased
        generator = _make_generator(scenario.repo)

        await generator.generate(
            ChangelogRequest(from_version=scenario.from_version, dry_run=False),
        )
        content_after_first = _read_changelog(scenario)

        await generator.generate(
            ChangelogRequest(from_version=scenario.from_version, dry_run=False),
        )
        content_after_second = _read_changelog(scenario)

        assert "## [0.3.0]" in content_after_first
        assert content_after_second.count("## [0.3.0]") == 1

    async def test_generate_when_same_version_exists_with_different_date_then_does_not_duplicate(
        self, scenario_repo_with_multiple_tags: Scenario
    ) -> None:
        scenario = scenario_repo_with_multiple_tags
        generator = _make_generator(scenario.repo)

        old_changelog = (
            "## [0.3.0] - 2000-01-01\n\n"
            "### Features\n\n"
            "- old entry\n\n"
            "## [0.2.0] - 2026-01-15\n\n"
            "### Features\n\n"
            "- **core**: add user registration\n\n"
        )
        scenario.changelog_path.write_text(old_changelog, encoding="utf-8")

        await generator.generate(
            ChangelogRequest(from_version=scenario.from_version, dry_run=False),
        )

        content = _read_changelog(scenario)
        assert content.count("## [0.3.0]") == 1
