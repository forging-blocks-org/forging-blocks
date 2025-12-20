from unittest.mock import patch

from scripts.release.infrastructure.versioning.poetry_versioning_service import (
    PoetryVersioningService,
)
from scripts.release.domain.value_objects import (
    ReleaseLevel,
    ReleaseVersion,
)


class TestPoetryVersioningService:
    @patch("scripts.release.infrastructure.versioning.poetry_versioning_service.run")
    def test_compute_next_version_parses_poetry_output(
        self,
        run_mock,
    ) -> None:
        run_mock.return_value = "my-package 1.2.3"

        service = PoetryVersioningService()

        version = service.compute_next_version(ReleaseLevel.from_str("minor"))

        assert version == ReleaseVersion(1, 3, 0)

    @patch("scripts.release.infrastructure.versioning.poetry_versioning_service.run")
    def test_apply_version_executes_poetry_version(
        self,
        run_mock,
    ) -> None:
        service = PoetryVersioningService()

        version = ReleaseVersion(1, 2, 3)

        service.apply_version(version)

        run_mock.assert_called_once_with(["poetry", "version", "1.2.3"])
