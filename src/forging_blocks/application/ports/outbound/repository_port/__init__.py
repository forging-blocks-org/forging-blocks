"""Generic repository interfaces for Domain-Driven Design.

This package defines repository interfaces used to persist and retrieve
aggregate roots. Repositories abstract infrastructure concerns and offer
type-safe contracts for both command-side and query-side data access in
CQRS or traditional architectures.

Responsibilities:
    - Persist and retrieve aggregates.
    - Abstract away storage mechanisms.

Non-Responsibilities:
    - Implement business invariants (aggregate enforces them).
    - Expose ORM models or database APIs directly.
"""

from ._read_only_repository_port import ReadOnlyRepositoryPort
from ._repository_port import RepositoryPort
from ._write_only_repository_port import WriteOnlyRepositoryPort

__all__ = [
    "ReadOnlyRepositoryPort",
    "RepositoryPort",
    "WriteOnlyRepositoryPort",
]
