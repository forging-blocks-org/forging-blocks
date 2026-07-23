"""MessageMetadata value object for messaging patterns."""

from datetime import datetime, timezone
from uuid import UUID, uuid7

from forging_blocks.foundation.value_object import ValueObject


class MessageMetadata(ValueObject[dict[str, object]]):
    """Metadata associated with foundational messages.

    Contains technical-level information about messages such as:
    - Unique message identifier
    - When the message was created
    - correlation_id is used to trace related messages across systems
      and link messages that belong to the same business process.
    - causation_id is used to identify the immediate predecessor message that caused
      this message.

    This separation allows messages to focus on foundational data while keeping
    infrastructure handling concerns in metadata without needing to understand anything about
    infrastructure rules.

    Example:
        ```python
        metadata = MessageMetadata(message_type="OrderCreated")

        # Or with custom values
        custom_metadata = MessageMetadata(
            message_type="UserCreated",
            message_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            created_at=datetime(2025, 6, 11, 19, 36, 6, tzinfo=timezone.utc),
        )
        ```

    """

    __slots__ = (
        "_message_type",
        "_message_id",
        "_created_at",
        "_correlation_id",
        "_causation_id",
    )

    def __init__(
        self,
        message_type: str,
        message_id: UUID | None = None,
        created_at: datetime | None = None,
        correlation_id: UUID | None = None,
        causation_id: UUID | None = None,
    ) -> None:
        """Initialize message metadata.

        Args:
            message_type: The type/name of the message.
            message_id: Unique identifier for the message. If None, generates a
                new UUID.
            created_at: When the message was created. If None, uses current UTC time.
            correlation_id: Identifier to correlate related messages. If None,
                generates a new UUID.
            causation_id: Identifier of the message that caused this one. If None,
                generates a new UUID.

        """
        super().__init__()
        self._message_type = message_type
        self._message_id = message_id if message_id is not None else uuid7()
        self._created_at = created_at if created_at is not None else datetime.now(timezone.utc)
        self._correlation_id = correlation_id if correlation_id is not None else uuid7()
        self._causation_id = causation_id if causation_id is not None else uuid7()

    @property
    def message_id(self) -> UUID:
        """Get the unique identifier for this message.

        Returns:
            The unique message identifier.

        """
        return self._message_id

    @property
    def causation_id(self) -> UUID:
        """Get the causation ID for this message.

        Returns:
            The causation identifier.

        """
        return self._causation_id

    @property
    def created_at(self) -> datetime:
        """Get the timestamp when this message was created.

        Returns:
            The timestamp (preserved as given when provided, or the
            current UTC time when defaulted).

        """
        return self._created_at

    @property
    def correlation_id(self) -> UUID:
        """Get the correlation ID for this message.

        Returns:
            The correlation identifier.

        """
        return self._correlation_id

    @property
    def message_type(self) -> str:
        """Get the type of this message.

        Returns:
            The message type name.

        """
        return self._message_type

    @property
    def value(self) -> dict[str, object]:
        """Get the raw dictionary representation of the metadata."""
        return {
            "created_at": self._created_at.isoformat(),
            "correlation_id": str(self._correlation_id),
            "causation_id": str(self._causation_id),
            "message_id": str(self._message_id),
            "message_type": self._message_type,
        }
