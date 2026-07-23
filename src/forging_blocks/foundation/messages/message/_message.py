"""Base Message class for messaging patterns."""

import inspect
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Self
from uuid import UUID

from forging_blocks.foundation.autofreeze import auto_freeze

from ._metadata import MessageMetadata


class Message[MessageRawType](ABC):
    """Base class for all foundation messages.

    Messages represent intent or facts in the application.  This is the
    base class for Commands (something to do), Events (something that
    happened), and Queries (something to obtain).

    Messages are immutable and each instance is unique -- equality is
    determined solely by the ``message_id`` carried in
    :class:`MessageMetadata`.

    This class should not be used directly.  Import :class:`Event` or
    :class:`Command` instead.
    """

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Automatically apply ``auto_freeze`` to concrete subclasses."""
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            auto_freeze(cls)

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
        """Compare messages by message ID.

        Two messages are equal if and only if they have the same
        ``message_id``.  All other fields (payload, timestamp, causation)
        are ignored for equality.
        """
        if type(self) is not type(other):
            return False
        return self.message_id == other.message_id  # type: ignore[union-attr]

    def __hash__(self) -> int:
        return hash(self.message_id)

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
    @abstractmethod
    def value(self) -> MessageRawType:
        """Return the raw message payload as a single value."""
