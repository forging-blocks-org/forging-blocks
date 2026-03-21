from unittest.mock import AsyncMock, MagicMock, create_autospec

import pytest
from scripts.release.application.ports.inbound import (
    PrepareReleaseInput,
    PrepareReleaseOutput,
)
from scripts.release.application.ports.outbound import (
    ChangelogGenerator,
    ChangelogRequest,
    ReleaseCommandBus,
    ReleaseTransaction,
    VersionControl,
    VersioningService,
)
from scripts.release.application.services.prepare_release_service import (
    PrepareReleaseService,
)
from scripts.release.application.workflow import ReleaseContext

from scripts.release.domain.messages import OpenPullRequestCommand
from scripts.release.domain.value_objects import (
    ReleaseBranchName,
    ReleaseVersion,
    TagName,
)


@pytest.mark.unit
class TestPrepareReleaseService:
    @pytest.fixture
    def current_version(self) -> ReleaseVersion:
        return ReleaseVersion(1, 1, 0)

    @pytest.fixture
    def next_version(self) -> ReleaseVersion:
        return ReleaseVersion(1, 2, 0)

    @pytest.fixture
    def branch_name(self) -> ReleaseBranchName:
        return ReleaseBranchName("release/v1.2.0")

    @pytest.fixture
    def versioning_service_mock(
        self, current_version: ReleaseVersion, next_version: ReleaseVersion
    ) -> MagicMock:
        mock = create_autospec(VersioningService, instance=True)
        mock.current_version.return_value = current_version
        mock.compute_next_version.return_value = next_version
        return mock

    @pytest.fixture
    def version_control_mock(self) -> MagicMock:
        mock = create_autospec(VersionControl, instance=True)
        mock.branch_exists.return_value = False
        return mock

    @pytest.fixture
    def transaction_mock(self) -> MagicMock:
        transaction = create_autospec(ReleaseTransaction, instance=True)
        transaction.__aenter__.return_value = transaction
        transaction.__aexit__.return_value = None
        return transaction

    @pytest.fixture
    def release_command_bus_mock(self) -> MagicMock:
        mock = create_autospec(ReleaseCommandBus, instance=True)
        mock.send = AsyncMock()
        return mock

    @pytest.fixture
    def changelog_generator_mock(self) -> MagicMock:
        mock = create_autospec(ChangelogGenerator, instance=True)
        mock.generate = AsyncMock()
        return mock

    @pytest.fixture
    def service(
        self,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        release_command_bus_mock: MagicMock,
        changelog_generator_mock: MagicMock,
    ) -> PrepareReleaseService:
        return PrepareReleaseService(
            versioning_service=versioning_service_mock,
            version_control=version_control_mock,
            transaction=transaction_mock,
            message_bus=release_command_bus_mock,
            changelog_generator=changelog_generator_mock,
        )

    @pytest.mark.parametrize("release_level", ["major", "minor", "patch"])
    async def test_execute_dry_run(
        self,
        service: PrepareReleaseService,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        release_command_bus_mock: MagicMock,
        next_version: ReleaseVersion,
        release_level: str,
    ) -> None:
        request = PrepareReleaseInput(level=release_level, dry_run=True)

        result = await service.execute(request)

        assert isinstance(result, PrepareReleaseOutput)
        assert result.version == next_version.value
        assert result.branch == f"release/v{next_version.value}"
        assert result.tag == f"v{next_version.value}"

        versioning_service_mock.current_version.assert_called_once()
        versioning_service_mock.compute_next_version.assert_called_once()
        version_control_mock.branch_exists.assert_called_once()

        release_command_bus_mock.send.assert_not_called()

    async def test_execute_full_flow(
        self,
        service: PrepareReleaseService,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        changelog_generator_mock: MagicMock,
        release_command_bus_mock: MagicMock,
        next_version: ReleaseVersion,
    ) -> None:
        request = PrepareReleaseInput(level="minor", dry_run=False)

        result = await service.execute(request)

        assert result.version == next_version.value

        transaction_mock.__aenter__.assert_called_once()
        transaction_mock.__aexit__.assert_called_once()

        versioning_service_mock.apply_version.assert_called_once_with(next_version)
        changelog_generator_mock.generate.assert_called_once()
        version_control_mock.commit_release_artifacts.assert_called_once()

        release_command_bus_mock.send.assert_called_once()

        assert transaction_mock.register_step.call_count == 4

    async def test_branch_exists(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
    ) -> None:
        version_control_mock.branch_exists.return_value = True

        await service.execute(PrepareReleaseInput(level="patch", dry_run=False))

        version_control_mock.checkout.assert_called_once()
        version_control_mock.create_branch.assert_not_called()

        assert transaction_mock.register_step.call_count == 3

    async def test_branch_not_exists(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
    ) -> None:
        version_control_mock.branch_exists.return_value = False

        await service.execute(PrepareReleaseInput(level="major", dry_run=False))

        version_control_mock.create_branch.assert_called_once()

        assert transaction_mock.register_step.call_count == 4

    async def test_transactional_flow(
        self,
        service: PrepareReleaseService,
        versioning_service_mock: MagicMock,
        transaction_mock: MagicMock,
        changelog_generator_mock: MagicMock,
        current_version: ReleaseVersion,
        next_version: ReleaseVersion,
    ) -> None:
        context = ReleaseContext(
            previous_version=current_version,
            version=next_version,
            branch=ReleaseBranchName("release/v1.2.0"),
            tag=TagName("v1.2.0"),
            branch_exists=False,
            dry_run=False,
        )

        await service._prepare_release_transactionally(context)

        transaction_mock.__aenter__.assert_called_once()

        versioning_service_mock.apply_version.assert_called_once_with(next_version)

        changelog_generator_mock.generate.assert_called_once()
        call_args = changelog_generator_mock.generate.call_args[0][0]
        assert isinstance(call_args, ChangelogRequest)
        assert call_args.from_version == next_version.value

    async def test_send_command(
        self,
        service: PrepareReleaseService,
        release_command_bus_mock: MagicMock,
    ) -> None:
        context = ReleaseContext(
            previous_version=ReleaseVersion(1, 1, 0),
            version=ReleaseVersion(1, 2, 0),
            branch=ReleaseBranchName("release/v1.2.0"),
            tag=TagName("v1.2.0"),
            branch_exists=False,
            dry_run=True,
        )

        await service._send_command(context)

        command = release_command_bus_mock.send.call_args[0][0]

        assert isinstance(command, OpenPullRequestCommand)
        assert command.branch == "release/v1.2.0"
        assert command.dry_run is True

    async def test_dry_run_short_circuit(
        self,
        service: PrepareReleaseService,
        transaction_mock: MagicMock,
        versioning_service_mock: MagicMock,
    ) -> None:
        context_mock = MagicMock(dry_run=True)

        await service._prepare_release_transactionally(context_mock)

        transaction_mock.__aenter__.assert_not_called()
        versioning_service_mock.apply_version.assert_not_called()
