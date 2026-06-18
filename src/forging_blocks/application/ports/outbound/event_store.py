"""Event store port for event-sourced aggregates.

Defines the ``EventStore`` abstract interface for appending and retrieving
domain events. The interface is agnostic of storage backend — in-memory,
relational, or event-native implementations are all supported.
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.result import Result


class EventStoreError(Exception):
    """Base error for event store operations."""


class ConcurrencyError(EventStoreError):
    """Raised when an optimistic concurrency check fails.

    Attributes:
        aggregate_id: The aggregate that experienced the conflict.
        expected_version: The version the caller expected.
        actual_version: The version currently stored.
    """

    def __init__(self, aggregate_id: UUID, expected_version: int, actual_version: int) -> None:
        self.aggregate_id = aggregate_id
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"Concurrency conflict for aggregate {aggregate_id}: "
            f"expected version {expected_version}, actual {actual_version}"
        )


class EventStore[EventPayloadType](ABC):
    """Abstract event store for appending and retrieving domain events.

    Implementations must handle:
      - Appending new events to an event stream.
      - Retrieving events within an optional version range.
      - Tracking the current version of each event stream.
      - Optimistic concurrency via ``expected_version``.
    """

    @abstractmethod
    async def append_events(
        self,
        aggregate_id: UUID,
        events: Sequence[Event[EventPayloadType]],
        expected_version: int | None = None,
    ) -> Result[int, EventStoreError]:
        """Append events to an aggregate's event stream.

        Args:
            aggregate_id: The aggregate identifier.
            events: The domain events to append.
            expected_version: Expected current version for optimistic
                concurrency. ``None`` means skip the check.

        Returns:
            A ``Result`` containing the new stream version on success or an
            ``EventStoreError`` on failure.
        """
        ...

    @abstractmethod
    async def get_events(
        self,
        aggregate_id: UUID,
        from_version: int | None = None,
        to_version: int | None = None,
    ) -> Result[Sequence[Event[EventPayloadType]], EventStoreError]:
        """Retrieve events from an aggregate's event stream.

        Args:
            aggregate_id: The aggregate identifier.
            from_version: Start version (inclusive). ``None`` means from
                the beginning.
            to_version: End version (inclusive). ``None`` means until
                the end.

        Returns:
            A ``Result`` containing the events on success or an
            ``EventStoreError`` on failure.
        """
        ...

    @abstractmethod
    async def get_current_version(self, aggregate_id: UUID) -> Result[int, EventStoreError]:
        """Retrieve the current version of an aggregate's event stream.

        Args:
            aggregate_id: The aggregate identifier.

        Returns:
            A ``Result`` containing the latest version number (0 for empty
            streams) on success, or an ``EventStoreError`` on failure.
        """
        ...
