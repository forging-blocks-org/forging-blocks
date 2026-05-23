"""ForgingBlocks infrastructure package initialization.

Provides generic, reusable infrastructure building blocks implementing
the outbound ports defined in the application layer.
"""

from .errors.repository_errors import RepositoryError, RepositoryNotFoundError
from .message_bus.in_memory_message_bus import InMemoryMessageBus
from .repositories.in_memory_read_repository import InMemoryReadRepository
from .repositories.in_memory_write_repository import InMemoryWriteRepository
from .unit_of_work.in_memory_unit_of_work import InMemoryUnitOfWork

__all__ = [
    "InMemoryMessageBus",
    "InMemoryReadRepository",
    "InMemoryUnitOfWork",
    "InMemoryWriteRepository",
    "RepositoryError",
    "RepositoryNotFoundError",
]
