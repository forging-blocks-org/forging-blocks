"""Module defining the base Event class for domain events."""

from abc import abstractmethod
from datetime import datetime
from typing import Any, TypeVar

from building_blocks.domain.messages.message import Message

EventRawType = TypeVar("EventRawType", covariant=True)


class Event(Message[EventRawType]):
    """Base class for all domain events.

    Domain events represent something significant that happened in the domain.
    They are immutable facts about the past that other parts of the system can react to.

    Events are named in past tense (e.g., OrderCreated, CustomerRegistered,
    PaymentProcessed).

    Example:
        >>> class OrderCreated(Event):
        ...     def __init__(
        ...         self,
        ...         order_id: str,
        ...         customer_id: str,
        ...         total: float,
        ...         metadata: MessageMetadata | None = None
        ...     ):
        ...         super().__init__(metadata)
        ...         self._order_id = order_id
        ...         self._customer_id = customer_id
        ...         self._total = total
        ...
        ...     @property
        ...     def order_id(self) -> str:
        ...         return self._order_id
        ...
        ...     @property
        ...     def customer_id(self) -> str:
        ...         return self._customer_id
        ...
        ...     @property
        ...     def total(self) -> float:
        ...         return self._total
        ...
        ...     @property
        ...     def payload(self) -> dict[str, Any]:
        ...         return {
        ...             "order_id": self._order_id,
        ...             "customer_id": self._customer_id,
        ...             "total": self._total
        ...         }
    """

    @property
    def occurred_at(self) -> datetime:
        """Get the timestamp when this event occurred.

        Returns:
            datetime: When the event occurred (UTC timezone)
        """
        return self.created_at

    @property
    @abstractmethod
    def _payload(self) -> dict[str, Any]:
        """Get the domain-specific data carried by this event.

        Returns:
            dict[str, object]: The event payload as a dictionary
        """
        pass
