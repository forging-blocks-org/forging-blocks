"""Aggregate RepositoryPort implementation.

Provides a repository specifically designed for AggregateRoot persistence
with event sourcing support.
"""

from typing import Any, cast
from uuid import UUID

from forging_blocks.domain.aggregate_root.aggregate_root import AggregateRoot
from forging_blocks.domain.messages.event import Event
from forging_blocks.infrastructure.event_stores.event_store_base import EventStoreBase
from forging_blocks.infrastructure.repositories.in_memory_repository import InMemoryRepository


class AggregateRepository[
    EventPayloadType,
    TAggregateRoot: AggregateRoot[UUID, Any],
    TId: UUID,
](InMemoryRepository[TAggregateRoot, TId]):
    """RepositoryPort for persisting event-sourced aggregates.
    Coordinates event store writes with in-memory snapshot caching
    for AggregateRoot subtypes.

    Type Parameters:
        EventPayloadType: The event payload type tracked by the event store.
            Flows through the public generic interface.
        TAggregateRoot: An AggregateRoot subtype with UUID identity whose event
            payload type must match ``EventPayloadType`` at each call site. The
            bound uses ``Any`` as the second type argument — not because the
            event type is untyped, but because PEP 695 (and the underlying type
            system) forbids one TypeVar from appearing inside another TypeVar's
            bound. The ``cast`` in `save` is the explicit, localized bridge
            across this gap. The invariant is enforced by construction.
        TId: The aggregate identity type, bounded by ``UUID``.

    Example:
        ```python
        class Event[T]:
            pass


        class AggregateRoot[TId, TPayload]:
            def __init__(self, aggregate_id: TId) -> None:
                self.id = aggregate_id


        class InMemoryEventStore[T]:
            def __init__(self) -> None: ...

            async def append_events(
                self, aggregate_id: object, events: list[object], expected_version: int
            ) -> None: ...
            async def get_events(self, aggregate_id: object) -> list[object]: ...
            async def get_current_version(self, aggregate_id: object) -> int: ...


        class MyAggregate(AggregateRoot[UUID, str]):
            def __init__(self, aggregate_id: UUID) -> None:
                super().__init__(aggregate_id)

            def _handle(self, event: Event[str]) -> None:
                pass


        event_store = InMemoryEventStore[str]()
        aggregate_id = UUID("00000000-0000-0000-0000-000000000001")
        repo = AggregateRepository[str, MyAggregate, UUID](
            event_store=event_store,
            aggregate_type=MyAggregate,
        )


        async def main() -> None:
            aggregate = MyAggregate(aggregate_id)
            await repo.save(aggregate)
            retrieved = await repo.get_by_id(aggregate_id)
        ```
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
        """Save an aggregate and its state-changing events.

        Writes state-changing events to the event store first, then persists
        the aggregate snapshot. Publication-only events recorded through
        ``AggregateRoot.record_event`` remain available to the Unit of Work
        but are not stored in the aggregate event stream.

        The repository does not drain either event queue. The Unit of Work is
        the authoritative event-drain boundary after publication. Saving the
        same aggregate again before that drain attempts to append the same
        state changes and raises a concurrency error.

        The ``cast`` on ``state_changes`` bridges the gap between
        ``TAggregateRoot``'s bound (``AggregateRoot[UUID, Any]``) and the
        repository's ``EventPayloadType`` generic. The types are guaranteed to
        match at runtime by construction; the type system cannot express this
        cross-TypeVar-bound relationship (see PEP 695 and Pyright's
        ``reportGeneralTypeIssues``).

        Args:
            aggregate: The aggregate to save.

        Raises:
            EventStoreError: If the event store write fails (e.g., concurrency
                conflict, I/O error).

        """
        events = cast(list[Event[EventPayloadType]], aggregate.state_changes)
        aggregate_id: UUID | None = aggregate.id
        if events and aggregate_id is not None:
            version = aggregate.version.value - len(events)
            result = await self._event_store.append_events(
                aggregate_id, events, expected_version=version
            )
            if not result.is_ok:
                raise result.error
        await super().save(aggregate)

    async def get_by_id(self, entity_id: TId) -> TAggregateRoot | None:
        """Retrieve an aggregate by ID and replay its events.

        Checks the in-memory cache first; if not cached, replays the
        aggregate from the event store and caches the result so subsequent
        reads avoid a full replay.

        Args:
            entity_id: Unique identifier of the aggregate.

        Returns:
            The retrieved aggregate or None if not found.

        Raises:
            EventStoreError: If the event store read fails. Callers can
                distinguish infrastructure failures from "not found" (None).

        """
        aggregate = await super().get_by_id(entity_id)
        if aggregate is not None:
            return aggregate

        result = await self._event_store.get_events(cast(UUID, entity_id))

        if not result.is_ok:
            raise result.error

        events = result.value

        if not events:
            return None

        aggregate = self._aggregate_type.reconstitute(entity_id, events)
        await super().save(aggregate)

        return aggregate
