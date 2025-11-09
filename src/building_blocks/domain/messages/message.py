"""Message module for domain messaging patterns.

This module provides the base Message class and MessageMetadata for implementing
domain messages following Domain-Driven Design (DDD) and CQRS principles.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, TypeVar
from uuid import UUID, uuid4

from building_blocks.domain.value_object import ValueObject


def now() -> datetime:
    """Get the current UTC datetime."""
    return datetime.now(timezone.utc)


MessageRawType = TypeVar("MessageRawType", covariant=True)


class MessageMetadata(ValueObject[dict[str, Any]]):
    """Metadata associated with domain messages.

    Contains infrastructure-level information about messages such as:
    - Unique message identifier
    - When the message was created
    - correlation_id is used to trace related messages across systems.
    - correlation_id is used to link messages that belong to the same business process.
    - causation_id is used to identify the immediate predecessor message that caused

    This separation allows messages to focus on domain data while keeping
    infrastructure concerns in metadata.

    Example:
        >>> metadata = MessageMetadata(message_type="OrderCreated")
        >>> # Or with custom values
        >>> custom_metadata = MessageMetadata(
        ...     message_type="UserCreated",
        ...     message_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        ...     created_at=datetime(2025, 6, 11, 19, 36, 6, tzinfo=timezone.utc)
        ... )
    """

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
        self._message_type = message_type
        self._message_id = message_id or uuid4()
        self._created_at = created_at or now()
        self._correlation_id = correlation_id or uuid4()
        self._causation_id = causation_id or uuid4()

    @property
    def message_id(self) -> UUID:
        """Get the unique identifier for this message.

        Returns:
            The unique message identifier.
        """
        return self._message_id

    @property
    def message_type(self) -> str:
        """Get the type of this message.

        Returns:
            The message type name.
        """
        return self._message_type

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
    def value(self) -> dict[str, Any]:
        """Get the raw dictionary representation of the metadata."""
        return {
            "created_at": self._created_at.isoformat(),
            "correlation_id": str(self._correlation_id),
            "causation_id": str(self._causation_id),
            "message_id": str(self._message_id),
            "message_type": self._message_type,
        }

    @classmethod
    def create(cls, message_type: str) -> MessageMetadata:
        """Factory for creating a new metadata instance with a given type.

        Args:
            message_type: The type/name of the message.

        Returns:
            A new MessageMetadata instance with generated ID and current timestamp.
        """
        return cls(message_type=message_type)

    def to_dict(self) -> dict[str, Any]:
        """Convert metadata to dictionary representation.

        Returns:
            Dictionary representation of the metadata.
        """
        return self.value

    def _equality_components(self) -> tuple[Any, ...]:
        """Message metadata equality is based on message ID and timestamp.

        Returns:
            Tuple containing message_id and created_at.
        """
        return (self._message_id, self._created_at)


class Message(ValueObject[MessageRawType], ABC):
    """Base class for all domain messages.

    Messages are immutable value objects that represent intent or facts in the domain.
    This is the base class for Events (something that happened) and Commands
    (something to do).

    Features:
    - Immutable by design (inherits from ValueObject)
    - Contains MessageMetadata for infrastructure concerns
    - Focus on domain data in subclasses
    - Each message instance is unique (based on metadata.message_id)

    This class should not be used directly. Use Event or Command instead.
    """

    def __init__(self, metadata: MessageMetadata | None = None) -> None:
        """Initialize the message with metadata.

        Args:
            metadata: Message metadata. If None, creates new metadata with
                generated ID and current timestamp.
        """
        effective_type = self.__class__.__name__
        self._metadata = metadata or MessageMetadata(message_type=effective_type)

    def __eq__(self, other: Any) -> bool:
        """Check equality based on _equality_components."""
        if not isinstance(other, Message):
            return False
        return self._equality_components() == other._equality_components()

    def __hash__(self) -> int:
        return hash(self._equality_components())

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
    def _payload(self) -> dict[str, Any]:
        """Get the domain-specific data carried by this message.

        Subclasses must implement this property to provide their specific message
        data. This makes the Message class truly abstract.

        Returns:
            The message payload.
        """
        pass

    def to_dict(self) -> dict[str, Any]:
        """Convert the message to a dictionary representation.

        Combines metadata, message type, and domain data.

        Returns:
            Complete dictionary representation of the message.
        """
        return {
            "metadata": self._metadata.to_dict(),
            "payload": self._payload,
        }

    def _equality_components(self) -> tuple[Any, ...]:
        """Messages are equal if they have the same message ID.

        Each message instance is unique, even if they have the same domain data.

        Returns:
            Tuple containing the message ID for equality comparison.
        """
        return (self._metadata.message_id,)
