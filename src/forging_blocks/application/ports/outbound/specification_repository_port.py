"""Specification-aware repository port.

Extends ``ReadOnlyRepository`` with query methods that accept
``Specification`` predicates for in-memory filtering.
"""

from abc import abstractmethod
from collections.abc import Sequence

from forging_blocks.application.ports.outbound.repository_port import ReadOnlyRepositoryPort
from forging_blocks.foundation.specification import Specification


class SpecificationRepositoryPort[TEntity, TId](ReadOnlyRepositoryPort[TEntity, TId]):
    """Read-only repository port with Specification-based query support.

    In addition to standard read-only operations, this interface
    allows querying by ``Specification`` predicates.

    Responsibilities:
        - Find all entities matching a ``Specification`` predicate.
        - Count entities satisfying a specification.
        - Check whether any entity matches a specification.

    Non-Responsibilities:
        - Compile or optimize ``Specification`` predicates.
        - Paginate or sort specification results.
        - Provide indexing strategies — that belongs to infrastructure.
    """

    @abstractmethod
    async def find_matching(self, spec: Specification[TEntity]) -> Sequence[TEntity]:
        """Return all entities that satisfy the specification."""
        ...

    @abstractmethod
    async def count_matching(self, spec: Specification[TEntity]) -> int:
        """Return the count of entities satisfying the specification."""
        ...

    @abstractmethod
    async def exists_matching(self, spec: Specification[TEntity]) -> bool:
        """Return ``True`` if at least one entity satisfies the specification."""
        ...
