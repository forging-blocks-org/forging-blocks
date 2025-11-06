"""Outbound port for sending commands asynchronously."""

from building_blocks.application.ports.outbound.message_bus import MessageBus
from building_blocks.domain.messages.command import Command


class CommandSender:
    """Asynchronous outbound port for sending commands.

    CommandSender is designed to send command messages through a message bus.
    It is ideal for implementing the command side of a CQRS-like architecture.

    This implementation is composed with a MessageBus to delegate the actual message dispatching
    logic.
    """

    def __init__(self, message_bus: MessageBus) -> None:
        self._message_bus = message_bus

    async def send(self, command: Command) -> None:
        """Send a command asynchronously."""
        await self._message_bus.dispatch(command)
