"""Inbound message-handling ports for the application blocks.

This module defines the contract for handling application messages
(commands, queries, and domain events). Message handlers sit at the
application boundary and orchestrate domain logic by invoking domain
services, aggregates, value objects, and outbound ports.

Responsibilities:
    - Process an incoming message of a specific type.
    - Delegate work to domain logic and outbound ports.
    - Execute asynchronously.

Non-Responsibilities:
    - Infrastructure concerns (transport, serialization, queues).
    - Transaction management (handled externally, e.g., by Unit of Work).
    - Persistence (handled by repositories).
"""

from typing import Any, Protocol, TypeAlias, TypeVar

from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.message import Message
from forging_blocks.foundation.messages.query import Query
from forging_blocks.foundation.ports import InboundPort

CommandType = TypeVar("CommandType", contravariant=True, bound=Command[Any])
QueryType = TypeVar("QueryType", contravariant=True, bound=Query)
EventType = TypeVar("EventType", contravariant=True, bound=Event[Any])
QueryResultType = TypeVar("QueryResultType", covariant=True)


class MessageHandler[MessageType: Message[Any], MessageHandlerResultType](
    InboundPort[MessageType, MessageHandlerResultType],
    Protocol,
):
    """Inbound port for handling messages asynchronously.

    A MessageHandler defines the contract for processing a single message
    and producing a typed result. Implementations must avoid infrastructure
    dependencies and remain purely application-blocks logic.

    Implementers typically:
        - Validate or transform the incoming message.
        - Orchestrate domain operations.
        - Invoke repositories, outbound ports, and publish domain events.
    """

    async def handle(self, message: MessageType) -> MessageHandlerResultType:
        """Process a message and return an application result.

        Args:
            message: The message instance to handle.

        Returns:
            A value representing the result of the message processing.

        Raises:
            ApplicationError: If processing fails due to business logic violations.

        Notes:
            This method is asynchronous and should not block. Infrastructure
            concerns such as retry logic or message acknowledgment must be
            handled externally.
        """
        ...


CommandHandler: TypeAlias = MessageHandler[CommandType, None]
QueryHandler: TypeAlias = MessageHandler[QueryType, QueryResultType]
EventHandler: TypeAlias = MessageHandler[EventType, None]
