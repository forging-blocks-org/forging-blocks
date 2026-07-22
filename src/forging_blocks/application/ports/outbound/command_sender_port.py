"""Outbound port for asynchronously sending commands.

Defines the ``CommandSenderPort`` ABC for dispatching commands via
an external message bus.  Infrastructure implementations determine
delivery semantics.

Responsibilities:
    - Abstract command dispatch from transport details.

Non-Responsibilities:
    - Delivery guarantees (at-least-once, ordering, retries).
    - Serialization or transport concerns.
"""

from abc import abstractmethod

from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.ports import OutboundPort


class CommandSenderPort[CommandPayloadType](
    OutboundPort,
):
    """ABC for dispatching command messages asynchronously.

    Responsibilities:
        - Accept any domain command type and dispatch it asynchronously.
        - Maintain a contract decoupled from any specific transport or
          message bus implementation.

    Non-Responsibilities:
        - Validate command payloads — that belongs to the validation layer.
        - Implement retry, delivery guarantees, or dead-letter handling.
        - Handle registration — registrations happen through a message bus,
          not through this port.
    """

    @abstractmethod
    async def send(self, command: Command[CommandPayloadType]) -> None:
        """Send a command asynchronously.

        Args:
            command: The command instance to dispatch.

        """
