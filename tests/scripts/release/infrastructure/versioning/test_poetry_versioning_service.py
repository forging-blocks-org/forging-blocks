# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from __future__ import annotations

import pytest
from scripts.release.infrastructure.versioning.poetry_versioning_service import (
    PoetryVersioningService,
)

from scripts.release.domain.value_objects import ReleaseLevel, ReleaseVersion
from tests.fixtures.git_test_repository import GitTestRepository


@pytest.mark.integration
class TestPoetryVersioningService:
    """Tests against a real git repository with a genuine pyproject.toml.
    No mocks are used."""

    @pytest.fixture
    def poetry_repo(self, pyproject_toml: GitTestRepository) -> GitTestRepository:
        return pyproject_toml

    @pytest.fixture
    def service(self, poetry_repo: GitTestRepository) -> PoetryVersioningService:
        return PoetryVersioningService(runner=poetry_repo.scoped_runner())

    def test_current_version_when_pyproject_has_version_then_returns_it(
        self, service: PoetryVersioningService
    ) -> None:
        version = service.current_version()
        assert version == ReleaseVersion(0, 0, 0)

    @pytest.mark.parametrize(
        ("level_str", "expected"),
        [("major", "1.0.0"), ("minor", "0.1.0"), ("patch", "0.0.1")],
    )
    def test_compute_next_version(
        self,
        service: PoetryVersioningService,
        level_str: str,
        expected: str,
    ) -> None:
        level = ReleaseLevel.from_str(level_str)
        version = service.compute_next_version(level)
        assert version.value == expected

    def test_apply_version_when_dry_run_false_then_mutates_pyproject(
        self,
        service: PoetryVersioningService,
        poetry_repo: GitTestRepository,
    ) -> None:
        service.apply_version(ReleaseVersion(2, 0, 0), dry_run=False)

        content = (poetry_repo.path / "pyproject.toml").read_text(encoding="utf-8")
        assert 'version = "2.0.0"' in content
        assert 'version = "0.0.0"' not in content

    def test_apply_version_when_dry_run_true_then_does_not_mutate_pyproject(
        self,
        service: PoetryVersioningService,
        poetry_repo: GitTestRepository,
    ) -> None:
        original = (poetry_repo.path / "pyproject.toml").read_text(encoding="utf-8")

        service.apply_version(ReleaseVersion(2, 0, 0), dry_run=True)

        content = (poetry_repo.path / "pyproject.toml").read_text(encoding="utf-8")
        assert content == original
        assert 'version = "2.0.0"' not in content

    def test_apply_version_when_dry_run_false_then_current_version_reflects_change(
        self,
        service: PoetryVersioningService,
    ) -> None:
        service.apply_version(ReleaseVersion(3, 1, 0), dry_run=False)

        version = service.current_version()
        assert version == ReleaseVersion(3, 1, 0)
