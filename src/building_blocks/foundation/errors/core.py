"""
This module contains core error components used throughout the application.
These components provide structured representations for error messages,
metadata, and field references, facilitating consistent error handling and reporting.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ErrorMessage:
    """Represents an immutable error message component."""

    value: str


@dataclass(frozen=True)
class ErrorMetadata:
    """Represents metadata about the error."""

    context: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FieldReference:
    """Represents a reference to a field in the error message."""

    value: str
