"""Base repository classes for common functionality.

Provides shared infrastructure for repository implementations.
"""

from collections.abc import Mapping, MutableMapping, Sequence
from typing import Any

from forging_blocks.application.ports.outbound.repository import (
    ReadOnlyRepositoryPort,
    WriteOnlyRepositoryPort,
)
from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.identified import Identified
from forging_blocks.foundation.specification import Specification
from forging_blocks.infrastructure.errors.repository_errors import (
    RepositoryError,
    RepositoryNotFoundError,
)


class BaseReadRepository[TEntity, TId](ReadOnlyRepositoryPort[TEntity, TId]):
    """Base class for read-only repositories with common functionality.

    Provides in-memory storage and basic query operations.
    """

    __slots__ = ("_storage",)

    def __init__(self, storage: Mapping[TId, TEntity] | None = None) -> None:
        """Initialize the read repository with optional external storage.

        Args:
            storage: An optional mapping to use as backing storage.
                If None, a new empty dictionary is used.
        """
        self._storage: dict[TId, TEntity] = dict(storage) if storage is not None else {}

    async def get_by_id(self, id: TId) -> TEntity | None:  # noqa: A002
        """Retrieve an entity by ID.

        Args:
            id: Unique identifier of the resource.

        Returns:
            The retrieved instance or None if not found.
        """
        return self._storage.get(id)

    async def list_all(self) -> Sequence[TEntity]:
        """Retrieve all resources in the repository.

        Returns:
            A sequence of entity instances.
        """
        return list(self._storage.values())

    async def find_matching(self, spec: Specification[TEntity]) -> Sequence[TEntity]:
        """Return all stored entities that satisfy the given specification.

        Args:
            spec: The specification predicate to filter by.

        Returns:
            A list of matching entities.
        """
        return [v for v in self._storage.values() if spec.is_satisfied_by(v)]

    async def count_matching(self, spec: Specification[TEntity]) -> int:
        """Return the count of entities satisfying the specification.

        Args:
            spec: The specification predicate to filter by.

        Returns:
            The count of matching entities.
        """
        return sum(1 for v in self._storage.values() if spec.is_satisfied_by(v))

    async def exists_matching(self, spec: Specification[TEntity]) -> bool:
        """Return True if at least one entity satisfies the specification.

        Args:
            spec: The specification predicate to filter by.

        Returns:
            True if any entity matches, False otherwise.
        """
        return any(spec.is_satisfied_by(v) for v in self._storage.values())


class BaseWriteRepository[TEntity: Identified[Any], TId](WriteOnlyRepositoryPort[TEntity, TId]):
    """Base class for write-only repositories with common functionality.

    Provides in-memory storage and basic write operations with ID validation.
    """

    __slots__ = ()

    def __init__(
        self,
        storage: MutableMapping[TId, TEntity] | None = None,
    ) -> None:
        """Initialize the write repository with optional external storage.

        Args:
            storage: An optional mutable mapping to use as backing storage.
                If None, a new empty dictionary is used.
        """
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


class BaseRepository[TEntity: Identified[Any], TId](
    BaseReadRepository[TEntity, TId],
    BaseWriteRepository[TEntity, TId],
):
    """Full CRUD repository base class combining read and write operations.

    Suitable for non-CQRS applications or simplified contexts.
    """

    __slots__ = ()

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
