"""Infrastructure error classes for repository operations."""

from .repository_errors import RepositoryError, RepositoryNotFoundError

__all__ = [
    "RepositoryError",
    "RepositoryNotFoundError",
]
