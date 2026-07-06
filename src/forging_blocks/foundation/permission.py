"""Granular permission identifiers for authorization checks."""

from enum import StrEnum


class Permission(StrEnum):
    """Granular permission identifiers for authorization checks."""

    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
