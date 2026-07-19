"""Event store port for event-sourced aggregates.

Defines the ``EventStorePort`` protocol for appending and retrieving
domain events. The interface is agnostic of storage backend — in-memory,
relational, or event-native implementations are all supported.
"""

from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from forging_blocks.application.errors.event_store_error import EventStoreError
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.ports import OutboundPort
from forging_blocks.foundation.result import Result


class EventStorePort[EventPayloadType, EventResultType](
    OutboundPort[Event[EventPayloadType], EventResultType],
    Protocol,
):
    """Protocol for event stores that persist and retrieve domain events.

    Implementations must handle:
      - Appending new events to an event stream.
      - Retrieving events within an optional version range.
      - Tracking the current version of each event stream.
      - Optimistic concurrency via ``expected_version``.
    """

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

    async def get_current_version(self, aggregate_id: UUID) -> Result[int, EventStoreError]:
        """Retrieve the current version of an aggregate's event stream.

        Args:
            aggregate_id: The aggregate identifier.

        Returns:
            A ``Result`` containing the latest version number (0 for empty
            streams) on success, or an ``EventStoreError`` on failure.
        """
        ...
