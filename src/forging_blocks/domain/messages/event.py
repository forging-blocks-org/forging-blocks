"""Module defining the base Event class for events."""

from abc import abstractmethod
from datetime import datetime

from forging_blocks.domain.messages.message import Message


class Event[RawEventType](Message[RawEventType]):
    """Base class for all events.

    Events represent something significant that happened in the system.
    They are immutable facts about the past that other parts of the system can react to.

    Events are named in past tense (e.g., OrderCreated, CustomerRegistered,
    PaymentProcessed).


    Example:
        ```python
        from forging_blocks.domain.messages.decorators import event_dataclass


        @event_dataclass
        class OrderCreated:
            order_id: str
            customer_id: str
            total: float


        event = OrderCreated(
            order_id="order-1",
            customer_id="customer-1",
            total=99.95,
        )

        assert isinstance(event, Event)
        assert event.occurred_at == event.created_at
        assert event.get_payload_fields() == {
            "order_id": "order-1",
            "customer_id": "customer-1",
            "total": 99.95,
        }
        ```

    """

    @property
    def occurred_at(self) -> datetime:
        """Get the timestamp when this event occurred (UTC timezone)."""
        return self.created_at

    @property
    @abstractmethod
    def _payload(self) -> RawEventType:
        """Return the event-specific payload data.

        Subclasses MUST implement this property to return the event-specific
        data.
        """
