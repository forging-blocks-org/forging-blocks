import pytest
from unittest.mock import MagicMock, create_autospec, AsyncMock

from scripts.release.application.services.prepare_release_service import (
    PrepareReleaseService,
)
from scripts.release.application.ports.inbound import PrepareReleaseInput, PrepareReleaseOutput
from scripts.release.application.ports.outbound import (
    VersioningService,
    VersionControl,
    ReleaseTransaction,
    ChangelogGenerator,
    ReleaseCommandBus,
    ChangelogRequest,
)
from scripts.release.application.errors import TagAlreadyExistsError
from scripts.release.domain.value_objects import (
    ReleaseVersion,
    ReleaseBranchName,
    ReleaseLevel,
    TagName,
)
from scripts.release.domain.messages import OpenPullRequestCommand


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
    def versioning_service_mock(self, current_version: ReleaseVersion, next_version: ReleaseVersion) -> MagicMock:
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
        """Test execute method with various release levels in dry_run mode."""
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
        
        # Should send command even in dry_run
        release_command_bus_mock.send.assert_called_once()
        
    async def test_execute_when_not_dry_run_then_performs_full_workflow(
        self,
        service: PrepareReleaseService,
        versioning_service_mock: MagicMock,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        changelog_generator_mock: MagicMock,
        current_version: ReleaseVersion,
        next_version: ReleaseVersion,
    ) -> None:
        """Test execute method when not in dry_run mode - full workflow execution."""
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
        
        # Verify transaction steps were registered
        assert transaction_mock.register_step.call_count >= 2  # At least global_setup and tag

    async def test_execute_when_branch_exists_then_checkout_existing_branch(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        """Test execute method when release branch already exists."""
        # Arrange
        request = PrepareReleaseInput(level="patch", dry_run=False)
        version_control_mock.branch_exists.return_value = True
        
        # Act
        await service.execute(request)
        
        # Assert
        version_control_mock.checkout.assert_called_once()
        # Should not register branch deletion step since branch already existed
        version_control_mock.create_branch.assert_not_called()

    async def test_execute_when_branch_not_exists_then_create_new_branch(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
    ) -> None:
        """Test execute method when release branch doesn't exist."""
        # Arrange
        request = PrepareReleaseInput(level="major", dry_run=False)
        version_control_mock.branch_exists.return_value = False
        
        # Act
        await service.execute(request)
        
        # Assert
        version_control_mock.create_branch.assert_called_once()
        # Should register branch deletion step for rollback
        transaction_mock.register_step.assert_called()

    async def test_execute_when_tag_exists_then_raise_tag_already_exists(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
        tag_name: TagName,
    ) -> None:
        """Test execute method raises error when tag already exists."""
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
        from scripts.release.application.workflow import ReleaseContext
        
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
        
        # Assert - Verify full transaction workflow
        transaction_mock.__aenter__.assert_called_once()
        
        # Verify all steps were executed
        transaction_mock.register_step.assert_called()  # Multiple calls expected
        versioning_service_mock.apply_version.assert_called_once_with(next_version)
        
        # Verify changelog generation with correct request
        changelog_generator_mock.generate.assert_called_once()
        call_args = changelog_generator_mock.generate.call_args[0][0]
        assert isinstance(call_args, ChangelogRequest)
        assert call_args.from_version == current_version.value
        
        # Verify commit and tag creation
        version_control_mock.commit_release_artifacts.assert_called_once()
        version_control_mock.create_tag.assert_called_once()

    # Command Sending Tests
    async def test_send_command_creates_correct_open_pull_request_command(
        self,
        service: PrepareReleaseService,
        release_command_bus_mock: MagicMock,
        next_version: ReleaseVersion,
    ) -> None:
        """Test _send_command creates and sends correct OpenPullRequestCommand."""
        # Arrange
        from scripts.release.application.workflow import ReleaseContext
        
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
        from scripts.release.application.workflow import ReleaseContext
        
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

    # Branch Handling Tests (existing)
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

    # Tag Handling Tests (existing)
    async def test_tag_handling_when_called_then_create_tag_and_register_undo_step(
        self,
        service: PrepareReleaseService,
        version_control_mock: MagicMock,
        transaction_mock: MagicMock,
    ) -> None:
        """Test _tag_handling creates tag and registers rollback step."""
        tag_mock = MagicMock()
        context_mock = MagicMock(tag=tag_mock)
        
        service._tag_handling(context_mock)
        
        version_control_mock.create_tag.assert_called_once_with(tag_mock)
        transaction_mock.register_step.assert_called_once()

    # Tag Existence Tests (existing)
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

    # Output Creation Tests (existing)
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

    # Global Setup Tests (existing)
    async def test_global_setup_when_called_then_register_checkout_main_step(
        self,
        service: PrepareReleaseService,
        transaction_mock: MagicMock,
        version_control_mock: MagicMock,
    ) -> None:
        """Test _global_setup registers checkout_main rollback step."""
        service._global_setup()
        
        transaction_mock.register_step.assert_called_once()
        call_args = transaction_mock.register_step.call_args[0][0]
        assert call_args.name == "checkout_main"

    # Dry Run Tests (existing)
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


