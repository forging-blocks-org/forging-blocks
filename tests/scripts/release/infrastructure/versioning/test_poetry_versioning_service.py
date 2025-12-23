import pytest
from unittest.mock import patch

from scripts.release.infrastructure.versioning.poetry_versioning_service import (
    PoetryVersioningService,
)
from scripts.release.domain.value_objects import ReleaseLevel, ReleaseVersion


class TestPoetryVersioningServiceErrors:
    @patch("subprocess.run")
    def test_compute_next_version_when_poetry_fails_then_error(self, run) -> None:
        run.side_effect = RuntimeError("poetry failed")

        service = PoetryVersioningService()

        with pytest.raises(RuntimeError):
            service.compute_next_version(ReleaseLevel.from_str("minor"))

    @patch("subprocess.run")
    def test_apply_version_when_poetry_fails_then_error(self, run) -> None:
        run.side_effect = RuntimeError("poetry failed")

        service = PoetryVersioningService()

        with pytest.raises(RuntimeError):
            service.apply_version(ReleaseVersion(1, 2, 3))

    @patch("scripts.release.infrastructure.versioning.poetry_versioning_service.run")
    def test_compute_next_version_parses_poetry_output_when_minor(
        self,
        run_mock,
    ) -> None:
        run_mock.return_value = "my-package 1.2.3"

        service = PoetryVersioningService()

        version = service.compute_next_version(ReleaseLevel.from_str("minor"))

        assert version == ReleaseVersion(1, 3, 0)

    @patch("scripts.release.infrastructure.versioning.poetry_versioning_service.run")
    def test_compute_next_version_parses_poetry_output_major(
        self,
        run_mock,
    ) -> None:
        run_mock.return_value = "my-package 1.2.3"

        service = PoetryVersioningService()

        version = service.compute_next_version(ReleaseLevel.from_str("major"))

        assert version == ReleaseVersion(2, 0, 0)

    @patch("scripts.release.infrastructure.versioning.poetry_versioning_service.run")
    def test_compute_next_version_parses_poetry_output_patch(
        self,
        run_mock,
    ) -> None:
        run_mock.return_value = "my-package 1.2.4"

        service = PoetryVersioningService()

        version = service.compute_next_version(ReleaseLevel.from_str("patch"))

        assert version == ReleaseVersion(1, 2, 5)

    @patch("scripts.release.infrastructure.versioning.poetry_versioning_service.run")
    def test_apply_version_executes_poetry_version(
        self,
        run_mock,
    ) -> None:
        service = PoetryVersioningService()

        version = ReleaseVersion(1, 2, 3)

        service.apply_version(version)

        run_mock.assert_called_once_with(["poetry", "version", "1.2.3"])

    def test_compute_next_version_when_poetry_output_invalid_then_error(self) -> None:
        service = PoetryVersioningService()

        with patch(
            "scripts.release.infrastructure.versioning.poetry_versioning_service.run",
            return_value="invalid-output",
        ):
            with pytest.raises(ValueError):
                service.compute_next_version(ReleaseLevel.from_str("minor"))
