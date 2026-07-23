# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from typing import Any, Self

import pytest
from scripts.release.infrastructure.bus.in_memory_release_command_bus import (
    InMemoryReleaseCommandBus,
)

from forging_blocks.application.ports.inbound.message_handler_port import MessageHandlerPort
from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.message import MessageMetadata


class FakeCommand(Command):
    """Minimal concrete Command for registration and routing tests."""

    def __init__(self, val: str = "test") -> None:
        super().__init__()
        self._value = val

    @property
    def value(self) -> str:
        return self._value

    @property
    def _payload(self) -> dict[str, Any]:
        return {"value": self._value}

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls(val=str(data.get("value", "test")))


class FakeHandler(MessageHandlerPort[FakeCommand, None]):
    """State-based handler fake — records handled commands."""

    def __init__(self) -> None:
        self.handled: list[Command[Any]] = []

    async def handle(self, message: FakeCommand) -> None:
        self.handled.append(message)


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

    async def test_register_when_called_then_handler_is_registered(
        self, bus: InMemoryReleaseCommandBus, handler: FakeHandler
    ) -> None:
        await bus.register(FakeCommand, handler)

        assert bus._subscribers[FakeCommand] is handler

    async def test_send_when_no_subscribers_then_key_error(
        self,
        bus: InMemoryReleaseCommandBus,
        command: FakeCommand,
    ) -> None:
        with pytest.raises(KeyError):
            await bus.send(command)

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

            @property
            def _payload(self) -> dict[str, Any]:
                return {"value": self._value}

            @classmethod
            def from_payload_fields(
                cls, data: dict[str, object], metadata: MessageMetadata
            ) -> "OtherCommand":
                return cls(val=str(data.get("value", "other")))

        with pytest.raises(KeyError):
            await bus.send(OtherCommand())
