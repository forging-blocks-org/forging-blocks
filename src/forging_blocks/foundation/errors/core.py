"""Core error components for the building blocks foundation.

Defines fundamental data structures for error messages, metadata, and field references.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import cast


@dataclass(frozen=True)
class ErrorMessage:
    """Represents an immutable error message component."""

    value: str


@dataclass(frozen=True)
class ErrorMetadata[T: Mapping[str, object]]:
    """Represents metadata about the error."""

    context: T = field(default_factory=lambda: cast(T, {}))


@dataclass(frozen=True)
class FieldReference:
    """Represents a reference to a field in the error message."""

    value: str
