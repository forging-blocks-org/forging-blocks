"""Base AggregateRoot class for Domain-Driven Design."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, Hashable, TypeVar

from forging_blocks.domain.entity import Entity
from forging_blocks.domain.errors.entity_id_none_error import EntityIdNoneError
from forging_blocks.foundation.messages.event import Event

from .aggregate_version import AggregateVersion

TId = TypeVar("TId", bound=Hashable)


class AggregateRoot(Entity[TId], Generic[TId], ABC):
    """Base class for Aggregate Roots in a Domain-Driven Design context.

    An Aggregate Root represents the entry point for manipulating
    a consistency boundary composed of entities and value objects.
    It encapsulates domain logic, maintains a version for concurrency control,
    and records uncommitted domain events.
    """

    _uncommitted_events: list[Event[Any]]

    def __init__(self, aggregate_id: TId, version: AggregateVersion | None = None) -> None:
        if aggregate_id is None or aggregate_id == "":
            raise EntityIdNoneError(self.__class__.__name__)
        self._version = version or AggregateVersion(0)
        self._uncommitted_events = []
        super().__init__(aggregate_id)

    @property
    def version(self) -> AggregateVersion:
        """Return the current version of the aggregate."""
        return self._version

    @property
    def uncommitted_changes(self) -> list[Event[Any]]:
        """Return a copy of uncommitted domain events recorded by this aggregate."""
        return self._uncommitted_events.copy()

    def collect_events(self) -> list[Event[Any]]:
        """Collect uncommitted events, clear array, increment the version and return events."""
        events = self._uncommitted_events.copy()
        self._uncommitted_events.clear()

        if events:
            self._version = self._version.increment()

        return events

    def discard_events(self) -> None:
        """Discard uncommitted events without incrementing the version.

        Used during rollback to clear events from a failed transaction
        without affecting the aggregate's committed version.
        """
        self._uncommitted_events.clear()

    def record_event(self, domain_event: Event[Any]) -> None:
        """Record a new domain event for later publication."""
        self._uncommitted_events.append(domain_event)

    @abstractmethod
    def apply(self, event: Event[Any]) -> None:
        """Apply a domain event to this aggregate.

        Subclasses must implement this method to define how each event
        type mutates the aggregate's state. Implementations should call
        ``self.record_event(event)`` to store the event for later
        collection by the unit of work.

        Args:
            event: The domain event to apply.
        """
        ...
