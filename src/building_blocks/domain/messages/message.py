"""Message module for domain messaging patterns.

This module provides the base Message class and MessageMetadata for implementing
domain messages following Domain-Driven Design (DDD) and CQRS principles.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple
from uuid import UUID, uuid4

from building_blocks.domain.value_object import ValueObject


class MessageMetadata(ValueObject):
    """Metadata associated with domain messages.

    Contains infrastructure-level information about messages such as:
    - Unique message identifier
    - When the message was created
    - Future: correlation ID, causation ID, user context, etc.

    This separation allows messages to focus on domain data while keeping
    infrastructure concerns in metadata.

    Example:
        >>> metadata = MessageMetadata()
        >>> # Or with custom values
        >>> custom_metadata = MessageMetadata(
        ...     message_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        ...     created_at=datetime(2025, 6, 11, 19, 36, 6, tzinfo=timezone.utc)
        ... )
    """

    def __init__(
        self, message_id: Optional[UUID] = None, created_at: Optional[datetime] = None
    ) -> None:
        """Initialize message metadata.

        Args:
            message_id: Uniqu identifier for the message. If None, generates a new UUID.
            created_at: When the message was created. If None, uses current UTC time.
        """
        self._message_id = message_id or uuid4()
        self._created_at = created_at or datetime.now(timezone.utc)

    @property
    def message_id(self) -> UUID:
        """Get the unique identifier for this message.

        Returns:
            UUID: The unique message identifier
        """
        return self._message_id

    @property
    def created_at(self) -> datetime:
        """Get the timestamp when this message was created.

        Returns:
            datetime: When the message was created (UTC timezone)
        """
        return self._created_at

    def _equality_components(self) -> Tuple[Any, ...]:
        """Message metadata equality is based on message ID and timestamp.

        Returns:
            tuple[Any, ...]: Tuple containing message_id and created_at
        """
        return (self._message_id, self._created_at)

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary representation.

        Returns:
            dict[str, Any]: dictionary representation of the metadata
        """
        return {
            "message_id": str(self._message_id),
            "created_at": self._created_at.isoformat(),
        }


class Message(ValueObject, ABC):
    """Base class for all domain messages.

    Messages are immutable value objects that represent intent or facts in the domain.
    This is the base class for Events (something that happened) and Commands (something
    to do).

    Features:
    - Immutable by design (inherits from ValueObject)
    - Contains MessageMetadata for infrastructure concerns
    - Focus on domain data in subclasses
    - Each message instance is unique (based on metadata.message_id)

    This class should not be used directly. Use Event or Command instead.
    """

    def __init__(self, metadata: Optional[MessageMetadata] = None) -> None:
        """Initialize the message with metadata.

        Args:
            metadata: Message metadata. If None, creates new metadata with generated ID
            and current timestamp.
        """
        self._metadata = metadata or MessageMetadata()

    @property
    def metadata(self) -> MessageMetadata:
        """Get the message metadata.

        Returns:
            MessageMetadata: The message metadata containing ID, timestamp, etc.
        """
        return self._metadata

    @property
    def message_id(self) -> UUID:
        """Convenience property to get the message ID.

        Returns:
            UUID: The unique message identifier
        """
        return self._metadata.message_id

    @property
    def created_at(self) -> datetime:
        """Convenience property to get when the message was created.

        Returns:
            datetime: When the message was created
        """
        return self._metadata.created_at

    @property
    def message_type(self) -> str:
        """Get the type of this message.

        Returns the class name of the concrete message implementation.

        Returns:
            str: The message type name (class name)
        """
        return self.__class__.__name__

    @property
    @abstractmethod
    def payload(self) -> Dict[str, Any]:
        """Get the domain-specific data carried by this message.

        Subclasses must implement this property to provide their specific message data.
        This makes the Message class truly abstract.

        Returns:
            dict[str, Any]: The message payload
        """
        pass

    def _equality_components(self) -> Tuple[Any, ...]:
        """Messages are equal if they have the same message ID.

        Each message instance is unique, even if they have the same domain data.

        Returns:
            tuple[Any, ...]: Tuple containing the message ID for equality comparison
        """
        return (self._metadata.message_id,)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the message to a dictionary representation.

        Combines metadata, message type, and domain data.

        Returns:
            dict[str, Any]: Complete dictionary representation of the message
        """
        return {
            **self._metadata.to_dict(),
            "message_type": self.message_type,
            **self.payload,
        }
