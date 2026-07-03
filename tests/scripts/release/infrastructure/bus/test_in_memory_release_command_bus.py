# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
"""Tests for the in-memory release command bus."""

import pytest
from scripts.release.domain.commands import OpenPullRequestCommand
from scripts.release.infrastructure.bus.in_memory_release_command_bus import (
    InMemoryReleaseCommandBus,
)


class FakeHandler:
    """State-based handler fake — records calls for assertion."""

    def __init__(self) -> None:
        self.handled_commands: list[OpenPullRequestCommand] = []

    async def handle(self, message: OpenPullRequestCommand) -> None:
        self.handled_commands.append(message)


@pytest.mark.unit
class TestInMemoryReleaseCommandBus:
    """Test the InMemoryReleaseCommandBus."""

    @pytest.fixture
    def command_bus(self) -> InMemoryReleaseCommandBus:
        return InMemoryReleaseCommandBus()

    @pytest.fixture
    def handler(self) -> FakeHandler:
        return FakeHandler()

    @pytest.fixture
    def test_command(self) -> OpenPullRequestCommand:
        return OpenPullRequestCommand(version="v0.3.11", branch="release/v0.3.11", dry_run=False)

    async def test_dispatch_calls_send(
        self,
        command_bus: InMemoryReleaseCommandBus,
        test_command: OpenPullRequestCommand,
        handler: FakeHandler,
    ) -> None:
        await command_bus.register(OpenPullRequestCommand, handler)

        await command_bus.dispatch(test_command)

        assert len(handler.handled_commands) == 1
        assert handler.handled_commands[0] is test_command

    async def test_register_and_send(
        self,
        command_bus: InMemoryReleaseCommandBus,
        test_command: OpenPullRequestCommand,
        handler: FakeHandler,
    ) -> None:
        await command_bus.register(OpenPullRequestCommand, handler)

        await command_bus.send(test_command)

        assert len(handler.handled_commands) == 1
        assert handler.handled_commands[0] is test_command
