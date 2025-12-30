import pytest
from unittest.mock import MagicMock, create_autospec

from scripts.release.application.services.prepare_release_service import (
    PrepareReleaseService,
)
from scripts.release.application.ports.inbound import PrepareReleaseInput
from scripts.release.application.ports.outbound import (
    VersioningService,
    VersionControl,
    ReleaseTransaction,
    ChangelogGenerator,
    ReleaseMessageBus,
)
from scripts.release.application.errors import TagAlreadyExistsError
from scripts.release.domain.value_objects import (
    ReleaseVersion,
    ReleaseBranchName,
)


class TestPrepareReleaseService:
    @pytest.fixture
    def version(self) -> ReleaseVersion:
        return ReleaseVersion(1, 2, 0)

    @pytest.fixture
    def branch_name(self) -> ReleaseBranchName:
        return ReleaseBranchName("release/v1.2.0")

    @pytest.fixture
    def versioning_service_mock(self) -> MagicMock:
        return create_autospec(VersioningService, instance=True)

    @pytest.fixture
    def version_control_mock(self) -> MagicMock:
        return create_autospec(VersionControl, instance=True)

    @pytest.fixture
    def transaction_mock(self) -> MagicMock:
        transaction = create_autospec(ReleaseTransaction, instance=True)
        transaction.__aenter__.return_value = transaction
        transaction.__aexit__.return_value = None
        return transaction

    @pytest.fixture
    def release_message_bus_mock(self) -> MagicMock:
        return create_autospec(ReleaseMessageBus, instance=True)

    @pytest.fixture
    def changelog_generator_mock(self) -> MagicMock:
        return create_autospec(ChangelogGenerator, instance=True)

    async def test_execute_when_tag_exists_then_raise_tag_already_exists(
        self,
        version: ReleaseVersion,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        release_message_bus_mock: MagicMock,
        changelog_generator_mock: MagicMock,
    ) -> None:
        versioning_service_mock.current_version.return_value = version
        versioning_service_mock.compute_next_version.return_value = version
        version_control_mock.tag_exists.return_value = True

        service = PrepareReleaseService(
            versioning_service=versioning_service_mock,
            version_control=version_control_mock,
            transaction=transaction_mock,
            message_bus=release_message_bus_mock,
            changelog_generator=changelog_generator_mock,
        )

        request = PrepareReleaseInput(level="minor", dry_run=False)

        with pytest.raises(TagAlreadyExistsError):
            await service.execute(request)

    async def test_execute_when_dry_run_then_event_published_but_no_other_side_effects(
        self,
        version: ReleaseVersion,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        release_message_bus_mock: MagicMock,
        changelog_generator_mock: MagicMock,
    ) -> None:
        versioning_service_mock.current_version.return_value = version
        versioning_service_mock.compute_next_version.return_value = version
        version_control_mock.tag_exists.return_value = False

        service = PrepareReleaseService(
            versioning_service=versioning_service_mock,
            version_control=version_control_mock,
            transaction=transaction_mock,
            message_bus=release_message_bus_mock,
            changelog_generator=changelog_generator_mock,
        )

        request = PrepareReleaseInput(level="minor", dry_run=True)

        result = await service.execute(request)

        version_control_mock.create_branch.assert_not_called()
        version_control_mock.checkout.assert_not_called()
        version_control_mock.commit_release_artifacts.assert_not_called()
        version_control_mock.create_tag.assert_not_called()
        release_message_bus_mock.publish.assert_called()

        assert result.version == version.value

    async def test_execute_when_branch_exists_then_checkout_branch(
        self,
        version: ReleaseVersion,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        release_message_bus_mock: MagicMock,
        changelog_generator_mock: MagicMock,
    ) -> None:
        versioning_service_mock.current_version.return_value = version
        versioning_service_mock.compute_next_version.return_value = version
        version_control_mock.tag_exists.return_value = False
        version_control_mock.branch_exists.return_value = True

        service = PrepareReleaseService(
            versioning_service=versioning_service_mock,
            version_control=version_control_mock,
            transaction=transaction_mock,
            message_bus=release_message_bus_mock,
            changelog_generator=changelog_generator_mock,
        )

        await service.execute(PrepareReleaseInput(level="minor", dry_run=False))

        version_control_mock.checkout.assert_called_once()
        version_control_mock.create_branch.assert_not_called()

    async def test_execute_when_branch_does_not_exist_then_create_branch(
        self,
        version: ReleaseVersion,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        release_message_bus_mock: MagicMock,
        changelog_generator_mock: MagicMock,
    ) -> None:
        versioning_service_mock.current_version.return_value = version
        versioning_service_mock.compute_next_version.return_value = version
        version_control_mock.tag_exists.return_value = False
        version_control_mock.branch_exists.return_value = False

        service = PrepareReleaseService(
            versioning_service=versioning_service_mock,
            version_control=version_control_mock,
            transaction=transaction_mock,
            message_bus=release_message_bus_mock,
            changelog_generator=changelog_generator_mock,
        )

        await service.execute(PrepareReleaseInput(level="minor", dry_run=False))

        version_control_mock.create_branch.assert_called_once()

    async def test_execute_when_version_applied_then_versioning_service_called(
        self,
        version: ReleaseVersion,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        release_message_bus_mock: MagicMock,
        changelog_generator_mock: MagicMock,
    ) -> None:
        versioning_service_mock.current_version.return_value = version
        versioning_service_mock.compute_next_version.return_value = version
        version_control_mock.tag_exists.return_value = False
        version_control_mock.branch_exists.return_value = False

        service = PrepareReleaseService(
            versioning_service=versioning_service_mock,
            version_control=version_control_mock,
            transaction=transaction_mock,
            message_bus=release_message_bus_mock,
            changelog_generator=changelog_generator_mock,
        )

        await service.execute(PrepareReleaseInput(level="minor", dry_run=False))

        versioning_service_mock.apply_version.assert_called_once_with(version)

    async def test_execute_when_changelog_generated_then_generator_called(
        self,
        version: ReleaseVersion,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        release_message_bus_mock: MagicMock,
        changelog_generator_mock: MagicMock,
    ) -> None:
        versioning_service_mock.current_version.return_value = version
        versioning_service_mock.compute_next_version.return_value = version
        version_control_mock.tag_exists.return_value = False
        version_control_mock.branch_exists.return_value = False

        service = PrepareReleaseService(
            versioning_service=versioning_service_mock,
            version_control=version_control_mock,
            transaction=transaction_mock,
            message_bus=release_message_bus_mock,
            changelog_generator=changelog_generator_mock,
        )

        await service.execute(PrepareReleaseInput(level="minor", dry_run=False))

        changelog_generator_mock.generate.assert_called_once()

    async def test_execute_when_transaction_succeeds_then_event_published(
        self,
        version: ReleaseVersion,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        release_message_bus_mock: MagicMock,
        changelog_generator_mock: MagicMock,
    ) -> None:
        versioning_service_mock.current_version.return_value = version
        versioning_service_mock.compute_next_version.return_value = version
        version_control_mock.tag_exists.return_value = False
        version_control_mock.branch_exists.return_value = False

        service = PrepareReleaseService(
            versioning_service=versioning_service_mock,
            version_control=version_control_mock,
            transaction=transaction_mock,
            message_bus=release_message_bus_mock,
            changelog_generator=changelog_generator_mock,
        )

        await service.execute(PrepareReleaseInput(level="minor", dry_run=False))

        release_message_bus_mock.publish.assert_called_once()

    async def test_execute_when_transaction_fails_then_no_event_published(
        self,
        version: ReleaseVersion,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        release_message_bus_mock: MagicMock,
        changelog_generator_mock: MagicMock,
    ) -> None:
        versioning_service_mock.current_version.return_value = version
        versioning_service_mock.compute_next_version.return_value = version
        version_control_mock.tag_exists.return_value = False
        version_control_mock.branch_exists.return_value = False

        transaction_mock.__aexit__.side_effect = Exception("Transaction failed")

        service = PrepareReleaseService(
            versioning_service=versioning_service_mock,
            version_control=version_control_mock,
            transaction=transaction_mock,
            message_bus=release_message_bus_mock,
            changelog_generator=changelog_generator_mock,
        )

        with pytest.raises(Exception):
            await service.execute(PrepareReleaseInput(level="minor", dry_run=False))

        release_message_bus_mock.publish.assert_not_called()
