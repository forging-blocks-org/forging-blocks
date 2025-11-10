"""Module defining the base abstraction for Aggregate Roots and their version control."""

from __future__ import annotations

from abc import ABC
from typing import Generic, Hashable, TypeVar

from building_blocks.domain.entity import Entity
from building_blocks.domain.errors.entity_id_none_error import EntityIdNoneError
from building_blocks.domain.messages.event import Event
from building_blocks.domain.value_object import ValueObject

TId = TypeVar("TId", bound=Hashable)


class AggregateVersion(ValueObject[int]):
    """Immutable value object representing the version of an aggregate root.

    Used for optimistic concurrency control to detect conflicting updates.
    """

    def __init__(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Expected int, got {type(value).__name__}")
        if value < 0:
            raise ValueError("Version cannot be negative")
        self._value = value

    @property
    def value(self) -> int:
        """Return the integer version value."""
        return self._value

    def increment(self) -> AggregateVersion:
        """Return a new AggregateVersion incremented by one."""
        return AggregateVersion(self._value + 1)

    def _equality_components(self) -> tuple[Hashable, ...]:
        """Components used for equality comparison."""
        return (self._value,)


class AggregateRoot(Entity[TId], Generic[TId], ABC):
    """Base class for Aggregate Roots in a Domain-Driven Design context.

    An Aggregate Root represents the entry point for manipulating
    a consistency boundary composed of entities and value objects.
    It encapsulates domain logic, maintains a version for concurrency control,
    and records uncommitted domain events.
    """

    _uncommitted_events: list[Event]

    def __init__(self, aggregate_id: TId, version: AggregateVersion | None = None) -> None:
        if not aggregate_id:
            raise EntityIdNoneError(self.__class__.__name__)
        self._version = version or AggregateVersion(0)
        self._uncommitted_events = []
        super().__init__(aggregate_id)

    @property
    def version(self) -> AggregateVersion:
        """Return the current version of the aggregate."""
        return self._version

    def collect_events(self) -> list[Event]:
        """Collect uncommitted events, clear array, increment the version and return events."""
        events = self._uncommitted_events.copy()
        self._uncommitted_events.clear()
        self._increment_version()

        return events

    def record_event(self, domain_event: Event) -> None:
        """Record a new domain event for later publication."""
        self._uncommitted_events.append(domain_event)

    def uncommitted_changes(self) -> list[Event]:
        """Return a copy of uncommitted domain events recorded by this aggregate."""
        return self._uncommitted_events.copy()

    def _increment_version(self) -> None:
        """Increment the aggregate's version value."""
        self._version = self._version.increment()
