"""Outbound port for asynchronously sending commands.

Defines the ``CommandSenderPort`` protocol for dispatching commands via
an external message bus.  Infrastructure implementations determine
delivery semantics.

Responsibilities:
    - Abstract command dispatch from transport details.

Non-Responsibilities:
    - Delivery guarantees (at-least-once, ordering, retries).
    - Serialization or transport concerns.
"""

from typing import Protocol, runtime_checkable

from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.ports import OutboundPort


@runtime_checkable
class CommandSenderPort[CommandPayloadType](
    OutboundPort[Command[CommandPayloadType], None],
    Protocol,
):
    """Protocol for dispatching command messages asynchronously.

    Any object with an async ``send`` method that accepts a ``Command``
    satisfies this protocol — no inheritance required.
    """

    async def send(self, command: Command[CommandPayloadType]) -> None:
        """Send a command asynchronously.

        Args:
            command: The command instance to dispatch.
        """
        ...
