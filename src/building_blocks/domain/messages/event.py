"""Event module.

Auto-generated minimal module docstring.
"""

from datetime import datetime
from uuid import UUID

from building_blocks.domain.messages.message import Message


class Event(Message):
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
        ...         metadata: Optional[MessageMetadata] = None
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
        ...     def payload(self) -> Dict[str, Any]:
        ...         return {
        ...             "order_id": self._order_id,
        ...             "customer_id": self._customer_id,
        ...             "total": self._total
        ...         }
    """

    @property
    def event_id(self) -> UUID:
        """Convenience property to get the event ID.

        Returns:
            UUID: The unique event identifier (same as message_id)
        """
        return self.message_id

    @property
    def occurred_at(self) -> datetime:
        """Convenience property to get when the event occurred.

        Returns:
            datetime: When the event occurred (same as created_at)
        """
        return self.created_at
