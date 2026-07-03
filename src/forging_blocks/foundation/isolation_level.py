"""Standard ANSI SQL isolation levels."""

from enum import StrEnum


class IsolationLevel(StrEnum):
    """Standard ANSI SQL isolation levels."""

    READ_UNCOMMITTED = "read_uncommitted"
    READ_COMMITTED = "read_committed"
    REPEATABLE_READ = "repeatable_read"
    SERIALIZABLE = "serializable"
