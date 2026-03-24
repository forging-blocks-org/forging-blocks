import os
import subprocess
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
from scripts.release.application.ports.inbound import (
    PrepareReleaseInput,
)
from scripts.release.application.ports.outbound.changelog_generator import ChangelogRequest
from scripts.release.application.services.open_release_pull_request_service import (
    OpenReleasePullRequestService,
)
from scripts.release.application.services.prepare_release_service import (
    PrepareReleaseService,
)
from scripts.release.domain.commands import OpenPullRequestCommand
from scripts.release.domain.value_objects.release_branch_name import ReleaseBranchName
from scripts.release.infrastructure.bus.in_memory_release_command_bus import (
    InMemoryReleaseCommandBus,
)
from scripts.release.infrastructure.changelog.git_cliff_changelog_generator import (
    GitCliffChangelogGenerator,
)
from scripts.release.infrastructure.git.git_version_control import GitVersionControl
from scripts.release.infrastructure.handlers.open_pull_request_handler import OpenPullRequestHandler
from scripts.release.infrastructure.transactions.in_memory_release_transaction import (
    InMemoryReleaseTransaction,
)
from scripts.release.infrastructure.versioning.poetry_versioning_service import (
    PoetryVersioningService,
)


def subprocess_run(*args, **kwargs):
    return subprocess.run(*args, **kwargs)


def create_bare_remote(tmp_path: Path, name: str = "remote.git") -> Path:
    remote_path = tmp_path / name
    subprocess_run(["git", "init", "--bare", str(remote_path)], check=True)
    return remote_path


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


@pytest.fixture
def git_repo_with_poetry(tmp_path: Path, git_repo):
    create_pyproject_toml(git_repo.path)

    subprocess_run(
        ["git", "add", "pyproject.toml"],
        cwd=git_repo.path,
        check=True,
    )
    subprocess_run(
        ["git", "commit", "-m", "Add pyproject.toml"],
        cwd=git_repo.path,
        check=True,
    )

    remote_path = create_bare_remote(tmp_path)

    subprocess_run(
        ["git", "remote", "add", "origin", str(remote_path)],
        cwd=git_repo.path,
        check=True,
    )

    subprocess_run(
        ["git", "push", "-u", "origin", "main"],
        cwd=git_repo.path,
        check=True,
    )

    return git_repo


@pytest.fixture
def version_control(git_repo_with_poetry):
    return GitVersionControl(git_repo_with_poetry.scoped_runner())


@pytest.fixture
def versioning_service(git_repo_with_poetry):
    return PoetryVersioningService(git_repo_with_poetry.scoped_runner())


@pytest.fixture
def changelog_generator(git_repo_with_poetry):
    return GitCliffChangelogGenerator(git_repo_with_poetry.scoped_runner())


@pytest.fixture
async def message_bus(git_repo_with_poetry):
    bus = InMemoryReleaseCommandBus()

    pull_request_service = MagicMock()
    pull_request_service.open = MagicMock()

    open_pr_service = OpenReleasePullRequestService(
        pull_request_service=pull_request_service,
    )

    handler = OpenPullRequestHandler(open_pr_service)

    await bus.register(OpenPullRequestCommand, handler)

    return bus


@pytest.fixture
def transaction():
    return InMemoryReleaseTransaction()


