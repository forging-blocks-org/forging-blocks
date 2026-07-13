"""Aggregate RepositoryPort implementation.

Provides a repository specifically designed for AggregateRoot persistence
with event sourcing support.
"""

from typing import Any, cast
from uuid import UUID

from forging_blocks.domain.aggregate_root.aggregate_root import AggregateRoot
from forging_blocks.foundation.messages.event import Event
from forging_blocks.infrastructure.event_stores.event_store_base import EventStoreBase
from forging_blocks.infrastructure.repositories.base_repository import BaseRepository


class AggregateRepository[
    EventPayloadType,
    TAggregateRoot: AggregateRoot[UUID, Any],
    TId: UUID,
](BaseRepository[TAggregateRoot, TId]):
    """RepositoryPort for AggregateRoot persistence with event sourcing.

    Extends BaseRepository with event store integration for
    event-sourced aggregates.

    Type Parameters:
        EventPayloadType: The event payload type tracked by the event store.
            Flows through the public generic interface.
        TAggregateRoot: An AggregateRoot subtype with UUID identity whose event
            payload type must match ``EventPayloadType`` at each call site. The
            bound uses ``Any`` as the second type argument — not because the
            event type is untyped, but because PEP 695 (and the underlying type
            system) forbids one TypeVar from appearing inside another TypeVar's
            bound. The ``cast`` in :meth:`save` is the explicit, localized bridge
            across this gap. The invariant is enforced by construction.
        TId: The aggregate identity type, bounded by ``UUID``.
    """

    _event_store: EventStoreBase[EventPayloadType]

    def __init__(
        self,
        event_store: EventStoreBase[EventPayloadType],
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

        Persists the aggregate via the base repository and appends
        its collected domain events to the event store with optimistic
        concurrency checks.

        The ``cast`` on ``collect_events()`` bridges the gap between
        ``TAggregateRoot``'s bound (``AggregateRoot[UUID, Any]``) and the
        repository's ``EventPayloadType`` generic. The types are guaranteed to
        match at runtime by construction; the type system cannot express this
        cross-TypeVar-bound relationship (see PEP 695, pyright
        ``reportGeneralTypeIssues``).

        Args:
            aggregate: The aggregate to save.
        """
        await super().save(aggregate)
        events = cast("list[Event[EventPayloadType]]", aggregate.collect_events())
        aggregate_id: UUID | None = aggregate.id  # type: ignore[assignment]
        if events and aggregate_id is not None:
            version = aggregate.version.value - len(events)
            await self._event_store.append_events(aggregate_id, events, expected_version=version)

    async def get_by_id(self, id: TId) -> TAggregateRoot | None:  # noqa: A002
        """Retrieve an aggregate by ID and replay its events.

        Args:
            id: Unique identifier of the aggregate.

        Returns:
            The retrieved aggregate or None if not found.
        """
        aggregate = await super().get_by_id(id)
        if aggregate is not None:
            return aggregate
        result = await self._event_store.get_events(id)  # type: ignore[arg-type]
        if not result.is_ok or not result.value:
            return None
        return None
