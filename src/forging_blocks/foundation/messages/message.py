"""Message module for messaging patterns.

This module provides the base Message class and MessageMetadata for implementing
foundation messages influenced by Domain-Driven Design (DDD) and CQRS principles.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Self, cast
from uuid import UUID, uuid7

from forging_blocks.foundation.value_object import ValueObject


class MessageMetadata(ValueObject[dict[str, object]]):
    """Metadata associated with foundational messages.

    Contains technical-level information about messages such as:
    - Unique message identifier
    - When the message was created
    - correlation_id is used to trace related messages across systems.
    - correlation_id is used to link messages that belong to the same business process.
    - causation_id is used to identify the immediate predecessor message that caused

    This separation allows messages to focus on foundational data while keeping
    infrastructure handling concerns in metadata without foundation understand anything about
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
        self._message_id = message_id or uuid7()
        self._created_at = created_at or datetime.now(timezone.utc)
        self._correlation_id = correlation_id or uuid7()
        self._causation_id = causation_id or uuid7()

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
            When the message was created (UTC timezone).
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

    @property
    def _equality_components(self) -> tuple[object, ...]:
        """Message metadata equality is based on message ID and timestamp.

        Returns:
            Tuple containing message_id and created_at.
        """
        return (self._message_id, self._created_at)

    def to_dict(self) -> dict[str, object]:
        """Convert metadata to dictionary representation.

        Returns:
            Dictionary representation of the metadata.
        """
        return self.value

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> MessageMetadata:
        """Create metadata from a dictionary representation.

        Args:
            data: Dictionary containing the serialised metadata fields.

        Returns:
            A new MessageMetadata instance reconstituted from *data*.
        """
        return cls(
            message_type=str(data["message_type"]),
            message_id=UUID(str(data["message_id"])) if "message_id" in data else None,
            created_at=datetime.fromisoformat(str(data["created_at"]))
            if "created_at" in data
            else None,
            correlation_id=UUID(str(data["correlation_id"])) if "correlation_id" in data else None,
            causation_id=UUID(str(data["causation_id"])) if "causation_id" in data else None,
        )


class Message[MessageRawType](ValueObject[MessageRawType], ABC):
    """Base class for all foundation messages.

    Messages are immutable value objects that represent intent or facts in the application.
    This is the base class for Events (something that happened) and Commands
    (something to do).

    Features:
    - Immutable by design (inherits from ValueObject)
    - Contains MessageMetadata for infrastructure concerns
    - Focus on data in subclasses
    - Each message instance is unique (based on metadata.message_id)

    This class should not be used directly. Use Event or Command instead.
    """

    def __init__(self, metadata: MessageMetadata | None = None) -> None:
        """Initialize the message with metadata.

        Args:
            metadata: Message metadata. If None, creates new metadata with
                generated ID and current timestamp.
        """
        super().__init__()
        effective_type = type(self).__name__
        self._metadata = metadata or MessageMetadata(message_type=effective_type)

    def __eq__(self, other: object) -> bool:
        """Check equality based on _equality_components."""
        if not isinstance(other, Message):
            return False
        return self._equality_components == other._equality_components

    def __hash__(self) -> int:
        return hash(self._equality_components)

    @property
    def metadata(self) -> MessageMetadata:
        """Get the message metadata.

        Returns:
            The message metadata containing ID, timestamp, etc.
        """
        return self._metadata

    @property
    def message_id(self) -> UUID:
        """Convenience property to get the message ID.

        Returns:
            The unique message identifier.
        """
        return self._metadata.message_id

    @property
    def created_at(self) -> datetime:
        """Convenience property to get when the message was created.

        Returns:
            When the message was created.
        """
        return self._metadata.created_at

    @property
    @abstractmethod
    def _payload(self) -> dict[str, object]:
        """Get the data carried by this message.

        Subclasses must implement this property to provide their specific message
        data. This makes the Message class truly abstract.

        Returns:
            The message payload.
        """
        ...

    @property
    def _equality_components(self) -> tuple[object, ...]:
        """Messages are equal if they have the same message ID.

        Each message instance is unique, even if they have the same data.

        Returns:
            Tuple containing the message ID for equality comparison.
        """
        return (self._metadata.message_id,)

    def to_dict(self) -> dict[str, object]:
        """Convert the message to a dictionary representation.

        Combines metadata, message type, payload, and domain data.

        Returns:
            Complete dictionary representation of the message.
        """
        result: dict[str, object] = {
            "metadata": self._metadata.to_dict(),
            "payload": self._payload,
        }
        result["data"] = self.get_domain_data()
        return result

    def get_domain_data(self) -> dict[str, object]:
        """Return the domain-level data carried by this message.

        The default implementation delegates to ``_payload``. Subclasses
        that use the decorator-based approach (``@event_dataclass`` etc.)
        override this to return only the message fields.

        Returns:
            Dictionary of domain data fields.
        """
        return self._payload

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Create a message instance from a dictionary representation.

        Args:
            data: Dictionary containing the serialised message.

        Returns:
            A new message instance reconstituted from *data*.
        """
        metadata = MessageMetadata.from_dict(cast(dict[str, object], data["metadata"]))
        payload = cast(dict[str, object], data.get("payload", data.get("data", {})))
        return cls._from_domain_data(payload, metadata)

    @classmethod
    def _from_domain_data(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        """Reconstruct a message from domain data and metadata.

        Subclasses override this to provide custom reconstruction logic.
        By default, calls ``_from_payload_fields`` if available, otherwise raises
        ``NotImplementedError``.

        Args:
            data: The domain data dictionary.
            metadata: The message metadata.

        Returns:
            A new message instance.

        Raises:
            NotImplementedError: If the subclass has not overridden this method or
                does not have a ``_from_payload_fields`` method.
        """

        method = getattr(cls, "_from_payload_fields", None)
        if method is not None:
            return cast(Callable[..., Self], method)(data, metadata)
        raise NotImplementedError
