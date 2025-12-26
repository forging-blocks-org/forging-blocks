import pytest
from unittest.mock import MagicMock, create_autospec

from scripts.release.infrastructure.commons.process import CommandRunner
from scripts.release.infrastructure.versioning.poetry_versioning_service import (
    PoetryVersioningService,
)
from scripts.release.domain.value_objects import ReleaseLevel, ReleaseVersion


class TestPoetryVersioningService:
    @pytest.fixture
    def runner_mock(self) -> MagicMock:
        return create_autospec(spec=CommandRunner, instance=True)

    def test_current_version_when_poetry_fails_then_error(self, runner_mock: MagicMock) -> None:
        runner_mock.run.side_effect = RuntimeError("poetry failed")

        service = PoetryVersioningService(runner=runner_mock)

        with pytest.raises(RuntimeError):
            service.current_version()

    def test_current_version_parses_poetry_output(self, runner_mock: MagicMock) -> None:
        runner_mock.run.return_value = "my-package 1.2.3"

        service = PoetryVersioningService(runner=runner_mock)

        version = service.current_version()

        assert version == ReleaseVersion(1, 2, 3)

    def test_compute_next_version_when_poetry_fails_then_error(self, runner_mock: MagicMock) -> None:
        runner_mock.run.side_effect = RuntimeError("poetry failed")

        service = PoetryVersioningService(runner=runner_mock)

        with pytest.raises(RuntimeError):
            service.compute_next_version(ReleaseLevel.from_str("minor"))

    def test_apply_version_when_poetry_fails_then_error(self, runner_mock: MagicMock) -> None:
        runner_mock.run.side_effect = RuntimeError("poetry failed")

        service = PoetryVersioningService(runner=runner_mock)

        with pytest.raises(RuntimeError):
            service.apply_version(ReleaseVersion(1, 2, 3))

    def test_compute_next_version_parses_poetry_output_when_minor(
        self,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.return_value = "my-package 1.2.3"

        service = PoetryVersioningService(runner=runner_mock)

        version = service.compute_next_version(ReleaseLevel.from_str("minor"))

        assert version == ReleaseVersion(1, 3, 0)

    def test_compute_next_version_parses_poetry_output_major(
        self,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.return_value = "my-package 1.2.3"

        service = PoetryVersioningService(runner=runner_mock)

        version = service.compute_next_version(ReleaseLevel.from_str("major"))

        assert version == ReleaseVersion(2, 0, 0)

    def test_compute_next_version_parses_poetry_output_patch(
        self,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.return_value = "my-package 1.2.4"

        service = PoetryVersioningService(runner=runner_mock)

        version = service.compute_next_version(ReleaseLevel.from_str("patch"))

        assert version == ReleaseVersion(1, 2, 5)

    def test_apply_version_executes_poetry_version(
        self,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.return_value = "my-package 1.2.4"
        service = PoetryVersioningService(runner=runner_mock)

        version = ReleaseVersion(1, 2, 3)

        service.apply_version(version)

        runner_mock.run.assert_called_once_with(["poetry", "version", "1.2.3"])

    def test_compute_next_version_when_poetry_output_invalid_then_error(
        self,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.return_value = "invalid-output"
        service = PoetryVersioningService(runner=runner_mock)

        with pytest.raises(ValueError):
            service.compute_next_version(ReleaseLevel.from_str("minor"))

    def test_rollback_version_executes_poetry_version(
        self,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.return_value = "my-package 0.9.9"
        service = PoetryVersioningService(runner=runner_mock)
        previous_version = ReleaseVersion(0, 9, 9)

        service.rollback_version(previous_version)

        runner_mock.run.assert_called_once_with(["poetry", "version", "0.9.9"])

    def test_rollback_version_when_poetry_fails_then_error(
        self,
        runner_mock: MagicMock,
    ) -> None:
        runner_mock.run.side_effect = RuntimeError("poetry failed")

        service = PoetryVersioningService(runner=runner_mock)
        previous_version = ReleaseVersion(0, 9, 9)

        with pytest.raises(RuntimeError):
            service.rollback_version(previous_version)
