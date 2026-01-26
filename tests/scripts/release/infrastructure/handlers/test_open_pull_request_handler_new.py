import pytest
from unittest.mock import MagicMock, create_autospec, AsyncMock

from scripts.release.infrastructure.handlers.open_pull_request_handler import OpenPullRequestHandler
from scripts.release.application.ports.inbound import OpenReleasePullRequestUseCase, OpenReleasePullRequestInput
from scripts.release.domain.messages.open_pull_request_command import OpenPullRequestCommand


class TestOpenPullRequestHandler:
    @pytest.fixture
    def use_case_mock(self) -> MagicMock:
        return create_autospec(OpenReleasePullRequestUseCase, instance=True)

    @pytest.fixture
    def handler(self, use_case_mock: MagicMock) -> OpenPullRequestHandler:
        return OpenPullRequestHandler(use_case_mock)

    @pytest.fixture
    def command(self) -> OpenPullRequestCommand:
        return OpenPullRequestCommand(
            version="1.2.0",
            branch="release/v1.2.0",
            dry_run=False
        )

    def test_init_when_called_then_sets_use_case(self, use_case_mock: MagicMock) -> None:
        handler = OpenPullRequestHandler(use_case_mock)

        assert handler._use_case == use_case_mock

    @pytest.mark.asyncio
    async def test_handle_when_called_then_creates_pr_input_with_command_data(
        self, handler: OpenPullRequestHandler, use_case_mock: MagicMock, command: OpenPullRequestCommand
    ) -> None:
        use_case_mock.execute = AsyncMock()

        await handler.handle(command)

        use_case_mock.execute.assert_called_once()
        call_args = use_case_mock.execute.call_args[0][0]
        assert isinstance(call_args, OpenReleasePullRequestInput)
        assert call_args.version == "1.2.0"
        assert call_args.branch == "release/v1.2.0"
        assert call_args.dry_run is False

    @pytest.mark.asyncio
    async def test_handle_when_dry_run_true_then_passes_dry_run_to_use_case(
        self, handler: OpenPullRequestHandler, use_case_mock: MagicMock
    ) -> None:
        use_case_mock.execute = AsyncMock()
        command = OpenPullRequestCommand(
            version="2.0.0",
            branch="release/v2.0.0",
            dry_run=True
        )

        await handler.handle(command)

        call_args = use_case_mock.execute.call_args[0][0]
        assert call_args.dry_run is True

    @pytest.mark.asyncio
    async def test_handle_when_use_case_raises_exception_then_propagates(
        self, handler: OpenPullRequestHandler, use_case_mock: MagicMock, command: OpenPullRequestCommand
    ) -> None:
        use_case_mock.execute = AsyncMock(side_effect=RuntimeError("Use case failed"))

        with pytest.raises(RuntimeError, match="Use case failed"):
            await handler.handle(command)

    @pytest.mark.asyncio
    async def test_handle_when_called_with_different_versions_then_maps_correctly(
        self, handler: OpenPullRequestHandler, use_case_mock: MagicMock
    ) -> None:
        use_case_mock.execute = AsyncMock()
        versions = ["1.0.0", "2.1.3", "10.5.7"]

        for version in versions:
            command = OpenPullRequestCommand(
                version=version,
                branch=f"release/v{version}",
                dry_run=False
            )

            await handler.handle(command)

            call_args = use_case_mock.execute.call_args[0][0]
            assert call_args.version == version
            assert call_args.branch == f"release/v{version}"

    @pytest.mark.asyncio
    async def test_handle_when_called_multiple_times_then_each_call_creates_separate_input(
        self, handler: OpenPullRequestHandler, use_case_mock: MagicMock
    ) -> None:
        use_case_mock.execute = AsyncMock()

        command1 = OpenPullRequestCommand(version="1.0.0", branch="release/v1.0.0", dry_run=False)
        command2 = OpenPullRequestCommand(version="2.0.0", branch="release/v2.0.0", dry_run=True)

        await handler.handle(command1)
        await handler.handle(command2)

        assert use_case_mock.execute.call_count == 2

        first_call_args = use_case_mock.execute.call_args_list[0][0][0]
        second_call_args = use_case_mock.execute.call_args_list[1][0][0]

        assert first_call_args.version == "1.0.0"
        assert first_call_args.dry_run is False
        assert second_call_args.version == "2.0.0"
        assert second_call_args.dry_run is True
