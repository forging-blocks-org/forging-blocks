"""Outbound port for asynchronously sending commands.

This module defines a CommandSenderPort, an application-blocks abstraction for
dispatching commands via an external message bus. It decouples command
issuance from transport details and message broker implementations.

Responsibilities:
    - Forward commands to an injected MessageBusPort.
    - Abstract message dispatch mechanism.

Non-Responsibilities:
    - Delivery guarantees (at-least-once, ordering, retries).
    - Serialization or transport concerns.
"""

from forging_blocks.application.ports.outbound.message_bus import MessageBusPort
from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.ports import OutboundPort


class CommandSenderPort[CommandPayloadType](OutboundPort[Command[CommandPayloadType], None]):
    """Outbound port for asynchronously sending command messages.

    The CommandSenderPort delegates message dispatching to a MessageBusPort. It is
    typically used by use cases or handlers that need to trigger command-side
    operations in other parts of the system.
    """

    def __init__(self, message_bus: MessageBusPort[Command[CommandPayloadType], None]) -> None:
        self._message_bus = message_bus

    async def send(self, command: Command[CommandPayloadType]) -> None:
        """Send a command asynchronously.

        Args:
            command: The command instance to dispatch.

        Notes:
            - This operation is fire-and-forget from the application's
              perspective.
            - Delivery semantics depend on the underlying MessageBusPort
              implementation.
        """
        await self._message_bus.dispatch(command)
