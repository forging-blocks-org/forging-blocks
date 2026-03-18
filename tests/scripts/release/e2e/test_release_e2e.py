from __future__ import annotations

import os
from pathlib import Path
from subprocess import run as subprocess_run
from unittest.mock import AsyncMock, MagicMock

import pytest
from scripts.release.application.ports.inbound import PrepareReleaseInput
from scripts.release.application.ports.outbound import ChangelogRequest
from scripts.release.application.services.open_release_pull_request_service import (
    OpenReleasePullRequestService,
)
from scripts.release.application.services.prepare_release_service import (
    PrepareReleaseService,
)
from scripts.release.infrastructure.bus.in_memory_release_command_bus import (
    InMemoryReleaseCommandBus,
)
from scripts.release.infrastructure.changelog.git_cliff_changelog_generator import (
    GitCliffChangelogGenerator,
)
from scripts.release.infrastructure.git.git_version_control import GitVersionControl
from scripts.release.infrastructure.transactions.in_memory_release_transaction import (
    InMemoryReleaseTransaction,
)
from scripts.release.infrastructure.versioning.poetry_versioning_service import (
    PoetryVersioningService,
)
from tests.fixtures.git_test_repository import GitTestRepository

from scripts.release.domain.messages import OpenPullRequestCommand
from scripts.release.domain.value_objects import ReleaseBranchName, TagName
from scripts.release.infrastructure.handlers import OpenPullRequestHandler