@pytest.fixture
async def service(
    version_control,
    versioning_service,
    changelog_generator,
    message_bus,
    transaction,
):
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
    async def test_execute_creates_release_branch(
        self,
        service,
        version_control,
        git_repo,
    ) -> None:
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        request = PrepareReleaseInput(level="minor", dry_run=False)

        await service.execute(request)

        assert version_control.branch_exists(ReleaseBranchName("release/v0.1.0"))

    async def test_execute_updates_pyproject_version(
        self,
        service,
        git_repo_with_poetry,
    ) -> None:
        git_repo_with_poetry.write_file("README.md", "# Test Project")
        git_repo_with_poetry.commit("Initial commit")

        request = PrepareReleaseInput(level="minor", dry_run=False)

        await service.execute(request)

        pyproject = (git_repo_with_poetry.path / "pyproject.toml").read_text()

        assert 'version = "0.1.0"' in pyproject

    async def test_execute_generates_changelog(
        self,
        changelog_generator,
        git_repo,
    ) -> None:
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")
        git_repo.write_file("CHANGELOG.md", "")
        git_repo.commit("Add changelog")

        result = await changelog_generator.generate(ChangelogRequest(from_version="0.0.0"))

        assert result is not None
        assert hasattr(result, "entries")

    async def test_execute_generates_changelog_with_correct_version(
        self,
        git_repo_with_poetry,
    ) -> None:
        git_repo_with_poetry.write_file("README.md", "# Test Project")
        git_repo_with_poetry.commit("feat: initial feature")

        generator = GitCliffChangelogGenerator(
            runner=git_repo_with_poetry.scoped_runner(),
            changelog_path=git_repo_with_poetry.path / "CHANGELOG.md",
        )

        result = await generator.generate(ChangelogRequest(from_version="0.1.0"))

        full_output = "\n".join(result.entries)

        assert "[0.1.0]" in full_output
        assert "unreleased" not in full_output.lower()
        assert (git_repo_with_poetry.path / "CHANGELOG.md").exists()

    async def test_execute_pushes_branch(
        self,
        service,
        git_repo,
    ) -> None:
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

    async def test_execute_checks_out_release_branch(
        self,
        service,
        git_repo,
    ) -> None:
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        request = PrepareReleaseInput(level="minor", dry_run=False)

        await service.execute(request)

        current_branch = subprocess_run(
            ["git", "branch", "--show-current"],
            cwd=git_repo.path,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        assert current_branch == "release/v0.1.0"

    async def test_execute_sends_pr_command(
        self,
        service,
        message_bus,
        git_repo,
    ) -> None:
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        request = PrepareReleaseInput(level="minor", dry_run=False)

        original_send = message_bus.send
        message_bus.send = AsyncMock(wraps=original_send)

        await service.execute(request)

        message_bus.send.assert_awaited()

        assert any(
            isinstance(call.args[0], OpenPullRequestCommand)
            for call in message_bus.send.await_args_list
        )

    async def test_execute_is_idempotent_when_branch_exists(
        self,
        service,
        git_repo,
    ) -> None:
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        request = PrepareReleaseInput(level="minor", dry_run=False)

        await service.execute(request)
        await service.execute(request)

        branches = subprocess_run(
            ["git", "branch"],
            cwd=git_repo.path,
            capture_output=True,
            text=True,
            check=True,
        ).stdout

        assert branches.count("release/v0.1.0") == 1

    async def test_dry_run_does_not_make_changes(
        self,
        service,
        git_repo,
    ) -> None:
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
            text=True,
            check=True,
        ).stdout

        assert initial_branches == final_branches

    async def test_rollback_when_push_fails(
        self,
        service,
        version_control,
        git_repo,
    ) -> None:
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        version_control.push = MagicMock(side_effect=RuntimeError("Push failed"))

        request = PrepareReleaseInput(level="minor", dry_run=False)

        with pytest.raises(RuntimeError, match="Push failed"):
            await service.execute(request)

    async def test_rollback_when_commit_fails(
        self,
        service,
        version_control,
        git_repo,
    ) -> None:
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        original_commit = version_control.commit_release_artifacts
        count = {"n": 0}

        def failing_commit():
            count["n"] += 1
            if count["n"] == 1:
                raise RuntimeError("Commit failed")
            return original_commit()

        version_control.commit_release_artifacts = failing_commit

        request = PrepareReleaseInput(level="minor", dry_run=False)

        with pytest.raises(RuntimeError, match="Commit failed"):
            await service.execute(request)

    async def test_rollback_when_changelog_fails(
        self,
        service,
        git_repo,
    ) -> None:
        git_repo.write_file("README.md", "# Test Project")
        git_repo.commit("Initial commit")

        service._changelog_generator.generate = AsyncMock(
            side_effect=RuntimeError("Changelog generation failed")
        )

        request = PrepareReleaseInput(level="minor", dry_run=False)

        with pytest.raises(RuntimeError, match="Changelog generation failed"):
            await service.execute(request)
