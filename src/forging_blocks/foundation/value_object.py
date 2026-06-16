"""Domain value objects module.

This module provides the base ValueObject class for implementing domain value objects
following the principles of Domain-Driven Design (DDD).
"""

import inspect
from abc import ABC, abstractmethod
from collections.abc import Hashable
from typing import Any

from forging_blocks.foundation.autofreeze import auto_freeze


@auto_freeze
class ValueObject[RawValueType](ABC):
    """Base class for all domain value objects.

    Value objects are immutable objects defined entirely by their attributes
    rather than by an identity. Two value objects with the same attributes
    are considered equal.

    Concrete subclasses are automatically frozen after ``__init__`` completes.
    Intermediate abstract classes remain unfrozen so their concrete leaf
    subclasses can finish setting up via ``super().__init__()``.

    Example:
        ```python
        class Email(ValueObject[str]):
            __slots__ = ("_value",)

            def __init__(self, value: str) -> None:
                super().__init__()
                if "@" not in value:
                    raise ValueError("Invalid email format")
                self._value = value

            @property
            def value(self) -> str:
                return self._value

            @property
            def _equality_components(self) -> tuple[Hashable, ...]:
                return (self._value,)
        ```
    """

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Automatically apply auto_freeze to concrete subclasses."""
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            auto_freeze(cls)

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        return self._equality_components == other._equality_components

    def __hash__(self) -> int:
        return hash(self._equality_components)

    def __str__(self) -> str:
        components = self._equality_components
        if len(components) == 1:
            return f"{self.__class__.__name__}({components[0]!r})"
        return f"{self.__class__.__name__}{components!r}"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    @abstractmethod
    def value(self) -> RawValueType:
        """Return the primary raw value encapsulated by the ValueObject."""

    @property
    @abstractmethod
    def _equality_components(self) -> tuple[Hashable, ...]:
        """Return the components used for equality and hashing."""
