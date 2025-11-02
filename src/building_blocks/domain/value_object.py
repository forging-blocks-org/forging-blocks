"""Domain value objects module.

This module provides the base ValueObject class for implementing domain value objects
following the principles of Domain-Driven Design (DDD).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Hashable


class ValueObject(ABC):
    """Base class for all domain value objects.

    Value objects are immutable objects that are defined by their attributes
    rather than their identity. Two value objects with the same attributes
    are considered equal.

    Value objects should be implemented as immutable by using properties
    without setters and avoiding direct attribute modification.

    Example:
        >>> class Email(ValueObject):
        ...     def __init__(self, value: str):
        ...         if "@" not in value:
        ...             raise ValueError("Invalid email format")
        ...         self._value = value
        ...
        ...     @property
        ...     def value(self) -> str:
        ...         return self._value
        ...
        ...     def _equality_components(self) -> tuple[Hashable, ...]:
        ...         return (self._value,)
    """

    def __eq__(self, other: object) -> bool:
        """Check equality based on equality components.

        Args:
            other: Object to compare with

        Returns:
            bool: True if objects are equal, False otherwise
        """
        if not isinstance(other, self.__class__):
            return False
        return self._equality_components() == other._equality_components()

    def __hash__(self) -> int:
        """Generate hash based on equality components.

        Returns:
            int: Hash value for the object
        """
        return hash(self._equality_components())

    def __str__(self) -> str:
        """String representation of the value object.

        Returns:
            str: String representation
        """
        components = self._equality_components()
        if len(components) == 1:
            return f"{self.__class__.__name__}({components[0]})"
        return f"{self.__class__.__name__}{components}"

    def __repr__(self) -> str:
        """Developer representation of the value object.

        Returns:
            str: Developer representation
        """
        return self.__str__()

    @abstractmethod
    def _equality_components(self) -> tuple[Hashable, ...]:
        """Return the components used for equality comparison.

        This method should return a tuple containing all the attributes
        that define the value object's equality.

        Returns:
            tuple[Hashable, ...]: Tuple of components for equality comparison
        """
        pass
