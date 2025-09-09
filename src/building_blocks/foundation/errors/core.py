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
