"""Base Entity class for domain layer."""

from __future__ import annotations

from abc import ABC
from collections.abc import Hashable
from typing import Any, Generic, TypeVar

from building_blocks.domain.errors.draft_entity_is_not_hashable_error import (
    DraftEntityIsNotHashableError,
)

TId = TypeVar("TId", bound=Hashable)


class Entity(Generic[TId], ABC):
    """Base class for all domain entities.

    An entity is defined by its identity rather than its attributes. Two entities with the same
    identifier are considered equal, regardless of their other attributes.
    """

    _id: TId | None
    __is_frozen: bool

    def __init__(self, entity_id: TId | None) -> None:
        object.__setattr__(self, "_id", entity_id)
        object.__setattr__(self, "_Entity__is_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent modification of '_id' once set."""
        if (
            getattr(self, "_Entity__is_frozen", False)
            and name == "_id"
            and getattr(self, "_id", None) is not None
            and value != self._id
        ):
            raise AttributeError(
                f"{self.__class__.__name__}: cannot modify '{name}' once set "
                f"(current value={self._id!r})."
            )
        object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        """Prevent deletion of '_id'."""
        if name == "_id":
            raise AttributeError(f"{self.__class__.__name__}: cannot delete 'id'.")
        object.__delattr__(self, name)

    def __eq__(self, other: object) -> bool:
        """Check equality based on type and identifier."""
        if type(self) is not type(other):
            return False
        assert isinstance(other, Entity)
        if self._id is None or other._id is None:
            return self is other
        return self._id == other._id

    def __hash__(self) -> int:
        """Return the hash based on the entity's identifier.

        Raises:
            DraftEntityIsNotHashableError: If the entity is a draft (id is None).
        """
        if self._id is None:
            raise DraftEntityIsNotHashableError.from_class_name(self.__class__.__name__)
        return hash(self._id)

    def __str__(self) -> str:
        """Return a user-friendly string representation of the entity."""
        return f"{self.__class__.__name__}(id={self._id})"

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the entity."""
        return str(self)

    @property
    def id(self) -> TId | None:
        """Return the entity's identifier, or None if it's a draft entity."""
        return self._id

    def is_persisted(self) -> bool:
        """Return True if the entity has a defined identifier (i.e., is persisted)."""
        return self._id is not None
