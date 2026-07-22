"""In-memory write-only repository implementation.

Provides a concrete implementation of WriteOnlyRepository backed by a
dictionary for command-side operations in CQRS architectures.
"""

from collections.abc import MutableMapping
from typing import Any

from forging_blocks.foundation.identified import Identified
from forging_blocks.infrastructure.repositories.base_repository import BaseWriteRepository


class InMemoryWriteRepository[TWriteAggregateRoot: Identified[Any], TWriteId](
    BaseWriteRepository[TWriteAggregateRoot, TWriteId],
):
    """In-memory implementation of WriteOnlyRepository for command operations.

    Stores aggregates in a dictionary keyed by their identifier. Designed
    for command-side usage in CQRS architectures.

    The storage mapping is injected via the constructor and copied on init
    to ensure independence from external mutation.
    """

    __slots__ = ()

    def __init__(
        self,
        storage: MutableMapping[TWriteId, TWriteAggregateRoot] | None = None,
    ) -> None:
        """Initialize the write repository with optional external storage.

        Args:
            storage: An optional mutable mapping to use as backing storage.
                If None, a new empty dictionary is used.

        """
        super().__init__(storage)
