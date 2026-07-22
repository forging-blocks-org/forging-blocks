from typing import Any, Generic, TypeVar

from forging_blocks.application.ports.inbound.message_handler_port import MessageHandlerPort
from forging_blocks.application.ports.outbound.message_bus_port import MessageBusPort
from forging_blocks.foundation.messages.command import Command

CommandType = TypeVar("CommandType", bound=Command[Any], contravariant=True)


class ReleaseCommandBus(MessageBusPort[CommandType, None], Generic[CommandType]):
    """Outbound port for registering message handlers and publishing release-related commands.
    A ReleaseCommandBus routes messages to their respective handlers and
    publishes domain command asynchronously.
    """

    async def register[CT: Command[Any]](
        self, command_type: type[CT], handler: MessageHandlerPort[CT, None]
    ) -> None:
        """Register a message handler for a specific message type.

        Args:
            message: The message type to handle.
            handler: The handler responsible for processing the message.

        Notes:
            - Handlers should be asynchronous.
            - Registration is typically done at application startup.
        """

    async def send(self, message: CommandType) -> None:
        """Publish a release-related domain command.

        Args:
            command: The domain command to publish.

        Notes:
            - Asynchronous and fire-and-forget.
            - Delivery reliability depends on the CommandBus implementation.
        """
