"""In-memory write-only repository backed by a dictionary.

Provides a concrete implementation of WriteOnlyRepositoryPort for
command-side operations in CQRS architectures. Storage is a plain
dictionary keyed by entity identifier.
"""

from collections.abc import MutableMapping
from typing import Any

from forging_blocks.application.ports.outbound.repository_port import WriteOnlyRepositoryPort
from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.identified import Identified
from forging_blocks.infrastructure.errors.repository_errors import (
    RepositoryError,
    RepositoryNotFoundError,
)


class InMemoryWriteRepository[TEntity: Identified[Any], TId](WriteOnlyRepositoryPort[TEntity, TId]):
    """In-memory write-only repository backed by a dictionary.

    Stores entities in a dictionary keyed by their identifier. Designed
    for command-side usage in CQRS architectures or single-process contexts.

    The storage mapping is injected via the constructor and copied on init
    to ensure independence from external mutation.
    """

    def __init__(
        self,
        storage: MutableMapping[TId, TEntity] | None = None,
    ) -> None:
        """Initialize the write repository with optional external storage.

        Args:
            storage: An optional mutable mapping to use as backing storage.
                If None, a new empty dictionary is used.

        """
        super().__init__()
        self._storage: dict[TId, TEntity] = dict(storage) if storage is not None else {}

    async def delete_by_id(self, id: TId) -> None:  # noqa: A002
        """Delete an entity by ID.

        Args:
            id: Unique identifier of the entity.

        Raises:
            RepositoryError: If the ID is None, an empty string,
                or the boolean False.
            RepositoryNotFoundError: If no entity exists with the given ID.

        """
        self._validate_id(id)
        if id not in self._storage:
            raise RepositoryNotFoundError.for_id(id)
        del self._storage[id]

    async def save(self, aggregate: TEntity) -> None:
        """Persist an entity instance.

        Args:
            aggregate: The entity to save.

        Raises:
            RepositoryError: If the entity has no valid identifier
                (None, empty string, or boolean False).

        """
        entity_id: TId = aggregate.id  # type: ignore[assignment]
        self._validate_id(entity_id)
        self._storage[entity_id] = aggregate

    @staticmethod
    def _validate_id(identifier: object) -> None:
        """Validate that an entity identifier is not None, empty, or False.

        Mirrors the validation performed by
        ``AggregateRoot._validate_identity`` so that the repository
        independently guards against invalid identifiers.

        Raises:
            RepositoryError: If *identifier* is ``None``, an empty string
                (``""``), or the boolean ``False``.

        """
        is_none = identifier is None
        is_empty_string = identifier == ""
        is_false = identifier is False

        if is_none or is_empty_string or is_false:
            raise RepositoryError(
                ErrorMessage(
                    "Invalid entity identifier (must not be None, empty string, or False)."
                )
            )
