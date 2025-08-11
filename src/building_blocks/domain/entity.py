"""
Base entity classes for domain-driven design (DDD) entities.
Includes:
- BaseEntity: Common logic for identity handling.
- Entity: Persisted entities (must have ID at creation).
- DraftEntity: Non-persisted entities (ID may be None until saved).
"""

from __future__ import annotations

from abc import ABC
from collections.abc import Hashable
from typing import Generic, Optional, TypeVar

from building_blocks.domain.errors.entity_id_errors import (
    DraftEntityIsNotHashableError,
    EntityIdCannotBeNoneError,
)

TId = TypeVar("TId", bound=Hashable)


class BaseEntity(Generic[TId], ABC):
    """
    Base class for domain entities.
    Identity is immutable once set.
    """

    __slots__ = ("_id",)

    def __init__(self, entity_id: Optional[TId]) -> None:
        self._id: Optional[TId] = entity_id

    @property
    def id(self) -> Optional[TId]:
        """The unique identifier of the entity (may be None for drafts)."""
        return self._id

    def __eq__(self, other: object) -> bool:
        """
        Default equality:
        - For persisted entities: same type & same ID.
        - For drafts: overridden in DraftEntity.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Entities can only be hashed if they have a non-null ID."""
        if self.id is None:
            raise TypeError(f"Unhashable {self.__class__.__name__}: id is None")
        return hash(self.id)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self) -> str:
        return str(self)


class Entity(BaseEntity[TId], ABC):
    """
    Base class for entities that must have an ID at creation.
    """

    def __init__(self, entity_id: TId) -> None:
        if entity_id is None:
            raise EntityIdCannotBeNoneError()
        super().__init__(entity_id)


class DraftEntity(BaseEntity[TId], ABC):
    """
    Base class for entities that may start without an ID (drafts).
    Drafts:
    - Compare equal only if they are the same instance when id is None.
    - Are never hashable.
    """

    def __init__(self, entity_id: Optional[TId] = None) -> None:
        super().__init__(entity_id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self.id is None or other.id is None:
            return self is other
        return self.id == other.id

    def __hash__(self) -> int:
        raise DraftEntityIsNotHashableError()
