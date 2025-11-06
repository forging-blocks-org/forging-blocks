from typing import Any
from unittest.mock import AsyncMock, MagicMock

from pytest import fixture

from building_blocks.application.ports.outbound.command_sender import CommandSender
from building_blocks.application.ports.outbound.message_bus import MessageBus
from building_blocks.domain.messages.command import Command


class FakeCommand(Command[str]):
    @property
    def value(self) -> str:
        return "foo"

    def _payload(self) -> dict[str, Any]:
        return {"foo": "foo"}


class TestCommandSender:
    @fixture
    def message_bus(self) -> MagicMock:
        bus = MagicMock(spec=MessageBus)
        bus.dispatch = AsyncMock()

        return bus

    def test_init_when_called_then_set_message_bus(self, message_bus: MagicMock) -> None:
        sender = CommandSender(message_bus)

        assert sender._message_bus == message_bus

    async def test_send_when_called_then_call_message_bus_dispatch_with_given_command(
        self, message_bus: MagicMock
    ) -> None:
        command = FakeCommand()
        sender = CommandSender(message_bus)

        await sender.send(command)

        message_bus.dispatch.assert_awaited_with(command)
