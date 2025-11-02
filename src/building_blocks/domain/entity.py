"""Domain entities module.

This module provides the base Entity class for implementing domain entities.
following the principles of Domain-Driven Design (DDD).

It includes methods for equality comparison and string representation.
"""

from __future__ import annotations

from abc import ABC
from collections.abc import Hashable
from typing import Generic, TypeVar

TId = TypeVar("TId", bound=Hashable)  # Type variable for the entity's unique identifier


class Entity(Generic[TId], ABC):
    """Base class for all domain entities with identity.

    Entities are objects that have a distinct identity that runs through time and
    different states. They are defined by their identity rather than their attributes.
    Two entities with the same identifier are considered equal, even if their
    attributes differ.

    Args:
        id (TId): The unique identifier for the entity.

    Type Parameters:
        TId: Type of the entity's unique identifier

    Example:
        >>> class User(Entity[str]):
        ...     def __init__(self, id: str, name: str):
        ...         super().__init__(id)
        ...         self.name = name
    """

    def __init__(self, id: TId) -> None:
        if id is None:
            raise ValueError("Entity ID cannot be None")
        self._id = id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return bool(self.id == other.id)

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def id(self) -> TId:
        """Returns the unique identifier of the entity.

        Returns:
            TId: The unique identifier of the entity.
        """
        return self._id
