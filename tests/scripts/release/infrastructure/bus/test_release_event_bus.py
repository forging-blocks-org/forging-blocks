# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from typing import Any

import pytest
from scripts.release.infrastructure.bus.in_memory_release_command_bus import (
    InMemoryReleaseCommandBus,
)

from forging_blocks.foundation.messages.command import Command


class FakeHandler:
    """State-based handler fake — records handled commands."""

    def __init__(self) -> None:
        self.handled: list[Command] = []

    async def handle(self, message: Command) -> None:
        self.handled.append(message)


class FakeCommand(Command):
    """Minimal concrete Command for registration and routing tests."""

    def __init__(self, val: str = "test") -> None:
        super().__init__()
        self._value = val

    @property
    def value(self) -> str:
        return self._value

    def _payload(self) -> dict[str, Any]:
        return {"value": self._value}


@pytest.mark.unit
class TestInMemoryReleaseCommandBus:
    @pytest.fixture
    def bus(self) -> InMemoryReleaseCommandBus:
        return InMemoryReleaseCommandBus()

    @pytest.fixture
    def handler(self) -> FakeHandler:
        return FakeHandler()

    @pytest.fixture
    def command(self) -> FakeCommand:
        return FakeCommand()

    def test_init_when_called_then_instance_created(self, bus: InMemoryReleaseCommandBus) -> None:
        assert isinstance(bus, InMemoryReleaseCommandBus)

    @pytest.mark.asyncio
    async def test_register_when_called_then_handler_is_registered(
        self, bus: InMemoryReleaseCommandBus, handler: FakeHandler
    ) -> None:
        await bus.register(FakeCommand, handler)

        assert bus._subscribers[FakeCommand] is handler

    @pytest.mark.asyncio
    async def test_send_when_no_subscribers_then_key_error(
        self,
        bus: InMemoryReleaseCommandBus,
        command: FakeCommand,
    ) -> None:
        with pytest.raises(KeyError):
            await bus.send(command)

    @pytest.mark.asyncio
    async def test_send_when_handler_registered_then_handler_handle_called(
        self,
        bus: InMemoryReleaseCommandBus,
        handler: FakeHandler,
        command: FakeCommand,
    ) -> None:
        await bus.register(FakeCommand, handler)

        await bus.send(command)

        assert len(handler.handled) == 1
        assert handler.handled[0] is command

    @pytest.mark.asyncio
    async def test_send_when_handler_registered_for_different_type_then_key_error(
        self,
        bus: InMemoryReleaseCommandBus,
        handler: FakeHandler,
        command: FakeCommand,
    ) -> None:
        await bus.register(FakeCommand, handler)

        class OtherCommand(Command):
            def __init__(self, val: str = "other") -> None:
                super().__init__()
                self._value = val

            @property
            def value(self) -> str:
                return self._value

            def _payload(self) -> dict[str, Any]:
                return {"value": self._value}

        with pytest.raises(KeyError):
            await bus.send(OtherCommand())