def create_pyproject_toml(path: Path, version: str = "0.0.0") -> None:
    """Create a minimal pyproject.toml for poetry."""
    pyproject_content = f"""[tool.poetry]
name = "test-project"
version = "{version}"
description = "Test project"
authors = ["Test <test@test.com>"]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
    (path / "pyproject.toml").write_text(pyproject_content)


def create_bare_remote(tmp_path: Path, name: str = "remote.git") -> Path:
    """Create a bare git repository to act as remote."""
    remote_path = tmp_path / name
    subprocess_run(["git", "init", "--bare", str(remote_path)], check=True)
    return remote_path


@pytest.fixture
def git_repo_with_poetry(tmp_path: Path, git_repo: GitTestRepository) -> GitTestRepository:
    """Extends git_repo fixture with pyproject.toml and remote for e2e tests."""
    create_pyproject_toml(git_repo.path)
    subprocess_run(["git", "add", "pyproject.toml"], cwd=git_repo.path, check=True)
    subprocess_run(["git", "commit", "-m", "Add pyproject.toml"], cwd=git_repo.path, check=True)

    remote_path = create_bare_remote(tmp_path)
    subprocess_run(
        ["git", "remote", "add", "origin", str(remote_path)], cwd=git_repo.path, check=True
    )
    subprocess_run(["git", "push", "-u", "origin", "main"], cwd=git_repo.path, check=True)

    return git_repo


@pytest.fixture
def version_control(git_repo_with_poetry: GitTestRepository) -> GitVersionControl:
    return GitVersionControl(git_repo_with_poetry.scoped_runner())


@pytest.fixture
def versioning_service(git_repo_with_poetry: GitTestRepository) -> PoetryVersioningService:
    return PoetryVersioningService(git_repo_with_poetry.scoped_runner())


@pytest.fixture
def changelog_generator(git_repo_with_poetry: GitTestRepository) -> GitCliffChangelogGenerator:
    return GitCliffChangelogGenerator(git_repo_with_poetry.scoped_runner())


@pytest.fixture
async def message_bus(git_repo_with_poetry: GitTestRepository) -> InMemoryReleaseCommandBus:
    bus = InMemoryReleaseCommandBus()
    pull_request_service = MagicMock()
    pull_request_service.open = MagicMock()
    open_pr_service = OpenReleasePullRequestService(pull_request_service=pull_request_service)
    handler = OpenPullRequestHandler(open_pr_service)

    await bus.register(OpenPullRequestCommand, handler)

    return bus


@pytest.fixture
def transaction() -> InMemoryReleaseTransaction:
    return InMemoryReleaseTransaction()


@pytest.fixture
async def service(
    version_control: GitVersionControl,
    versioning_service: PoetryVersioningService,
    changelog_generator: GitCliffChangelogGenerator,
    message_bus: InMemoryReleaseCommandBus,
    transaction: InMemoryReleaseTransaction,
) -> PrepareReleaseService:
    return PrepareReleaseService(
        versioning_service=versioning_service,
        version_control=version_control,
        transaction=transaction,
        message_bus=message_bus,
        changelog_generator=changelog_generator,
    )


@pytest.mark.skipif(
    not os.environ.get("RUN_E2E_TESTS"),
    reason="Set RUN_E2E_TESTS=1 to run E2E release workflow tests",
)
@pytest.mark.e2e
class TestReleaseWorkflow:
    """E2E tests for the release workflow.

    Current behavior:
    1. Stay on current branch (or release branch if exists)
    2. Create/checkout release branch
    3. Apply version (update pyproject.toml)
    4. Generate changelog
    5. Commit on release branch
    6. Push release branch
    7. Open PR from release branch to main
    """

    async def test_execute_with_flag_creates_release_branch(
        self,
        service: PrepareReleaseService,
        version_control: GitVersionControl,
        git_repo: GitTestRepository,
    ) -> None:
        """Test that release creates a release branch."""
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        request = PrepareReleaseInput(level="minor", dry_run=False)

        await service.execute(request)

        assert version_control.branch_exists(ReleaseBranchName("release/v0.1.0"))

    async def test_execute_with_flag_generates_changelog(
        self,
        changelog_generator: GitCliffChangelogGenerator,
        git_repo: GitTestRepository,
    ) -> None:
        """Test that release generates a changelog."""
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")
        git_repo.write_file("CHANGELOG.md", "")
        git_repo.commit("Add changelog")

        result = await changelog_generator.generate(ChangelogRequest(from_version="0.0.0"))

        assert result is not None
        assert hasattr(result, "entries")

    async def test_execute_with_flag_generates_changelog_with_correct_version(
        self,
        git_repo_with_poetry: GitTestRepository,
    ) -> None:
        """Test that changelog shows version (e.g. [0.1.0]) not 'unreleased'."""
        git_repo_with_poetry.write_file("README.md", "# Test Project")
        git_repo_with_poetry.commit("feat: initial feature")

        from scripts.release.infrastructure.changelog.git_cliff_changelog_generator import (
            GitCliffChangelogGenerator,
        )

        generator = GitCliffChangelogGenerator(
            runner=git_repo_with_poetry.scoped_runner(),
            changelog_path=git_repo_with_poetry.path / "CHANGELOG.md",
        )

        result = await generator.generate(ChangelogRequest(from_version="0.1.0"))

        full_output = "\n".join(result.entries)
        assert "[0.1.0]" in full_output
        assert "unreleased" not in full_output.lower()
        assert (git_repo_with_poetry.path / "CHANGELOG.md").exists()

    async def test_execute_with_flag_pushes_branch(
        self,
        service: PrepareReleaseService,
        git_repo: GitTestRepository,
    ) -> None:
        """Test that release pushes the branch to remote with tags."""
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        request = PrepareReleaseInput(level="minor", dry_run=False)

        await service.execute(request)

        branches = subprocess_run(
            ["git", "branch", "-r"],
            cwd=git_repo.path,
            capture_output=True,
            text=True,
            check=True,
        ).stdout

        assert "origin/release/v0.1.0" in branches

        # Verify that the release tag has also been pushed to the remote.
        remote_tag_output = subprocess_run(
            ["git", "ls-remote", "--tags", "origin", "v0.1.0"],
            cwd=git_repo.path,
            capture_output=True,
            text=True,
            check=True,
        ).stdout

        assert remote_tag_output.strip() != ""

    async def test_execute_with_flag_creates_tag(
        self,
        service: PrepareReleaseService,
        version_control: GitVersionControl,
        git_repo: GitTestRepository,
    ) -> None:
        """Test that release creates a tag."""
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        request = PrepareReleaseInput(level="minor", dry_run=False)

        await service.execute(request)

        assert version_control.tag_exists(TagName("v0.1.0"))

    async def test_execute_with_flag_sends_pr_command(
        self,
        service: PrepareReleaseService,
        message_bus: InMemoryReleaseCommandBus,
        git_repo: GitTestRepository,
    ) -> None:
        """Test that release sends the PR command."""
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        request = PrepareReleaseInput(level="minor", dry_run=False)

        # Spy on the message bus to ensure a PR command is actually sent.
        original_send = message_bus.send
        message_bus.send = AsyncMock(wraps=original_send)

        await service.execute(request)

        # Ensure that a command was sent through the bus.
        message_bus.send.assert_awaited()
        # Ensure that an OpenPullRequestCommand was among the sent commands.
        assert any(
            isinstance(call.args[0], OpenPullRequestCommand)
            for call in message_bus.send.await_args_list
        )

    async def test_dryrun_without_flag_does_not_make_git_changes(
        self,
        service: PrepareReleaseService,
        version_control: GitVersionControl,
        git_repo: GitTestRepository,
    ) -> None:
        """Test that dry-run mode does not make any git changes."""
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        initial_branches = subprocess_run(
            ["git", "branch", "-a"],
            cwd=git_repo.path,
            capture_output=True,
            text=True,
            check=True,
        ).stdout

        request = PrepareReleaseInput(level="minor", dry_run=True)

        await service.execute(request)

        final_branches = subprocess_run(
            ["git", "branch", "-a"],
            cwd=git_repo.path,
            capture_output=True,
            check=True,
            text=True,
        ).stdout

        assert initial_branches == final_branches

    async def test_rollback_when_push_fails_then_raises_error(
        self,
        service: PrepareReleaseService,
        version_control: GitVersionControl,
        git_repo: GitTestRepository,
    ) -> None:
        """Test that when push fails, an error is raised."""
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        version_control.push = MagicMock(side_effect=RuntimeError("Push failed"))

        request = PrepareReleaseInput(level="minor", dry_run=False)

        with pytest.raises(RuntimeError, match="Push failed"):
            await service.execute(request)

    async def test_rollback_when_commit_fails_then_raises_error(
        self,
        service: PrepareReleaseService,
        version_control: GitVersionControl,
        git_repo: GitTestRepository,
    ) -> None:
        """Test that when commit fails, an error is raised."""
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        original_commit = version_control.commit_release_artifacts
        commit_called = {"count": 0}

        def failing_commit():
            commit_called["count"] += 1
            if commit_called["count"] == 1:
                raise RuntimeError("Commit failed")
            return original_commit()

        version_control.commit_release_artifacts = failing_commit

        request = PrepareReleaseInput(level="minor", dry_run=False)

        with pytest.raises(RuntimeError, match="Commit failed"):
            await service.execute(request)

    async def test_rollback_when_changelog_fails_then_raises_error(
        self,
        service: PrepareReleaseService,
        git_repo: GitTestRepository,
    ) -> None:
        """Test that when changelog generation fails, an error is raised."""
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        service._changelog_generator.generate = AsyncMock(
            side_effect=RuntimeError("Changelog generation failed")
        )

        request = PrepareReleaseInput(level="minor", dry_run=False)

        with pytest.raises(RuntimeError, match="Changelog generation failed"):
            await service.execute(request)
