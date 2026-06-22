"""ForgingBlocks infrastructure package initialization.

Provides generic, reusable infrastructure building blocks implementing
the outbound ports defined in the application layer.
"""

from .errors.repository_errors import RepositoryError, RepositoryNotFoundError
from .event_bus import EventBus, NoHandlerError
from .event_buses.in_memory_event_bus import InMemoryEventBus
from .event_store import ConcurrencyError, EventStore
from .event_stores.in_memory_event_store import InMemoryEventStore
from .file_system.os_file_system import OSFileSystem
from .logging.stdlib_logger import StdlibLogger
from .message_bus.in_memory_message_bus import InMemoryMessageBus
from .repositories import (
    AggregateRepository,
    BaseReadRepository,
    BaseRepository,
    BaseWriteRepository,
    InMemoryReadRepository,
    InMemoryWriteRepository,
)
from .unit_of_work.in_memory_unit_of_work import InMemoryUnitOfWork

__all__ = [
    "AggregateRepository",
    "BaseReadRepository",
    "BaseRepository",
    "BaseWriteRepository",
    "ConcurrencyError",
    "EventBus",
    "EventStore",
    "InMemoryEventBus",
    "InMemoryEventStore",
    "InMemoryMessageBus",
    "InMemoryReadRepository",
    "InMemoryUnitOfWork",
    "InMemoryWriteRepository",
    "NoHandlerError",
    "OSFileSystem",
    "RepositoryError",
    "RepositoryNotFoundError",
    "StdlibLogger",
]
