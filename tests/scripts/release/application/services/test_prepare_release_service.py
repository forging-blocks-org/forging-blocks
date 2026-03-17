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
from scripts.release.application.workflow import ReleaseContext, ReleaseStep

from scripts.release.application.errors import TagAlreadyExistsError
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
    def tag_name(self) -> TagName:
        return TagName("v1.2.0")

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
        mock.tag_exists.return_value = False
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

    # Constructor Tests
    async def test_init_when_called_then_stores_dependencies(
        self,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        release_command_bus_mock: MagicMock,
        changelog_generator_mock: MagicMock,
    ) -> None:
        """Test that constructor properly initializes all dependencies."""
        service = PrepareReleaseService(
            versioning_service=versioning_service_mock,
            version_control=version_control_mock,
            transaction=transaction_mock,
            message_bus=release_command_bus_mock,
            changelog_generator=changelog_generator_mock,
        )

        assert service._versioning_service == versioning_service_mock
        assert service._version_control == version_control_mock
        assert service._transaction == transaction_mock
        assert service._message_bus == release_command_bus_mock
        assert service._changelog_generator == changelog_generator_mock

    # Main Execute Method Tests
    @pytest.mark.parametrize("release_level", ["major", "minor", "patch"])
    async def test_execute_with_valid_input_then_returns_prepare_output(
        self,
        service: PrepareReleaseService,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        release_command_bus_mock: MagicMock,
        next_version: ReleaseVersion,
        release_level: str,
    ) -> None:
        """Test execute returns correct output in dry_run mode without sending command."""
        # Arrange
        request = PrepareReleaseInput(level=release_level, dry_run=True)

        # Act
        result = await service.execute(request)

        # Assert
        assert isinstance(result, PrepareReleaseOutput)
        assert result.version == next_version.value
        assert result.branch == f"release/v{next_version.value}"
        assert result.tag == f"v{next_version.value}"

        # Verify service interactions
        versioning_service_mock.current_version.assert_called_once()
        versioning_service_mock.compute_next_version.assert_called_once()
        version_control_mock.tag_exists.assert_called_once()
        version_control_mock.branch_exists.assert_called_once()

        # dry_run must NOT send command — guard lives at the producer
        release_command_bus_mock.send.assert_not_called()

    async def test_execute_when_not_dry_run_then_performs_full_workflow(
        self,
        service: PrepareReleaseService,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        changelog_generator_mock: MagicMock,
        release_command_bus_mock: MagicMock,
        next_version: ReleaseVersion,
    ) -> None:
        """Test execute performs full workflow and sends command when not dry_run."""
        # Arrange
        request = PrepareReleaseInput(level="minor", dry_run=False)

        # Act
        result = await service.execute(request)

        # Assert
        assert isinstance(result, PrepareReleaseOutput)
        assert result.version == next_version.value

        # Verify transaction was used
        transaction_mock.__aenter__.assert_called_once()
        transaction_mock.__aexit__.assert_called_once()

        # Verify full workflow was executed
        versioning_service_mock.apply_version.assert_called_once_with(next_version)
        changelog_generator_mock.generate.assert_called_once()
        version_control_mock.commit_release_artifacts.assert_called_once()

        # Verify command is sent when not dry_run
        release_command_bus_mock.send.assert_called_once()

        # checkout_main + delete_local_branch (new branch) + rollback_version + delete_remote_branch
        assert transaction_mock.register_step.call_count == 4

    async def test_execute_when_branch_exists_then_checkout_existing_branch(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        """Test execute checks out existing branch and skips local branch deletion step."""
        # Arrange
        request = PrepareReleaseInput(level="patch", dry_run=False)
        version_control_mock.branch_exists.return_value = True

        # Act
        await service.execute(request)

        # Assert
        version_control_mock.checkout.assert_called_once()
        version_control_mock.create_branch.assert_not_called()

        # checkout_main + rollback_version + delete_remote_branch (no delete_local_branch)
        assert transaction_mock.register_step.call_count == 3

    async def test_execute_when_branch_not_exists_then_create_new_branch(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
    ) -> None:
        """Test execute creates branch and registers local branch deletion step."""
        # Arrange
        request = PrepareReleaseInput(level="major", dry_run=False)
        version_control_mock.branch_exists.return_value = False

        # Act
        await service.execute(request)

        # Assert
        version_control_mock.create_branch.assert_called_once()

        # checkout_main + delete_local_branch + rollback_version + delete_remote_branch
        assert transaction_mock.register_step.call_count == 4

    async def test_execute_when_tag_exists_then_raise_tag_already_exists(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
    ) -> None:
        """Test execute raises error when tag already exists."""
        # Arrange
        request = PrepareReleaseInput(level="minor", dry_run=False)
        version_control_mock.tag_exists.return_value = True

        # Act & Assert
        with pytest.raises(TagAlreadyExistsError):
            await service.execute(request)

    # Transaction Flow Tests
    async def test_prepare_release_transactionally_when_not_dry_run_then_full_execution(
        self,
        service: PrepareReleaseService,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        changelog_generator_mock: MagicMock,
        current_version: ReleaseVersion,
        next_version: ReleaseVersion,
    ) -> None:
        """Test _prepare_release_transactionally performs full workflow."""
        # Arrange
        context = ReleaseContext(
            previous_version=current_version,
            version=next_version,
            branch=ReleaseBranchName("release/v1.2.0"),
            tag=TagName("v1.2.0"),
            branch_exists=False,
            dry_run=False,
        )

        # Act
        await service._prepare_release_transactionally(context)

        # Assert
        transaction_mock.__aenter__.assert_called_once()

        versioning_service_mock.apply_version.assert_called_once_with(next_version)

        changelog_generator_mock.generate.assert_called_once()
        call_args = changelog_generator_mock.generate.call_args[0][0]
        assert isinstance(call_args, ChangelogRequest)
        assert call_args.from_version == current_version.value

        version_control_mock.commit_release_artifacts.assert_called_once()

    # Command Sending Tests
    async def test_send_command_creates_correct_open_pull_request_command(
        self,
        service: PrepareReleaseService,
        release_command_bus_mock: MagicMock,
        next_version: ReleaseVersion,
    ) -> None:
        """Test _send_command creates and sends correct OpenPullRequestCommand."""
        # Arrange
        context = ReleaseContext(
            previous_version=ReleaseVersion(1, 1, 0),
            version=next_version,
            branch=ReleaseBranchName("release/v1.2.0"),
            tag=TagName("v1.2.0"),
            branch_exists=False,
            dry_run=True,
        )

        # Act
        await service._send_command(context)

        # Assert
        release_command_bus_mock.send.assert_called_once()
        command = release_command_bus_mock.send.call_args[0][0]
        assert isinstance(command, OpenPullRequestCommand)
        assert command.version == next_version.value
        assert command.branch == "release/v1.2.0"
        assert command.dry_run is True

    @pytest.mark.parametrize("dry_run_value", [True, False])
    async def test_send_command_preserves_dry_run_flag(
        self,
        service: PrepareReleaseService,
        release_command_bus_mock: MagicMock,
        dry_run_value: bool,
    ) -> None:
        """Test _send_command preserves dry_run flag in command."""
        # Arrange
        context = ReleaseContext(
            previous_version=ReleaseVersion(1, 0, 0),
            version=ReleaseVersion(1, 1, 0),
            branch=ReleaseBranchName("release/v1.1.0"),
            tag=TagName("v1.1.0"),
            branch_exists=False,
            dry_run=dry_run_value,
        )

        # Act
        await service._send_command(context)

        # Assert
        command = release_command_bus_mock.send.call_args[0][0]
        assert command.dry_run is dry_run_value

    # Branch Handling Tests
    async def test_branch_handling_when_branch_exists_then_checkout_called(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        """Test _branch_handling when branch exists."""
        context_mock = MagicMock(branch_exists=True, branch=branch_name)
        service._branch_handling(context_mock)
        version_control_mock.checkout.assert_called_once_with(branch_name)

    async def test_branch_handling_when_branch_does_not_exist_then_create_branch_and_register_undo(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        """Test _branch_handling when branch doesn't exist."""
        context_mock = MagicMock(branch_exists=False, branch=branch_name)

        service._branch_handling(context_mock)

        version_control_mock.create_branch.assert_called_once_with(branch_name)
        transaction_mock.register_step.assert_called_once()
        step = transaction_mock.register_step.call_args[0][0]
        assert step.name == "delete_local_branch"

    # Tag Existence Tests
    async def test_ensure_tag_doesnt_exist_when_tag_exists_then_raises_error(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
    ) -> None:
        """Test _ensure_tag_doesnt_exist raises error when tag exists."""
        version_control_mock.tag_exists.return_value = True
        tag_mock = MagicMock()
        tag_mock.value = "v1.2.0"

        with pytest.raises(TagAlreadyExistsError):
            service._ensure_tag_doesnt_exist(tag_mock)

    async def test_ensure_tag_doesnt_exist_when_tag_does_not_exist_then_no_error(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
    ) -> None:
        """Test _ensure_tag_doesnt_exist passes when tag doesn't exist."""
        version_control_mock.tag_exists.return_value = False
        tag_mock = MagicMock()

        service._ensure_tag_doesnt_exist(tag_mock)  # Should not raise

    # Output Creation Tests
    async def test_make_output_when_called_then_returns_correct_output(
        self,
        service: PrepareReleaseService,
    ) -> None:
        """Test _make_output creates correct PrepareReleaseOutput."""
        context_mock = MagicMock()
        context_mock.version.value = "1.2.0"
        context_mock.branch.value = "release/v1.2.0"
        context_mock.tag.value = "v1.2.0"

        result = service._make_output(context_mock)

        assert result.version == "1.2.0"
        assert result.branch == "release/v1.2.0"
        assert result.tag == "v1.2.0"

    # Global Setup Tests
    async def test_global_setup_when_called_then_register_checkout_main_step(
        self,
        service: PrepareReleaseService,
        transaction_mock: MagicMock,
        version_control_mock: MagicMock,
    ) -> None:
        """Test _global_setup registers checkout_main rollback step."""
        service._global_setup()

        transaction_mock.register_step.assert_called_once()
        step = transaction_mock.register_step.call_args[0][0]
        assert step.name == "checkout_main"

    # Dry Run Tests
    async def test_prepare_release_transactionally_when_dry_run_then_early_return(
        self,
        service: PrepareReleaseService,
        transaction_mock: MagicMock,
        versioning_service_mock: MagicMock,
    ) -> None:
        """Test _prepare_release_transactionally returns early on dry_run."""
        context_mock = MagicMock(dry_run=True)

        await service._prepare_release_transactionally(context_mock)

        transaction_mock.__aenter__.assert_not_called()
        versioning_service_mock.apply_version.assert_not_called()

    async def test_execute_when_push_fails_then_deletes_remote_branch_on_rollback(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        # Arrange
        version_control_mock.tag_exists.return_value = False
        version_control_mock.branch_exists.return_value = False
        version_control_mock.push.side_effect = RuntimeError("Push failed!")

        input_data = PrepareReleaseInput(level="minor", dry_run=False)

        registered_steps: list[ReleaseStep] = []

        def capture_step(step: ReleaseStep) -> None:
            registered_steps.append(step)

        transaction_mock.register_step.side_effect = capture_step

        # Act & Assert
        with pytest.raises(RuntimeError, match="Push failed!"):
            await service.execute(input_data)

        delete_remote_step = next(
            (s for s in registered_steps if s.name == "delete_remote_branch"), None
        )
        assert delete_remote_step is not None, "delete_remote_branch step should be registered"

        delete_remote_step.undo()
        version_control_mock.delete_remote_branch.assert_called_once_with(branch_name)

    async def test_execute_when_successful_then_registers_remote_cleanup_before_push(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
    ) -> None:
        # Arrange
        version_control_mock.tag_exists.return_value = False
        version_control_mock.branch_exists.return_value = False

        input_data = PrepareReleaseInput(level="minor", dry_run=False)

        operation_order: list[str] = []

        def track_register_step(step: ReleaseStep) -> None:
            operation_order.append(f"register_{step.name}")

        def track_push(branch: ReleaseBranchName, *, push_tags: bool) -> None:
            operation_order.append("push")

        transaction_mock.register_step.side_effect = track_register_step
        version_control_mock.push.side_effect = track_push

        # Act
        await service.execute(input_data)

        # Assert
        delete_remote_index = operation_order.index("register_delete_remote_branch")
        push_index = operation_order.index("push")

        assert delete_remote_index < push_index, (
            f"delete_remote_branch step should be registered before push. Order: {operation_order}"
        )
