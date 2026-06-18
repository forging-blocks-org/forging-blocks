"""In-memory implementation of the EventStore port.

Stores ``Event`` objects in a dictionary keyed by aggregate UUID.
Supports optimistic concurrency via ``expected_version`` checks.

This implementation is suitable for testing and single-process
applications. For persistence, replace with a database-backed
implementation.
"""

from collections.abc import Sequence
from uuid import UUID

from forging_blocks.application.ports.outbound.event_store import (
    ConcurrencyError,
    EventStore,
    EventStoreError,
)
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.result import Result


class InMemoryEventStore[EventPayloadType](EventStore[EventPayloadType]):
    """In-memory event store backed by dictionaries.

    Attributes:
        _streams: Per-aggregate ordered event lists.
        _versions: Per-aggregate current version counters.
    """

    __slots__ = ("_streams", "_versions")

    def __init__(self) -> None:
        self._streams: dict[UUID, list[Event[EventPayloadType]]] = {}
        self._versions: dict[UUID, int] = {}

    async def append_events(
        self,
        aggregate_id: UUID,
        events: Sequence[Event[EventPayloadType]],
        expected_version: int | None = None,
    ) -> Result[int, EventStoreError]:
        """Append events to an aggregate's stream with optional concurrency check.

        Args:
            aggregate_id: The aggregate identifier.
            events: Events to append.
            expected_version: Expected current version. If provided and
                it does not match the actual version, a ``ConcurrencyError``
                is returned.

        Returns:
            A ``Result`` containing the new stream version.
        """
        current = self._versions.get(aggregate_id, 0)

        if expected_version is not None and current != expected_version:
            return Result.from_err(ConcurrencyError(aggregate_id, expected_version, current))

        stream = self._streams.setdefault(aggregate_id, [])
        stream.extend(events)
        new_version = current + len(events)
        self._versions[aggregate_id] = new_version
        return Result.from_ok(new_version)

    async def get_events(
        self,
        aggregate_id: UUID,
        from_version: int | None = None,
        to_version: int | None = None,
    ) -> Result[Sequence[Event[EventPayloadType]], EventStoreError]:
        """Retrieve events within an optional version range.

        Args:
            aggregate_id: The aggregate identifier.
            from_version: Inclusive start (0-indexed). ``None`` = beginning.
            to_version: Inclusive end (0-indexed). ``None`` = end.

        Returns:
            A ``Result`` containing the matching events.
        """
        stream = self._streams.get(aggregate_id, [])
        start = from_version if from_version is not None else 0
        end = to_version + 1 if to_version is not None else len(stream)
        sliced = stream[start:end]
        return Result.from_ok(sliced)

    async def get_current_version(self, aggregate_id: UUID) -> Result[int, EventStoreError]:
        """Get the current version of an aggregate's stream.

        Args:
            aggregate_id: The aggregate identifier.

        Returns:
            A ``Result`` containing the version number (0 for empty streams).
        """
        return Result.from_ok(self._versions.get(aggregate_id, 0))
