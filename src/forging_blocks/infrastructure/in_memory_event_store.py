"""
In-memory implementation of the EventStorePort port.

This implementation stores events in memory and is suitable for testing
and development purposes.
"""

from collections import defaultdict
from typing import Any, Dict, List, Optional

from forging_blocks.infrastructure.event_store import ConcurrencyError, EventStorePort


class InMemoryEventStore(EventStorePort):
    """
    In-memory implementation of the EventStorePort port.

    Stores events in a dictionary keyed by aggregate ID.
    """

    def __init__(self) -> None:
        self._events: Dict[str, List[dict[str, Any]]] = defaultdict(list)
        self._snapshots: Dict[str, Dict[int, dict[str, Any]]] = defaultdict(dict)

    async def save_events(
        self,
        aggregate_id: str,
        events: List[dict[str, Any]],
        expected_version: Optional[int] = None,
    ) -> None:
        """
        Save a list of events for an aggregate.

        Args:
            aggregate_id: The unique identifier of the aggregate.
            events: The list of events to save.
            expected_version: The expected version of the aggregate.

        Raises:
            ConcurrencyError: If the expected version does not match the current version.
        """
        current_version = len(self._events[aggregate_id])

        if expected_version is not None and current_version != expected_version:
            raise ConcurrencyError(
                f"Concurrency conflict for aggregate {aggregate_id}: "
                f"expected version {expected_version}, but current version is {current_version}"
            )

        for event in events:
            event["version"] = current_version + 1
            event["aggregate_id"] = aggregate_id
            self._events[aggregate_id].append(event)
            current_version += 1

    async def get_events(
        self,
        aggregate_id: str,
        from_version: Optional[int] = None,
        to_version: Optional[int] = None,
    ) -> list[dict[str, object]]:
        """
        Retrieve events for an aggregate.

        Args:
            aggregate_id: The unique identifier of the aggregate.
            from_version: The starting version (inclusive).
            to_version: The ending version (inclusive).

        Returns:
            A list of events.
        """
        events = self._events.get(aggregate_id, [])

        if from_version is not None:
            events = [e for e in events if e.get("version", 0) >= from_version]

        if to_version is not None:
            events = [e for e in events if e.get("version", 0) <= to_version]

        return events

    async def get_snapshot(self, aggregate_id: str, version: int) -> dict[str, object] | None:
        """
        Retrieve a snapshot of an aggregate at a specific version.

        Args:
            aggregate_id: The unique identifier of the aggregate.
            version: The version of the snapshot.

        Returns:
            The snapshot data, or None if not found.
        """
        return self._snapshots.get(aggregate_id, {}).get(version)

    async def save_snapshot(
        self, aggregate_id: str, version: int, snapshot: dict[str, object]
    ) -> None:
        """
        Save a snapshot of an aggregate.

        Args:
            aggregate_id: The unique identifier of the aggregate.
            version: The version of the snapshot.
            snapshot: The snapshot data.
        """
        self._snapshots[aggregate_id][version] = snapshot
