"""Domain value objects module.

This module provides the base ValueObject class for implementing domain value objects
following the principles of Domain-Driven Design (DDD).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Hashable
from typing import Any, Generic, TypeVar

RawValueType = TypeVar("RawValueType", covariant=True)


class ValueObject(ABC, Generic[RawValueType]):
    """Base class for all domain value objects.

    Value objects are immutable objects defined entirely by their attributes
    rather than by an identity. Two value objects with the same attributes
    are considered equal.

    This base class enforces immutability after initialization by blocking
    all further attribute assignments once frozen.

    Example:
        >>> class Email(ValueObject[str]):
        ...     __slots__ = ("_value",)
        ...
        ...     def __init__(self, value: str):
        ...         super().__init__()
        ...         if "@" not in value:
        ...             raise ValueError("Invalid email format")
        ...         self._value = value
        ...         self._freeze()
        ...
        ...     @property
        ...     def value(self) -> str:
        ...         return self._value
        ...
        ...     def _equality_components(self) -> tuple[Hashable, ...]:
        ...         return (self._value,)
    """

    __is_frozen: bool = False

    def __init__(self) -> None:
        """Initialize the value object in a mutable state (for setup)."""
        object.__setattr__(self, "_ValueObject__is_frozen", False)

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent modification once frozen."""
        immutability_error_message = (
            f"{self.__class__.__name__} is immutable: cannot modify '{name}' after initialization"
        )
        if getattr(self, "_ValueObject__is_frozen", False):
            raise AttributeError(immutability_error_message)
        object.__setattr__(self, name, value)

    def __eq__(self, other: object) -> bool:
        """Check equality based on equality components."""
        if not isinstance(other, self.__class__):
            return False
        return self._equality_components() == other._equality_components()

    def __hash__(self) -> int:
        """Generate hash based on equality components."""
        return hash(self._equality_components())

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        components = self._equality_components()
        if len(components) == 1:
            return f"{self.__class__.__name__}({components[0]!r})"
        return f"{self.__class__.__name__}{components!r}"

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return self.__str__()

    @property
    @abstractmethod
    def value(self) -> RawValueType:
        """Get the primary raw value encapsulated by the ValueObject."""
        pass

    def _freeze(self) -> None:
        """Freeze the object to enforce immutability."""
        object.__setattr__(self, "_ValueObject__is_frozen", True)

    @abstractmethod
    def _equality_components(self) -> tuple[Hashable, ...]:
        """Return the components used for equality comparison."""
        pass
