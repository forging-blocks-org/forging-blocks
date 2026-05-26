"""In-memory Unit of Work implementation.

Provides an in-memory transactional boundary that coordinates changes across
repositories and publishes domain events on successful commit.
"""

from __future__ import annotations

from typing import Any

from forging_blocks.application.errors.unit_of_work_error import UnitOfWorkError
from forging_blocks.application.ports.outbound.event_publisher import EventPublisher
from forging_blocks.application.ports.outbound.unit_of_work import UnitOfWork
from forging_blocks.domain.aggregate_root import AggregateRoot
from forging_blocks.foundation.errors.core import ErrorMessage


class InMemoryUnitOfWork(UnitOfWork):
    """In-memory implementation of UnitOfWork for coordinating transactions.

    Tracks aggregates modified during the transaction and publishes their
    collected domain events upon successful commit. The actual persistence
    is handled by the repositories, while this class coordinates event
    publication and transactional consistency.

    Usage::

        async with InMemoryUnitOfWork(event_publisher) as uow:
            uow.register_modified(aggregate)
            await write_repo.save(aggregate)
    """

    __slots__ = ("_committed", "_event_publisher", "_modified_aggregates", "_rolled_back")

    def __init__(self, event_publisher: EventPublisher | None = None) -> None:
        """Initialize the in-memory unit of work.

        Args:
            event_publisher: An optional EventPublisher for publishing
                domain events collected from aggregates on commit.
        """
        self._event_publisher = event_publisher
        self._modified_aggregates: dict[Any, AggregateRoot[Any]] = {}
        self._committed = False
        self._rolled_back = False

    @property
    def committed(self) -> bool:
        """Return True if the transaction has been successfully committed."""
        return self._committed

    @property
    def rolled_back(self) -> bool:
        """Return True if the transaction has been rolled back."""
        return self._rolled_back

    @property
    def session(self) -> Any | None:
        """Return the transaction state dict, or None if not active."""
        return None

    def register_modified(self, aggregate: AggregateRoot[Any]) -> None:
        """Register an aggregate as modified within the current transaction.

        Args:
            aggregate: The aggregate root that was modified.
        """
        self._modified_aggregates[aggregate.id] = aggregate

    async def commit(self) -> None:
        """Commit all changes and publish collected domain events.

        Iterates through registered modified aggregates, snapshots their
        uncommitted domain events, publishes them through the configured
        EventPublisher, and only then clears the events from the aggregates.

        Raises:
            UnitOfWorkError: If commit fails.
        """
        try:
            aggregates_with_events: list[tuple[AggregateRoot[Any], list[Any]]] = [
                (aggregate, list(aggregate.uncommitted_changes))
                for aggregate in self._modified_aggregates.values()
            ]

            if self._event_publisher is not None:
                for _, events in aggregates_with_events:
                    for event in events:
                        await self._event_publisher.publish(event)

            for aggregate, _ in aggregates_with_events:
                aggregate.collect_events()
        except Exception as exc:
            raise UnitOfWorkError(ErrorMessage(f"Failed to commit transaction: {exc}")) from exc

        self._committed = True
        self._rolled_back = False
        self._modified_aggregates.clear()

    async def rollback(self) -> None:
        """Roll back the transaction and discard tracked aggregates.

        Discards uncommitted events from all tracked aggregates and
        clears the modified aggregate registry.
        """
        for aggregate in self._modified_aggregates.values():
            aggregate.discard_events()
        self._modified_aggregates.clear()
        self._rolled_back = True
        self._committed = False
