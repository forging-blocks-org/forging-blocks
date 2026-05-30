"""Base AggregateRoot class for Domain-Driven Design."""

from __future__ import annotations

from abc import abstractmethod
from typing import Any, Generic, Hashable, TypeVar

from forging_blocks.domain.entity import Entity
from forging_blocks.domain.errors.entity_id_none_error import EntityIdNoneError
from forging_blocks.foundation import FinalABCMeta, runtime_final
from forging_blocks.foundation.messages.event import Event

from .aggregate_version import AggregateVersion

TId = TypeVar("TId", bound=Hashable)


class AggregateRoot(Entity[TId], Generic[TId], metaclass=FinalABCMeta):
    """Base class for Aggregate Roots in a Domain-Driven Design context.

    An Aggregate Root represents the entry point for manipulating
    a consistency boundary composed of entities and value objects.
    It encapsulates domain logic, maintains a version for concurrency control,
    and records uncommitted domain events.

    References:
        Vernon, V. (2013). Implementing Domain-Driven Design.
        Addison-Wesley. Ch.8, Ch.10, Appendix A.
    """

    def __init__(self, aggregate_id: TId, version: AggregateVersion | None = None) -> None:
        self._validate_identity(aggregate_id)
        self._version = version or AggregateVersion(0)
        self._uncommitted_events: list[Event[Any]] = []
        super().__init__(aggregate_id)

    @runtime_final
    def _validate_identity(self, aggregate_id: Hashable) -> None:
        """Ensure the aggregate root identity is valid.

        Aggregate roots must always have a defined, non-falsy identity.
        Draft state is intentionally prohibited — identity must exist before
        construction, not after persistence.

        Raises:
            EntityIdNoneError: If the identity is None, an empty string,
                or the boolean False.
        """
        is_none = aggregate_id is None
        is_empty_string = isinstance(aggregate_id, str) and aggregate_id == ""
        is_false = isinstance(aggregate_id, bool) and aggregate_id is False

        if is_none or is_empty_string or is_false:
            raise EntityIdNoneError(self.__class__.__name__)

    @property
    def version(self) -> AggregateVersion:
        """Return the current version of the aggregate."""
        return self._version

    @property
    def uncommitted_changes(self) -> list[Event[Any]]:
        """Return a copy of uncommitted domain events recorded by this aggregate."""
        return self._uncommitted_events.copy()

    @runtime_final
    def collect_events(self) -> list[Event[Any]]:
        """Drain uncommitted events for the dispatcher.

        Called by the Unit of Work or repository after persistence.
        No version side-effect — version is already correct from apply().
        """
        events = self._uncommitted_events.copy()
        self._uncommitted_events.clear()
        return events

    @runtime_final
    def discard_events(self) -> None:
        """Discard uncommitted events on rollback.

        Clears the queue without touching version — the committed
        version must remain consistent with persisted state.
        """
        self._uncommitted_events.clear()

    @runtime_final
    def record_event(self, domain_event: Event[Any]) -> None:
        """Record an event that occurred outside aggregate state mutation.

        Use for integration events or application-layer concerns
        that do not trigger a state transition.
        """
        self._uncommitted_events.append(domain_event)

    @runtime_final
    def apply(self, event: Event[Any]) -> None:
        """Single entry point for state transitions.

        Delegates mutation to _handle(), increments version,
        and appends to the uncommitted queue.
        Version increment lives here so reconstitution from
        an event store replays through the same path.
        """
        self._handle(event)
        self._version = self._version.increment()
        self._uncommitted_events.append(event)

    @abstractmethod
    def _handle(self, event: Event[Any]) -> None:
        """Mutate aggregate state in response to an event.

        Implemented by concrete subclasses. Called exclusively
        by apply() — never directly.
        """
        ...
