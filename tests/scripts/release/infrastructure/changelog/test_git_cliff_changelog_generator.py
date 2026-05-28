from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, create_autospec, patch

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


@pytest.mark.unit
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
        assert "--" not in cmd
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
        assert "--" not in cmd

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

    async def test_future_version_returns_full_history(
        self, scenario_repo_with_multiple_tags: Scenario
    ) -> None:
        scenario = scenario_repo_with_multiple_tags
        response = await _make_generator(scenario.repo).generate(
            ChangelogRequest(from_version=scenario.from_version),
        )

        full = "\n".join(response.entries)
        assert "Initial scaffold" in full
        assert "Add user registration" in full
        assert "Prevent duplicate emails" in full
        assert "Add password reset" in full
        assert "Handle expired tokens" in full
        assert "[0.3.0]" in full
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
        assert "add password reset" in content_after
        assert "handle expired tokens" in content_after

        section_030 = content_after.split("## [0.2.0]")[0]
        section_020_and_below = content_after.split("## [0.2.0]")[1]

        assert "## [0.3.0]" in section_030
        assert "add password reset" in section_030
        assert "handle expired tokens" in section_030
        assert section_020_and_below.count("add password reset") == 0
        assert section_020_and_below.count("handle expired tokens") == 0
        assert content_after.count("add password reset") == 1
        assert content_after.count("handle expired tokens") == 1
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

    async def test_git_cliff_not_installed_raises_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)

        generator = GitCliffChangelogGenerator(
            runner=SubprocessCommandRunner(),
            changelog_path=tmp_path / "CHANGELOG.md",
        )

        original_run = subprocess.run

        def mock_run(
            args: list[str],
            **kwargs: object,
        ) -> subprocess.CompletedProcess[str]:
            if args[0] == "git-cliff":
                raise FileNotFoundError(
                    "[Errno 2] No such file or directory: 'git-cliff'"
                )
            return original_run(args, **kwargs)  # type: ignore[return-value]

        with patch("subprocess.run", side_effect=mock_run):
            with pytest.raises(
                ChangelogGenerationError,
                match="git-cliff is not installed or not found in PATH",
            ):
                await generator.generate(ChangelogRequest(from_version="1.0.0"))
