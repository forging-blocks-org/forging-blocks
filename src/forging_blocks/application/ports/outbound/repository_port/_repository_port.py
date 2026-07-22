"""Full CRUD repository abstraction combining read and write interfaces."""

from ._read_only_repository_port import ReadOnlyRepositoryPort
from ._write_only_repository_port import WriteOnlyRepositoryPort


class RepositoryPort[TAggregateRoot, TId](
    ReadOnlyRepositoryPort[TAggregateRoot, TId],
    WriteOnlyRepositoryPort[TAggregateRoot, TId],
):
    """Full CRUD repository abstraction.

    Combines read and write capabilities into a single repository interface.
    Suitable for non-CQRS applications or simplified contexts.
    """

    ...
