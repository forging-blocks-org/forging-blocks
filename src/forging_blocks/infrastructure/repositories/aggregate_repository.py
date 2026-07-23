"""Aggregate RepositoryPort implementation.

Provides a repository specifically designed for AggregateRoot persistence
with event sourcing support.
"""

from typing import Any, cast
from uuid import UUID

from forging_blocks.domain.aggregate_root.aggregate_root import AggregateRoot
from forging_blocks.foundation.messages.event import Event
from forging_blocks.infrastructure.event_stores.event_store_base import EventStoreBase
from forging_blocks.infrastructure.repositories.in_memory_repository import InMemoryRepository


class AggregateRepository[
    EventPayloadType,
    TAggregateRoot: AggregateRoot[UUID, Any],
    TId: UUID,
](InMemoryRepository[TAggregateRoot, TId]):
    """RepositoryPort for AggregateRoot persistence with event sourcing.
    Extends InMemoryRepository with event store integration for
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
        aggregate_type: type[TAggregateRoot],
        storage: dict[TId, TAggregateRoot] | None = None,
    ) -> None:
        """Initialize the aggregate repository.

        Args:
            event_store: The event store for persisting domain events.
            aggregate_type: The aggregate root class. Used via
                its ``reconstitute`` classmethod when an aggregate
                must be rebuilt from stored events.
            storage: Optional in-memory storage for aggregate snapshots.

        """
        super().__init__(storage)
        self._event_store = event_store
        self._aggregate_type = aggregate_type

    async def save(self, aggregate: TAggregateRoot) -> None:
        """Save an aggregate and its uncommitted events.

        Writes events to the event store first, then persists the aggregate
        snapshot. If the event store write fails, the error is raised so the
        Unit of Work can rollback and the aggregate retains its uncommitted
        events.

        The ``cast`` on ``uncommitted_changes`` bridges the gap between
        ``TAggregateRoot``'s bound (``AggregateRoot[UUID, Any]``) and the
        repository's ``EventPayloadType`` generic. The types are guaranteed to
        match at runtime by construction; the type system cannot express this
        cross-TypeVar-bound relationship (see PEP 695, pyright
        ``reportGeneralTypeIssues``).

        Args:
            aggregate: The aggregate to save.

        Raises:
            EventStoreError: If the event store write fails (e.g., concurrency
                conflict, I/O error).

        """
        events = cast(list[Event[EventPayloadType]], aggregate.uncommitted_changes)
        aggregate_id: TId | None = aggregate.id
        if events and aggregate_id is not None:
            version = aggregate.version.value - len(events)
            result = await self._event_store.append_events(
                aggregate_id, events, expected_version=version
            )
            if not result.is_ok:
                raise result.error
        await super().save(aggregate)

    async def get_by_id(self, id: TId) -> TAggregateRoot | None:
        """Retrieve an aggregate by ID and replay its events.

        Checks the in-memory cache first; if not cached, replays the
        aggregate from the event store and caches the result so subsequent
        reads avoid a full replay.

        Args:
            id: Unique identifier of the aggregate.

        Returns:
            The retrieved aggregate or None if not found.

        Raises:
            EventStoreError: If the event store read fails. Callers can
                distinguish infrastructure failures from "not found" (None).

        """
        aggregate = await super().get_by_id(id)
        if aggregate is not None:
            return aggregate

        result = await self._event_store.get_events(cast(UUID, id))

        if not result.is_ok:
            raise result.error

        events = result.value

        if not events:
            return None

        aggregate = self._aggregate_type.reconstitute(id, events)
        await super().save(aggregate)

        return aggregate
