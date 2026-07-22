"""Module defining the Command base class for domain commands."""

from datetime import datetime
from uuid import UUID

from forging_blocks.foundation.messages.message import Message


class Command[RawCommandType](Message[RawCommandType]):
    """Base class for all domain commands.

    Commands represent an intent to do something in the domain.
    They are requests that may succeed or fail, and are handled by a command handler.

    Commands are named in imperative mood (e.g., CreateOrder, RegisterCustomer,
    ProcessPayment).

    Example:
        ```python
        class CreateOrder(Command[dict[str, object]]):
            def __init__(
                self, customer_id: str, items: list, metadata: MessageMetadata | None = None
            ):
                super().__init__(metadata)
                self._customer_id = customer_id
                self._items = items

            @property
            def _payload(self) -> dict[str, object]:
                return {"customer_id": self._customer_id, "items": self._items}
        ```

    """

    @property
    def command_id(self) -> UUID:
        """Get the unique identifier for this command (same as message_id)."""
        return self.message_id

    @property
    def issued_at(self) -> datetime:
        """Get the timestamp when this command was issued (same as created_at)."""
        return self.created_at
