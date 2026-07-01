"""Message-bus-backed CommandSenderPort adapter.

Delegates command dispatch to an injected ``MessageBusPort``.
"""

from forging_blocks.application.ports.outbound.message_bus import MessageBusPort
from forging_blocks.foundation.messages.command import Command


class MessageBusCommandSender[CommandPayloadType]:
    """Infrastructure adapter that sends commands via a ``MessageBusPort``.

    Implements ``CommandSenderPort`` by delegating ``send`` to
    ``MessageBusPort.dispatch``.
    """

    def __init__(self, message_bus: MessageBusPort[Command[CommandPayloadType], None]) -> None:
        self._message_bus = message_bus

    async def send(self, command: Command[CommandPayloadType]) -> None:
        """Send a command asynchronously via the message bus."""
        await self._message_bus.dispatch(command)
