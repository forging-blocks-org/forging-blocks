from typing import Generic, Protocol, TypeVar

from building_blocks.domain.messages.command import Command
from building_blocks.domain.messages.event import Event
from building_blocks.domain.messages.message import Message
from building_blocks.domain.messages.query import Query

TMessage = TypeVar("TMessage", contravariant=True, bound=Message)
TMessageHandlerResult = TypeVar("TMessageHandlerResult", covariant=True)
TQueryResult = TypeVar("TQueryResult", covariant=True)


class MessageHandler(Protocol, Generic[TMessage, TMessageHandlerResult]):
    """
    Inbound port for handling messages asynchronously.

    This interface defines the contract for handling messages in a CQRS
    architecture. It is designed to be implemented by message handlers that
    process incoming messages and perform the necessary actions.

    Perfect for:
    - Command handlers
    - Query handlers (later. this should return a value)
    - Event handlers
    - Any other message processing logic
    """

    async def handle(self, message: TMessage) -> TMessageHandlerResult:
        """
        Handle a message asynchronously.

        Args:
            message: The message to be handled.
        """
        ...


CommandHandler = MessageHandler[Command, None]
QueryHandler = MessageHandler[Query, TQueryResult]
EventHandler = MessageHandler[Event, None]
