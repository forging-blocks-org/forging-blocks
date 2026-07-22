"""In-memory full CRUD repository backed by a dictionary.

Combines InMemoryReadRepository and InMemoryWriteRepository into a single
class suitable for non-CQRS applications or simplified contexts.
"""

from collections.abc import MutableMapping
from typing import Any

from forging_blocks.foundation.identified import Identified
from forging_blocks.infrastructure.repositories.in_memory_read_repository import (
    InMemoryReadRepository,
)
from forging_blocks.infrastructure.repositories.in_memory_write_repository import (
    InMemoryWriteRepository,
)


class InMemoryRepository[TEntity: Identified[Any], TId](
    InMemoryReadRepository[TEntity, TId],
    InMemoryWriteRepository[TEntity, TId],
):
    """Full CRUD in-memory repository backed by a dictionary.

    Combines read and write operations into a single class using shared
    dictionary-based storage. Suitable for non-CQRS applications or
    simplified single-process contexts.
    """

    def __init__(
        self,
        storage: MutableMapping[TId, TEntity] | None = None,
    ) -> None:
        """Initialize the repository with optional external storage.

        Args:
            storage: An optional mutable mapping to use as backing storage.
                If None, a new empty dictionary is used.

        """
        super().__init__(storage)
