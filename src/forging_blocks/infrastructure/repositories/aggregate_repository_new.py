"""Aggregate RepositoryPort implementation.

Provides a repository specifically designed for AggregateRoot persistence
with event sourcing support.
"""

from uuid import UUID

from forging_blocks.domain.aggregate_root.aggregate_root import AggregateRoot
from forging_blocks.infrastructure.event_stores.event_store_base import EventStoreBase
from forging_blocks.infrastructure.repositories.base_repository import BaseRepository


class AggregateRepository[TAggregateRoot: AggregateRoot[object, UUID], TId: UUID](
    BaseRepository[TAggregateRoot, TId]
):
    """RepositoryPort for AggregateRoot persistence with event sourcing.
    Extends BaseRepository with event store integration for event-sourced aggregates.
    """

    _event_store: EventStoreBase

    def __init__(
        self,
        event_store: EventStoreBase,
        storage: dict[TId, TAggregateRoot] | None = None,
    ) -> None:
        super().__init__(storage)
        self._event_store = event_store

    async def save(self, aggregate: TAggregateRoot) -> None:
        await super().save(aggregate)
        events = aggregate.collect_events()
        aggregate_id: UUID | None = aggregate.id  # type: ignore[assignment]
        if events and aggregate_id is not None:
            version = aggregate.version.value - len(events)
            await self._event_store.append_events(aggregate_id, events, expected_version=version)

    async def get_by_id(self, id: TId) -> TAggregateRoot | None:  # noqa: A002
        aggregate = await super().get_by_id(id)
        if aggregate is not None:
            return aggregate
        result = await self._event_store.get_events(id)
        if not result.is_ok or not result.value:
            return None
        return None  # Replay not implemented — override in subclasses
