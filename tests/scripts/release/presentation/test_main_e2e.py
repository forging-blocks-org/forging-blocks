# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from __future__ import annotations

import os
from unittest.mock import MagicMock

import pytest
from scripts.release.application.ports.inbound import PrepareReleaseInput
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
from scripts.release.infrastructure.handlers.open_pull_request_handler import (
    OpenPullRequestHandler,
)
from scripts.release.infrastructure.transactions.in_memory_release_transaction import (
    InMemoryReleaseTransaction,
)
from scripts.release.infrastructure.versioning.poetry_versioning_service import (
    PoetryVersioningService,
)

from tests.fixtures.git_test_repository import GitTestRepository


@pytest.mark.skipif(
    not os.environ.get("RUN_E2E_TESTS"),
    reason="Set RUN_E2E_TESTS=1 to run E2E release workflow tests",
)
@pytest.mark.e2e
class TestMainE2E:
    """End-to-end tests for the release flow through the service layer.

    All infrastructure services are real (no mocks) except for the
    GitHub pull-request service which requires the ``gh`` CLI.
    """

    @pytest.fixture
    def git_repo_with_poetry(
        self, pyproject_toml: GitTestRepository, git_repo_with_remote: GitTestRepository
    ) -> GitTestRepository:
        return pyproject_toml

    @pytest.fixture
    def versioning_service(
        self, git_repo_with_poetry: GitTestRepository
    ) -> PoetryVersioningService:
        return PoetryVersioningService(runner=git_repo_with_poetry.scoped_runner())

    @pytest.fixture
    def version_control(
        self, git_repo_with_poetry: GitTestRepository
    ) -> GitVersionControl:
        return GitVersionControl(runner=git_repo_with_poetry.scoped_runner())

    @pytest.fixture
    def changelog_generator(
        self, git_repo_with_poetry: GitTestRepository
    ) -> GitCliffChangelogGenerator:
        return GitCliffChangelogGenerator(runner=git_repo_with_poetry.scoped_runner())

    @pytest.fixture
    def transaction(self) -> InMemoryReleaseTransaction:
        return InMemoryReleaseTransaction()

    @pytest.fixture
    async def service(
        self,
        versioning_service: PoetryVersioningService,
        version_control: GitVersionControl,
        changelog_generator: GitCliffChangelogGenerator,
        transaction: InMemoryReleaseTransaction,
        git_repo_with_poetry: GitTestRepository,
    ) -> PrepareReleaseService:
        bus = InMemoryReleaseCommandBus()
        pull_request_service = MagicMock()
        pull_request_service.open = MagicMock()
        open_pr_service = OpenReleasePullRequestService(
            pull_request_service=pull_request_service,
        )
        handler = OpenPullRequestHandler(open_pr_service)
        await bus.register(OpenPullRequestCommand, handler)

        return PrepareReleaseService(
            versioning_service=versioning_service,
            version_control=version_control,
            changelog_generator=changelog_generator,
            transaction=transaction,
            message_bus=bus,
        )

    async def test_execute_when_dry_run_false_then_mutates_files(
        self,
        service: PrepareReleaseService,
        git_repo_with_poetry: GitTestRepository,
    ) -> None:
        repo = git_repo_with_poetry
        repo.write_file("README.md", "# Test")
        repo.commit("feat: initial feature")

        await service.execute(PrepareReleaseInput(level="minor", dry_run=False))

        pyproject = (repo.path / "pyproject.toml").read_text(encoding="utf-8")
        assert 'version = "0.1.0"' in pyproject

        changelog_path = repo.path / "CHANGELOG.md"
        assert changelog_path.exists()

        assert service._version_control.branch_exists(
            ReleaseBranchName("release/v0.1.0")
        )

    async def test_execute_when_dry_run_true_then_does_not_mutate_files(
        self,
        service: PrepareReleaseService,
        git_repo_with_poetry: GitTestRepository,
    ) -> None:
        repo = git_repo_with_poetry
        repo.write_file("README.md", "# Test")
        repo.commit("feat: initial feature")

        pyproject_before = (repo.path / "pyproject.toml").read_text(encoding="utf-8")

        await service.execute(PrepareReleaseInput(level="minor", dry_run=True))

        pyproject_after = (repo.path / "pyproject.toml").read_text(encoding="utf-8")
        assert pyproject_after == pyproject_before

        assert not (repo.path / "CHANGELOG.md").exists()

    async def test_execute_when_not_dry_run_then_pushes_branch(
        self,
        service: PrepareReleaseService,
        git_repo_with_poetry: GitTestRepository,
        version_control: GitVersionControl,
    ) -> None:
        repo = git_repo_with_poetry
        repo.write_file("README.md", "# Test")
        repo.commit("feat: initial feature")

        await service.execute(PrepareReleaseInput(level="minor", dry_run=False))

        assert version_control.remote_branch_exists(
            ReleaseBranchName("release/v0.1.0")
        )

    async def test_execute_when_dry_run_true_then_does_not_push(
        self,
        service: PrepareReleaseService,
        git_repo_with_poetry: GitTestRepository,
        version_control: GitVersionControl,
    ) -> None:
        repo = git_repo_with_poetry
        repo.write_file("README.md", "# Test")
        repo.commit("feat: initial feature")

        await service.execute(PrepareReleaseInput(level="minor", dry_run=True))

        assert not version_control.branch_exists(
            ReleaseBranchName("release/v0.1.0")
        )
        assert not version_control.remote_branch_exists(
            ReleaseBranchName("release/v0.1.0")
        )
