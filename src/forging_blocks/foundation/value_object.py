"""Domain value objects module.

This module provides the base ValueObject class for implementing domain value objects
following the principles of Domain-Driven Design (DDD).
"""

import inspect
from abc import ABC, abstractmethod
from typing import Any

from forging_blocks.foundation.autofreeze import auto_freeze
from forging_blocks.foundation.autohash import auto_hash


class ValueObject[RawValueType](ABC):
    """Base class for all domain value objects.

    Value objects are immutable objects defined entirely by their attributes
    rather than by an identity. Two value objects with the same attributes
    are considered equal.

    Concrete subclasses are automatically frozen and hashable via
    :func:`auto_freeze` and :func:`auto_hash`, which generate
    ``__hash__`` / ``__eq__`` from slot fields and enforce
    immutability.  Intermediate abstract classes are skipped so leaf
    subclasses finish their own ``__init__`` without restriction.

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
        ```

    """

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Apply ``auto_freeze`` and ``auto_hash`` to concrete subclasses.

        ``auto_freeze`` enforces immutability; ``auto_hash`` generates
        ``__hash__`` / ``__eq__`` from class fields.
        """
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            auto_freeze(cls)
            auto_hash(cls)

    def __str__(self) -> str:
        field_names = getattr(self, "__auto_hash_fields__", ())
        components = tuple(getattr(self, name) for name in field_names)
        if len(components) == 1:
            return f"{self.__class__.__name__}({components[0]!r})"
        return f"{self.__class__.__name__}{components!r}"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    @abstractmethod
    def value(self) -> RawValueType:
        """Return the primary raw value encapsulated by the ValueObject."""
