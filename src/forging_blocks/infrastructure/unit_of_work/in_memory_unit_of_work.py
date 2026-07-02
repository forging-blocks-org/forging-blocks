"""In-memory Unit of Work implementation.

Provides an in-memory transactional boundary that coordinates changes across
repositories and publishes domain events on successful commit.
"""

from types import TracebackType
from typing import Self

from forging_blocks.application.errors.unit_of_work_error import UnitOfWorkError
from forging_blocks.application.ports.outbound.event_publisher_port import EventPublisherPort
from forging_blocks.application.ports.outbound.unit_of_work_port import UnitOfWorkPort
from forging_blocks.domain import AggregateRoot
from forging_blocks.foundation.errors.core import ErrorMessage


class InMemoryUnitOfWork[IdType, EventPayloadType](UnitOfWorkPort):
    """In-memory implementation of UnitOfWorkPort for coordinating transactions.

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

    def __init__(self, event_publisher: EventPublisherPort[EventPayloadType] | None = None) -> None:
        """Initialize the in-memory unit of work.

        Args:
            event_publisher: An optional EventPublisherPort for publishing
                domain events collected from aggregates on commit.
        """
        self._event_publisher = event_publisher
        self._modified_aggregates: dict[IdType, AggregateRoot[IdType, EventPayloadType]] = {}
        self._committed = False
        self._rolled_back = False

    async def __aenter__(self) -> Self:
        """Enter the Unit of Work context."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the Unit of Work context.

        Commits if no exception occurred; otherwise rolls back.
        """
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    @property
    def committed(self) -> bool:
        """Return True if the transaction has been successfully committed."""
        return self._committed

    @property
    def rolled_back(self) -> bool:
        """Return True if the transaction has been rolled back."""
        return self._rolled_back

    def register_modified(self, aggregate: AggregateRoot[IdType, EventPayloadType]) -> None:
        """Register an aggregate as modified within the current transaction.

        Args:
            aggregate: The aggregate root that was modified.
        """
        if aggregate.id is None:
            raise ValueError("Cannot register aggregate with None id")
        self._modified_aggregates[aggregate.id] = aggregate

    async def commit(self) -> None:
        """Commit all changes and publish collected domain events.

        Raises:
            UnitOfWorkError: If commit fails.
        """
        try:
            await self._publish_events()
            self._clear_events()
            self._mark_committed()
        except Exception as exc:
            raise UnitOfWorkError(ErrorMessage(f"Failed to commit transaction: {exc}")) from exc

    async def rollback(self) -> None:
        """Roll back the transaction and discard tracked aggregates."""
        self._discard_all_events()
        self._mark_rolled_back()

    async def _publish_events(self) -> None:
        """Publish all uncommitted events from modified aggregates."""
        if self._event_publisher is None:
            return

        for aggregate in self._modified_aggregates.values():
            for event in aggregate.uncommitted_changes:
                await self._event_publisher.publish(event)

    def _clear_events(self) -> None:
        """Clear events from all modified aggregates."""
        for aggregate in self._modified_aggregates.values():
            aggregate.collect_events()

    def _discard_all_events(self) -> None:
        """Discard uncommitted events from all modified aggregates."""
        for aggregate in self._modified_aggregates.values():
            aggregate.discard_events()

    def _mark_committed(self) -> None:
        """Mark transaction as committed and reset state."""
        self._committed = True
        self._rolled_back = False
        self._modified_aggregates.clear()

    def _mark_rolled_back(self) -> None:
        """Mark transaction as rolled back and reset state."""
        self._rolled_back = True
        self._committed = False
        self._modified_aggregates.clear()
