"""Module defining the Command base class for commands."""

from datetime import datetime
from uuid import UUID

from forging_blocks.domain.messages.message import Message


class Command[RawCommandType](Message[RawCommandType]):
    """Base class for all commands.

    Commands represent an intent to do something in the system.
    They are requests that may succeed or fail, and are handled by a command handler.

    Commands are named in imperative mood (e.g., CreateOrder, RegisterCustomer,
    ProcessPayment).


    Example:
        ```python
        from forging_blocks.domain.messages.decorators import command_dataclass


        @command_dataclass
        class CreateOrder:
            customer_id: str
            items: tuple[str, ...]


        command = CreateOrder(
            customer_id="customer-1",
            items=("coffee", "tea"),
        )

        assert isinstance(command, Command)
        assert command.command_id == command.message_id
        assert command.get_payload_fields() == {
            "customer_id": "customer-1",
            "items": ("coffee", "tea"),
        }
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
