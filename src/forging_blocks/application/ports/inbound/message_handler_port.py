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

from abc import abstractmethod

from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.query import Query
from forging_blocks.foundation.ports import InboundPort


class MessageHandlerPort[MessageType, MessageHandlerResultType](
    InboundPort,
):
    """Inbound port for handling messages asynchronously.

    A MessageHandlerPort defines the contract for processing a single message
    and producing a typed result. Implementations must avoid infrastructure
    dependencies and remain purely application-blocks logic.

    Implementers typically:
        - Validate or transform the incoming message.
        - Orchestrate domain operations.
        - Invoke repositories, outbound ports, and publish domain events.
    """

    @abstractmethod
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


class CommandHandlerPort[CommandPayloadType](
    MessageHandlerPort[Command[CommandPayloadType], None],
):
    """Inbound port for handling commands asynchronously."""


class QueryHandlerPort[QueryPayloadType, QueryResultType](
    MessageHandlerPort[Query[QueryPayloadType], QueryResultType],
):
    """Inbound port for handling queries asynchronously."""


class EventHandlerPort[EventPayloadType](
    MessageHandlerPort[Event[EventPayloadType], None],
):
    """Inbound port for handling events asynchronously."""
