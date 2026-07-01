"""ForgingBlocks infrastructure package initialization.

Provides generic, reusable infrastructure building blocks implementing
the outbound ports defined in the application layer.
"""

from .caching.in_memory_cache import InMemoryCache
from .errors.repository_errors import RepositoryError, RepositoryNotFoundError
from .event_bus import EventBusPort, NoHandlerError
from .event_buses.in_memory_event_bus import InMemoryEventBus
from .event_store import ConcurrencyError, EventStorePort
from .event_stores.in_memory_event_store import InMemoryEventStore
from .file_system.os_file_system import OSFileSystem
from .http_client.urllib_client import URLLibClient
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
    "EventBusPort",
    "EventStorePort",
    "InMemoryCache",
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
    "URLLibClient",
]
