"""Outbound port defining the MessageBus abstraction.

A MessageBus provides a generic asynchronous dispatch mechanism for commands,
queries, or events. It is the central connector between application ports and
transport infrastructure (queues, brokers, in-memory routing, etc.).

Responsibilities:
    - Route messages of various types to their respective handlers or transports.
    - Provide an asynchronous dispatch API.

Non-Responsibilities:
    - Business logic.
    - Handler invocation policies unless explicitly implemented.
    - Delivery guarantees (up to infrastructure).
"""

from typing import Protocol, TypeVar

from forging_blocks.foundation import OutboundPort

MessageType = TypeVar("MessageType", contravariant=True)
MessageBusResultType = TypeVar("MessageBusResultType", covariant=True)


class MessageBus(OutboundPort[MessageType, MessageBusResultType], Protocol):
    """Outbound port representing a generic asynchronous message bus.

    A MessageBus dispatches messages to infrastructure or internal handlers.
    Implementations vary from simple function routers to networked brokers.
    """

    async def dispatch(self, message: MessageType) -> MessageBusResultType:
        """Dispatch a message to the configured handler or transport.

        Args:
            message: The message instance to dispatch.

        Returns:
            A typed result depending on the nature of the message.

        Notes:
            Infrastructure determines:
                - routing strategy,
                - reliability,
                - ordering,
                - concurrency model.
        """
        ...
