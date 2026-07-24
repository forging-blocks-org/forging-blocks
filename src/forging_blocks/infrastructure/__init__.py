"""Infrastructure block — concrete implementations of application outbound ports.

Provides generic, reusable infrastructure building blocks implementing
the outbound ports defined in the application layer. Includes in-memory
adapters for repositories, event buses, event stores, message buses,
caching, logging, file system, and HTTP; plus MessageCodec/DictMessageCodec, abstract
errors.
"""

from .caching.in_memory_cache import InMemoryCache
from .errors.repository_errors import RepositoryError, RepositoryNotFoundError
from .event_buses import (
    EventBusBase,
    InMemoryEventBus,
    InMemoryEventBusBase,
)
from .event_stores import (
    EventStoreBase,
    InMemoryEventStore,
    InMemoryEventStoreBase,
)
from .file_system.os_file_system import OSFileSystem
from .http_client.urllib_client import URLLibClient
from .logging.stdlib_logger import StdlibLogger
from .message_bus.in_memory_message_bus import InMemoryMessageBus
from .message_bus.message_bus_command_sender import MessageBusCommandSender
from .message_bus.message_bus_event_publisher import MessageBusEventPublisher
from .message_bus.message_bus_query_fetcher import MessageBusQueryFetcher
from .repositories import (
    AggregateRepository,
    InMemoryReadRepository,
    InMemoryRepository,
    InMemoryWriteRepository,
)
from .serialization import DictMessageCodec, MessageCodec
from .unit_of_work.in_memory_unit_of_work import InMemoryUnitOfWork

__all__ = [
    "AggregateRepository",
    "EventBusBase",
    "EventStoreBase",
    "InMemoryCache",
    "InMemoryEventBus",
    "InMemoryEventBusBase",
    "InMemoryEventStore",
    "InMemoryEventStoreBase",
    "InMemoryMessageBus",
    "InMemoryReadRepository",
    "InMemoryRepository",
    "InMemoryUnitOfWork",
    "InMemoryWriteRepository",
    "MessageBusCommandSender",
    "MessageBusEventPublisher",
    "MessageBusQueryFetcher",
    "OSFileSystem",
    "RepositoryError",
    "RepositoryNotFoundError",
    "DictMessageCodec",
    "MessageCodec",
    "StdlibLogger",
    "URLLibClient",
]
