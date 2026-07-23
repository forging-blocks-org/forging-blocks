"""Module defining the base Event class for events."""

from abc import abstractmethod
from datetime import datetime

from forging_blocks.foundation.messages.message import Message


class Event[RawEventType](Message[RawEventType]):
    """Base class for all events.

    Events represent something significant that happened in the system.
    They are immutable facts about the past that other parts of the system can react to.

    Events are named in past tense (e.g., OrderCreated, CustomerRegistered,
    PaymentProcessed).


    Example:
        ```python
        class OrderCreated(Event[dict[str, object]]):
            def __init__(self, order_id: str, customer_id: str, total: float):
                super().__init__()
                self._order_id = order_id
                self._customer_id = customer_id
                self._total = total

            @property
            def _payload(self) -> dict[str, object]:
                return {
                    "order_id": self._order_id,
                    "customer_id": self._customer_id,
                    "total": self._total,
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
        """Retrieve the event's payload as a dictionary.

        Subclasses MUST implement this property to return the event-specific
        data.
        """
