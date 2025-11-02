"""Event publisher module.

Auto-generated minimal module docstring.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from building_blocks.domain.messages.event import Event

TEvent = TypeVar("TEvent", bound=Event)


class AsyncEventPublisher(ABC, Generic[TEvent]):
    """Asynchronous outbound port for publishing events.

    This interface defines the contract for publishing domain events in a
    CQRS architecture. It is designed to be implemented by event bus or
    message broker services, allowing for asynchronous event handling and
    decoupling of components.
    Perfect for:
    - Event-driven architectures
    - Decoupling domain logic from event handling
    - Implementing event sourcing patterns
    - Integrating with message brokers or event buses
    """

    @abstractmethod
    async def publish(self, event: TEvent) -> None:
        """Publish an event synchronously.

        Args:
            event: The domain event to be published.
        """


class SyncEventPublisher(ABC, Generic[TEvent]):
    """Synchronous outbound port for publishing events.

    This interface defines the contract for publishing domain events in a
    CQRS architecture. It is designed to be implemented by event bus or
    message broker services, allowing for asynchronous event handling and
    decoupling of components.
    Perfect for:
    - Event-driven architectures
    - Decoupling domain logic from event handling
    - Implementing event sourcing patterns
    - Integrating with message brokers or event buses
    """

    @abstractmethod
    def publish(self, event: TEvent) -> None:
        """Publish an event asynchronously.

        Args:
            event: The domain event to be published.
        """
