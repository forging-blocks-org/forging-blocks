# pyright: reportAttributeAccessIssue=false, reportUnknownMemberType=false, reportArgumentType=false
"""Aggregate RepositoryPort implementation.

Provides a repository specifically designed for AggregateRoot persistence
with event sourcing support.
"""

from typing import Any

from forging_blocks.domain.aggregate_root.aggregate_root import AggregateRoot
from forging_blocks.infrastructure.event_stores.event_store_base import EventStoreBase
from forging_blocks.infrastructure.repositories.base_repository import BaseRepository


class AggregateRepository[TAggregateRoot: AggregateRoot[Any, Any], TId: Any](
    BaseRepository[TAggregateRoot, TId]
):
    """RepositoryPort for AggregateRoot persistence with event sourcing.

    Extends BaseRepository with event store integration for
    event-sourced aggregates.
    """

    def __init__(
        self,
        event_store: EventStoreBase[object],
        storage: dict[TId, TAggregateRoot] | None = None,
    ) -> None:
        """Initialize the aggregate repository.

        Args:
            event_store: The event store for persisting domain events.
            storage: Optional in-memory storage for aggregate snapshots.
        """
        super().__init__(storage)
        self._event_store = event_store

    async def save(self, aggregate: TAggregateRoot) -> None:
        """Save an aggregate and its uncommitted events.

        Args:
            aggregate: The aggregate to save.
        """
        # Save the aggregate snapshot
        await super().save(aggregate)

        # Persist uncommitted events to the event store
        events = aggregate.collect_events()
        if events:
            await self._event_store.save_events(
                aggregate_id=str(aggregate.id),
                events=[event.to_dict() for event in events],
                expected_version=aggregate.version.value - len(events),
            )

    async def get_by_id(self, id: TId) -> TAggregateRoot | None:  # noqa: A002
        """Retrieve an aggregate by ID and replay its events.

        Args:
            id: Unique identifier of the aggregate.

        Returns:
            The retrieved aggregate or None if not found.
        """
        # First check in-memory storage
        aggregate = await super().get_by_id(id)
        if aggregate is not None:
            return aggregate

        # If not in memory, try to load from event store
        events = await self._event_store.get_events(str(id))
        if not events:
            return None

        # Reconstruct aggregate from events
        # This requires the aggregate type to have a factory method
        # For now, return None - concrete implementations should override
        return None
