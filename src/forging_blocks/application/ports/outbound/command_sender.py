"""Outbound port for asynchronously sending commands.

This module defines a CommandSender, an application-layer abstraction for
dispatching commands via an external message bus. It decouples command
issuance from transport details and message broker implementations.

Responsibilities:
    - Forward commands to an injected MessageBus.
    - Abstract message dispatch mechanism.

Non-Responsibilities:
    - Delivery guarantees (at-least-once, ordering, retries).
    - Serialization or transport concerns.
"""

from forging_blocks.application.ports.outbound.message_bus import MessageBus
from forging_blocks.domain.messages.command import Command
from forging_blocks.foundation.ports import OutboundPort


class CommandSender(OutboundPort[Command, None]):
    """Outbound port for asynchronously sending command messages.

    The CommandSender delegates message dispatching to a MessageBus. It is
    typically used by use cases or handlers that need to trigger command-side
    operations in other parts of the system.
    """

    def __init__(self, message_bus: MessageBus[Command, None]) -> None:
        self._message_bus = message_bus

    async def send(self, command: Command) -> None:
        """Send a command asynchronously.

        Args:
            command: The command instance to dispatch.

        Notes:
            - This operation is fire-and-forget from the application's
              perspective.
            - Delivery semantics depend on the underlying MessageBus
              implementation.
        """
        await self._message_bus.dispatch(command)
