"""Service context for application services.

Provides a context object that carries dependencies and state
for application service execution.
"""

from typing import Any, Generic, TypeVar

from forging_blocks.application.ports.outbound.event_publisher import EventPublisher
from forging_blocks.application.ports.outbound.unit_of_work import UnitOfWork

TEventPayload = TypeVar("TEventPayload")


class ServiceContext(Generic[TEventPayload]):
    """Context object for application service execution.

    Carries the dependencies needed by application services,
    including the Unit of Work and Event Publisher.
    """

    __slots__ = ("_unit_of_work", "_event_publisher", "_data")

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        event_publisher: EventPublisher[TEventPayload] | None = None,
    ) -> None:
        """Initialize the service context.

        Args:
            unit_of_work: The Unit of Work for transaction management.
            event_publisher: Optional event publisher for domain events.
        """
        self._unit_of_work = unit_of_work
        self._event_publisher = event_publisher
        self._data: dict[str, Any] = {}

    @property
    def unit_of_work(self) -> UnitOfWork:
        """Get the Unit of Work."""
        return self._unit_of_work

    @property
    def event_publisher(self) -> EventPublisher[TEventPayload] | None:
        """Get the event publisher."""
        return self._event_publisher

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the context data."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a value in the context data."""
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the context data."""
        return key in self._data
