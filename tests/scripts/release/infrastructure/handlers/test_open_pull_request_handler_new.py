# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest
from scripts.release.application.ports.inbound import (
    OpenReleasePullRequestInput,
    OpenReleasePullRequestOutput,
)
from scripts.release.application.ports.inbound.open_release_pull_request_use_case import (
    OpenReleasePullRequestUseCase,
)
from scripts.release.domain.commands.open_pull_request_command import (
    OpenPullRequestCommand,
)
from scripts.release.infrastructure.handlers.open_pull_request_handler import (
    OpenPullRequestHandler,
)


class FakeOpenReleasePullRequestUseCase(OpenReleasePullRequestUseCase):
    """State-based use-case fake — records inputs and returns configured output."""

    def __init__(self) -> None:
        self.execute_calls: list[OpenReleasePullRequestInput] = []
        self._raise: Exception | None = None

    async def execute(self, request: OpenReleasePullRequestInput) -> OpenReleasePullRequestOutput:
        if self._raise is not None:
            raise self._raise
        self.execute_calls.append(request)
        return OpenReleasePullRequestOutput(pr_id=None, url=None)


@pytest.mark.unit
class TestOpenPullRequestHandler:
    @pytest.fixture
    def use_case(self) -> FakeOpenReleasePullRequestUseCase:
        return FakeOpenReleasePullRequestUseCase()

    @pytest.fixture
    def handler(self, use_case: FakeOpenReleasePullRequestUseCase) -> OpenPullRequestHandler:
        return OpenPullRequestHandler(use_case)

    @pytest.fixture
    def command(self) -> OpenPullRequestCommand:
        return OpenPullRequestCommand(version="1.2.0", branch="release/v1.2.0", dry_run=False)

    def test_init_when_called_then_sets_use_case(
        self, use_case: FakeOpenReleasePullRequestUseCase
    ) -> None:
        handler = OpenPullRequestHandler(use_case)

        assert handler._use_case is use_case

    @pytest.mark.asyncio
    async def test_handle_when_called_then_creates_pr_input_with_command_data(
        self,
        handler: OpenPullRequestHandler,
        use_case: FakeOpenReleasePullRequestUseCase,
        command: OpenPullRequestCommand,
    ) -> None:
        await handler.handle(command)

        assert len(use_case.execute_calls) == 1
        call_args = use_case.execute_calls[0]
        assert isinstance(call_args, OpenReleasePullRequestInput)
        assert call_args.version == "1.2.0"
        assert call_args.branch == "release/v1.2.0"
        assert call_args.dry_run is False

    @pytest.mark.asyncio
    async def test_handle_when_dry_run_true_then_passes_dry_run_to_use_case(
        self, handler: OpenPullRequestHandler, use_case: FakeOpenReleasePullRequestUseCase
    ) -> None:
        command = OpenPullRequestCommand(version="2.0.0", branch="release/v2.0.0", dry_run=True)

        await handler.handle(command)

        assert use_case.execute_calls[0].dry_run is True

    @pytest.mark.asyncio
    async def test_handle_when_use_case_raises_exception_then_propagates(
        self,
        handler: OpenPullRequestHandler,
        use_case: FakeOpenReleasePullRequestUseCase,
        command: OpenPullRequestCommand,
    ) -> None:
        use_case._raise = RuntimeError("Use case failed")

        with pytest.raises(RuntimeError, match="Use case failed"):
            await handler.handle(command)

    @pytest.mark.asyncio
    async def test_handle_when_called_with_different_versions_then_maps_correctly(
        self, handler: OpenPullRequestHandler, use_case: FakeOpenReleasePullRequestUseCase
    ) -> None:
        versions = ["1.0.0", "2.1.3", "10.5.7"]

        for version in versions:
            command = OpenPullRequestCommand(
                version=version, branch=f"release/v{version}", dry_run=False
            )
            await handler.handle(command)

        assert len(use_case.execute_calls) == 3
        assert use_case.execute_calls[0].version == "1.0.0"
        assert use_case.execute_calls[1].version == "2.1.3"
        assert use_case.execute_calls[2].version == "10.5.7"

    @pytest.mark.asyncio
    async def test_handle_when_called_multiple_times_then_each_call_creates_separate_input(
        self, handler: OpenPullRequestHandler, use_case: FakeOpenReleasePullRequestUseCase
    ) -> None:
        command1 = OpenPullRequestCommand(version="1.0.0", branch="release/v1.0.0", dry_run=False)
        command2 = OpenPullRequestCommand(version="2.0.0", branch="release/v2.0.0", dry_run=True)

        await handler.handle(command1)
        await handler.handle(command2)

        assert len(use_case.execute_calls) == 2

        assert use_case.execute_calls[0].version == "1.0.0"
        assert use_case.execute_calls[0].dry_run is False
        assert use_case.execute_calls[1].version == "2.0.0"
        assert use_case.execute_calls[1].dry_run is True
