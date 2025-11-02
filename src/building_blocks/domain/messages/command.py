"""Command module.

Auto-generated minimal module docstring.
"""

from datetime import datetime
from uuid import UUID

from building_blocks.domain.messages.message import Message


class Command(Message):
    """Base class for all domain commands.

    Commands represent an intent to do something in the domain.
    They are requests that may succeed or fail, and they are handled by command handler.

    Commands are named in imperative mood (e.g., CreateOrder, RegisterCustomer,
    ProcessPayment).

    Example:
        >>> class CreateOrder(Command):
        ...     def __init__(
        ...         self,
        ...         customer_id: str,
        ...         items: list,
        ...         metadata: Optional[MessageMetadata] = None
        ...     ):
        ...         super().__init__(metadata)
        ...         self._customer_id = customer_id
        ...         self._items = items
        ...
        ...     @property
        ...     def customer_id(self) -> str:
        ...         return self._customer_id
        ...
        ...     @property
        ...     def items(self) -> list:
        ...         return self._items
        ...
        ...     @property
        ...     def payload(self) -> dict[str, Any]:
        ...         return {
        ...             "customer_id": self._customer_id,
        ...             "items": self._items
        ...         }
    """

    @property
    def command_id(self) -> UUID:
        """Convenience property to get the command ID.

        Returns:
            UUID: The unique command identifier (same as message_id)
        """
        return self.message_id

    @property
    def issued_at(self) -> datetime:
        """Convenience property to get when the command was issued.

        Returns:
            datetime: When the command was issued (same as created_at)
        """
        return self.created_at
