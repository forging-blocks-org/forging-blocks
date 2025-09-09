"""
AggregateRoot and DraftAggregateRoot base class and related components for Domain-Driven
Design.
Inspired by Vaughn Vernon's "Implementing Domain-Driven Design".
This module provides the foundational classes for creating aggregate roots,
managing their versions, and handling domain events in a DDD context.
"""

from __future__ import annotations

from abc import ABC
from typing import Generic, Hashable, TypeVar

from building_blocks.domain.entity import Entity
from building_blocks.domain.messages.event import Event
from building_blocks.domain.value_object import ValueObject

TId = TypeVar("TId", bound=Hashable)


class AggregateVersion(ValueObject):
    """
    Value object representing the version of an aggregate root.

    This is used for optimistic concurrency control to ensure that updates
    to the aggregate are consistent and do not conflict with other changes.
    """

    def __init__(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Expected int, got {type(value).__name__}")
        if value < 0:
            raise ValueError("Version cannot be negative")
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def increment(self) -> AggregateVersion:
        """
        Increment version value by 1 and return a new AggregateVersion instance.
        This is used to track changes to the aggregate state and ensure
        optimistic concurrency control.

        Returns:
            AggregateVersion: A new instance with the incremented version value.
        """
        return AggregateVersion(self._value + 1)

    def _equality_components(self) -> tuple[Hashable, ...]:
        """
        Return the components used for equality comparison.

        This is used by the ValueObject base class to determine equality.
        """
        return (self._value,)


class AggregateRoot(Entity[TId], Generic[TId], ABC):
    """
    Base class for aggregate roots in Domain-Driven Design.

    An AggregateRoot is a special type of Entity that serves as the entry point
    for managing a cluster of related entities and value objects. It encapsulates
    the business logic and invariants of the aggregate, ensuring that all changes
    to the aggregate are made through its methods. This class is designed to
    follow the principles of Domain-Driven Design (DDD) and is inspired by Vaughn
    Vernon's approach in "Implementing Domain-Driven Design".

    This implementation provides methods for managing the aggregate version,
    recording uncommitted domain events, and marking changes as committed.
    It is intended to be subclassed to create specific aggregate roots that
    represent business concepts in the domain.

    This implementation follows Vaughn Vernon's approach from
    "Implementing Domain-Driven Design" and is designed to be used in and
    with a Domain-Driven Design context.
    It provides a foundation for building aggregates that encapsulate business
    logic and maintain consistency across related entities and value objects.
    """

    _uncommitted_events: list[Event]

    def __init__(
        self, aggregate_id: TId, version: AggregateVersion | None = None
    ) -> None:
        """
        Initialize the aggregate root.

        Args:
            aggregate_id: Unique identifier for this aggregate
            version: Optional initial version for optimistic concurrency control.
                     If not provided, defaults to AggregateVersion(0).
        """
        super().__init__(aggregate_id)
        self._id = aggregate_id
        self._version = version or AggregateVersion(0)
        self._uncommitted_events: list[Event] = []

    @property
    def version(self) -> AggregateVersion:
        """
        Get the current version of this aggregate.
        """
        return self._version

    def uncommitted_changes(self) -> list[Event]:
        """
        Get the uncommitted domain events raised by this aggregate.

        Returns a copy to prevent external modification.
        Following Vaughn Vernon's naming convention.

        Returns:
            list[Event]: Copy of uncommitted domain events
        """
        return self._uncommitted_events.copy()

    def record_event(self, domain_event: Event) -> None:
        """
        Record a domain event to be published.

        This is the primary method for recording domain events when significant
        business events occur. Following Vaughn Vernon's naming convention.

        Args:
            domain_event: The domain event to record
        """
        self._uncommitted_events.append(domain_event)

    def mark_changes_as_committed(self) -> None:
        """
        Mark all uncommitted changes as committed and clear them.

        This method should be called after events have been successfully
        published and the aggregate has been persisted.
        Following Vaughn Vernon's naming convention.
        """
        self._uncommitted_events.clear()
        self._increment_version()

    def _increment_version(self) -> None:
        """
        Increment the aggregate version.

        Protected method to be called when the aggregate state changes.
        Useful for optimistic concurrency control.
        """
        self._version = self._version.increment()
