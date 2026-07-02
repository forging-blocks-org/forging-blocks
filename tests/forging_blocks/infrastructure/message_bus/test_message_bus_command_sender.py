# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from typing import Any, Self
from unittest.mock import AsyncMock, MagicMock

import pytest

from forging_blocks.application import MessageBusPort
from forging_blocks.foundation.messages import Command, MessageMetadata
from forging_blocks.infrastructure import MessageBusCommandSender


class FakeCommand(Command[str]):
    @property
    def value(self) -> str:
        return "foo"

    def _payload(self) -> dict[str, Any]:  # type: ignore[override]
        return {"foo": "foo"}

    @classmethod
    def _from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls()


@pytest.mark.integration
class TestMessageBusCommandSender:
    """Integration tests for the MessageBusCommandSender adapter."""

    def test_init_when_called_then_stores_message_bus(self) -> None:
        bus = MagicMock(spec=MessageBusPort)

        sender = MessageBusCommandSender(bus)

        assert sender._message_bus is bus

    async def test_send_when_called_then_delegates_to_message_bus_dispatch(self) -> None:
        bus = MagicMock(spec=MessageBusPort)
        bus.dispatch = AsyncMock()
        sender = MessageBusCommandSender(bus)
        command = FakeCommand()

        await sender.send(command)

        bus.dispatch.assert_awaited_once_with(command)

    def test_implements_command_sender_port(self) -> None:
        """MessageBusCommandSender satisfies the CommandSenderPort protocol."""
        assert hasattr(MessageBusCommandSender, "send")
