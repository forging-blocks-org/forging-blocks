from typing import Generic, Protocol, TypeVar

from forging_blocks.application.ports.inbound.message_handler import CommandHandler
from forging_blocks.application.ports.outbound.message_bus import MessageBus
from forging_blocks.domain.messages.command import Command


CommandType = TypeVar("CommandType", bound=Command, contravariant=True)

class ReleaseCommandBus(MessageBus[CommandType, None], Generic[CommandType], Protocol):
    """
    Outbound port for registering message handlers and publishing release-related commands.
    A ReleaseCommandBus routes messages to their respective handlers and
    publishes domain command asynchronously.
    """
    async def register(self, command_type: type[Command], handler: CommandHandler) -> None:
        """Register a message handler for a specific message type.
        Args:
            message: The message type to handle.
            handler: The handler responsible for processing the message.
        Notes:
            - Handlers should be asynchronous.
            - Registration is typically done at application startup.
        """
        ...

    async def send(self, message: CommandType) -> None:
        """Publish a release-related domain command.

        Args:
            command: The domain command to publish.
        Notes:
            - Asynchronous and fire-and-forget.
            - Delivery reliability depends on the CommandBus implementation.
        """
        ...
