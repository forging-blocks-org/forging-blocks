"""In-memory read-only repository backed by a dictionary.

Provides a concrete implementation of ReadOnlyRepositoryPort for
query-side operations in CQRS architectures. Storage is a plain
dictionary keyed by entity identifier.
"""

from collections.abc import Mapping, Sequence

from forging_blocks.application.ports.outbound.repository_port import ReadOnlyRepositoryPort
from forging_blocks.domain.specification import Specification


class InMemoryReadRepository[TEntity, TId](ReadOnlyRepositoryPort[TEntity, TId]):
    """In-memory read-only repository backed by a dictionary.

    Stores entities in a dictionary keyed by their identifier. Designed
    for query-side usage in CQRS architectures or single-process contexts.

    The storage mapping is injected via the constructor and copied on init
    to ensure independence from external mutation.
    """

    def __init__(self, storage: Mapping[TId, TEntity] | None = None) -> None:
        """Initialize the read repository with optional external storage.

        Args:
            storage: An optional mapping to use as backing storage.
                If None, a new empty dictionary is used.

        """
        super().__init__()
        self._storage: dict[TId, TEntity] = dict(storage) if storage is not None else {}

    async def get_by_id(self, id: TId) -> TEntity | None:  # noqa: A002
        """Retrieve an entity by ID.

        Args:
            id: Unique identifier of the entity.

        Returns:
            The entity if found, otherwise None.

        """
        return self._storage.get(id)

    async def list_all(self) -> Sequence[TEntity]:
        """Retrieve all resources in the repository.

        Returns:
            A sequence of all stored entities.

        """
        return list(self._storage.values())

    async def find_matching(self, spec: Specification[TEntity]) -> Sequence[TEntity]:
        """Return all stored entities that satisfy the given specification.

        Args:
            spec: Specification predicate to filter entities.

        Returns:
            A list of matching entities.

        """
        return [v for v in self._storage.values() if spec.is_satisfied_by(v)]

    async def count_matching(self, spec: Specification[TEntity]) -> int:
        """Return the count of entities satisfying the specification.

        Args:
            spec: Specification predicate to filter entities.

        Returns:
            The number of matching entities.

        """
        return sum(1 for v in self._storage.values() if spec.is_satisfied_by(v))

    async def exists_matching(self, spec: Specification[TEntity]) -> bool:
        """Return True if at least one entity satisfies the specification.

        Args:
            spec: Specification predicate to filter entities.

        Returns:
            True if at least one entity matches, False otherwise.

        """
        return any(spec.is_satisfied_by(v) for v in self._storage.values())
