"""Domain entities module.

This module provides base classes for domain entities.
"""

from __future__ import annotations

from abc import ABC
from collections.abc import Hashable
from typing import Any, Generic, TypeVar

from building_blocks.domain.errors.draft_entity_is_not_hashable_error import (
    DraftEntityIsNotHashableError,
)

TId = TypeVar("TId", bound=Hashable)


class Entity(Generic[TId], ABC):
    """Base class for domain entities.

    Entities represent objects with identity. The identity (ID) may be:
      - `None`: Draft entity before persistence (e.g., DB autogenerates ID)
      - A valid ID: Assigned before or during construction

    Behavior:
      - Equality: by ID if both have IDs, otherwise by identity (`is`)
      - Hashing: allowed only for persisted entities (ID is not None)
      - ID immutability: `_id` cannot be modified or deleted once set
      - No `set_id()` method — lifecycle controlled by Python data model
    """

    _id: TId | None
    __is_frozen: bool

    def __init__(self, entity_id: TId | None) -> None:
        object.__setattr__(self, "_id", entity_id)
        object.__setattr__(self, "_Entity__is_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent reassignment of the ID after initialization."""
        if name == "_id" and getattr(self, "_id", None) is not None:
            raise AttributeError(f"Cannot modify 'id' once set ({self._id!r}).")
        object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        """Prevent deletion of the ID."""
        if name == "_id":
            raise AttributeError("Cannot delete 'id'.")
        object.__delattr__(self, name)

    @property
    def id(self) -> TId | None:
        """Unique identifier (may be None for drafts)."""
        return self._id

    def is_persisted(self) -> bool:
        """Check if the entity has a defined (non-None) ID."""
        return self._id is not None

    def __eq__(self, other: object) -> bool:
        """Entity equality comparison magic method.

        Entities are equal if:
        - They are of the same class AND
        - Both have IDs and IDs are equal
        Otherwise, identity equality (same instance).
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self._id is None or other._id is None:
            return self is other
        return self._id == other._id

    def __hash__(self) -> int:
        """Hash based on ID; drafts are not hashable."""
        if self._id is None:
            raise DraftEntityIsNotHashableError.from_class_name(self.__class__.__name__)
        return hash(self._id)

    def __str__(self) -> str:
        """Readable representation showing ID."""
        return f"{self.__class__.__name__}(id={self._id})"

    def __repr__(self) -> str:
        """Concise representation for debugging."""
        return str(self)
