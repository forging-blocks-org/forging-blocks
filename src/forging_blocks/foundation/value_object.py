"""Domain value objects module.

This module provides the base ValueObject class for implementing domain value objects
following the principles of Domain-Driven Design (DDD).
"""

import inspect
from abc import ABC, abstractmethod
from collections.abc import Hashable
from typing import Any

from forging_blocks.foundation.autofreeze import auto_freeze
from forging_blocks.foundation.errors.cant_modify_immutable_attribute_error import (
    CantModifyImmutableAttributeError,
)


class ValueObject[RawValueType](ABC):
    """Base class for all domain value objects.
    rather than by an identity. Two value objects with the same attributes
    are considered equal.

    Concrete subclasses are automatically frozen after ``__init__`` completes.
    Intermediate abstract classes remain unfrozen so their concrete leaf
    subclasses can finish setting up via ``super().__init__()``.

    Example:
        ```python
        class Email(ValueObject[str]):
            __slots__ = ("_value",)

            def __init__(self, value: str):
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

    __is_frozen: bool = False

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Automatically freeze concrete subclasses after __init__ completes."""
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            auto_freeze(cls)

    def __init__(self) -> None:
        object.__setattr__(self, "_ValueObject__is_frozen", False)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_ValueObject__is_frozen", False):
            raise CantModifyImmutableAttributeError(
                class_name=self.__class__.__name__,
                attribute_name=name,
            )
        object.__setattr__(self, name, value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
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

    def freeze_instance(self) -> None:
        """Make the instance immutable. Raises CantModifyImmutableAttributeError on attr set."""
        object.__setattr__(self, "_ValueObject__is_frozen", True)

    def _freeze(self) -> None:
        """Freeze the object. Delegates to freeze_instance()."""
        self.freeze_instance()
