"""Base Message class for messaging patterns."""

from abc import ABC, abstractmethod
from collections.abc import Hashable
from datetime import datetime
from typing import Self
from uuid import UUID

from forging_blocks.foundation.value_object import ValueObject

from ._metadata import MessageMetadata


class Message[MessageRawType](ValueObject[MessageRawType], ABC):
    """Base class for all foundation messages.

    Messages are immutable value objects that represent intent or facts in the application.
    This is the base class for Commands (something to do), Events (something that happened),
    and Queries (something to obtain).

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
    def _payload(self) -> MessageRawType:
        """Get the data carried by this message.

        Subclasses must implement this property to provide their specific message
        data. This makes the Message class truly abstract.

        Returns:
            The message payload.

        """

    @classmethod
    @abstractmethod
    def from_payload_fields(
        cls,
        data: MessageRawType,
        metadata: MessageMetadata,
    ) -> Self:
        """Reconstruct a message instance from payload fields and metadata.

        Abstract classmethod that subclasses must implement.  The
        ``@message_dataclass`` decorator provides a concrete implementation
        automatically; manual subclasses that need codec support must override
        this method themselves.

        Returns:
            A new message instance reconstructed from the given payload
            fields and metadata.

        """

    @property
    def _equality_components(self) -> tuple[Hashable, ...]:
        """Messages are equal if they have the same message ID.

        Each message instance is unique, even if they have the same data.

        Returns:
            Tuple containing the message ID for equality comparison.

        """
        return (self._metadata.message_id,)
