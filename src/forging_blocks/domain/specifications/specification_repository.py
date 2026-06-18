"""Specification-aware repository protocol.

Extends ``ReadOnlyRepository`` with query methods that accept
``Specification`` predicates for in-memory filtering.
"""

from collections.abc import Sequence
from typing import Protocol

from forging_blocks.application.ports.outbound.repository import ReadOnlyRepository
from forging_blocks.domain.specifications.specification import Specification


class SpecificationRepository[TEntity, TId](ReadOnlyRepository[TEntity, TId], Protocol):
    """Repository that supports specification-based queries.

    In addition to standard read-only operations, this interface
    allows querying by ``Specification`` predicates.
    """

    async def find_matching(self, spec: Specification[TEntity]) -> Sequence[TEntity]:
        """Return all entities that satisfy the specification."""
        ...

    async def count_matching(self, spec: Specification[TEntity]) -> int:
        """Return the count of entities satisfying the specification."""
        ...

    async def exists_matching(self, spec: Specification[TEntity]) -> bool:
        """Return ``True`` if at least one entity satisfies the specification."""
        ...
