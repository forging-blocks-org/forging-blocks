# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
from typing import Any, Self

import pytest

from forging_blocks.domain.messages import Command, MessageMetadata
from forging_blocks.infrastructure import MessageBusCommandSender
from tests.fixtures.fake_message_bus import FakeMessageBus


class FakeCommand(Command[str]):
    @property
    def value(self) -> str:
        return "foo"

    def _payload(self) -> dict[str, Any]:  # type: ignore[override]
        return {"foo": "foo"}

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls()


@pytest.mark.integration
class TestMessageBusCommandSender:
    """Integration tests for the MessageBusCommandSender adapter."""

    @pytest.fixture
    def fake_bus(self) -> FakeMessageBus:
        return FakeMessageBus()

    @pytest.fixture
    def sender(self, fake_bus: FakeMessageBus) -> MessageBusCommandSender:
        return MessageBusCommandSender(fake_bus)

    @pytest.fixture
    def command(self) -> FakeCommand:
        return FakeCommand()

    def test_init_when_called_then_stores_message_bus(self, fake_bus: FakeMessageBus) -> None:
        sender = MessageBusCommandSender(fake_bus)

        assert sender._message_bus is fake_bus

    async def test_send_when_called_then_delegates_to_message_bus_dispatch(
        self, sender: MessageBusCommandSender, command: FakeCommand, fake_bus: FakeMessageBus
    ) -> None:
        await sender.send(command)

        assert len(fake_bus.dispatched_messages) == 1
        assert fake_bus.dispatched_messages[0] is command

    def test_implements_command_sender_port(self) -> None:
        """MessageBusCommandSender satisfies the CommandSenderPort protocol."""
        assert hasattr(MessageBusCommandSender, "send")
