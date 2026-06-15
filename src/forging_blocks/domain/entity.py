"""Base Entity class for domain blocks."""

from __future__ import annotations

import inspect
from abc import ABC
from collections.abc import Hashable
from typing import Any, cast

from forging_blocks.domain.errors import (
    DraftEntityIsNotHashableError,
    EntityIdDeletionError,
    EntityIdModificationError,
)
from forging_blocks.foundation.autofreeze import auto_freeze


class Entity[TId: Hashable](ABC):
    """Base class for all domain entities.

    An entity is defined by its identity rather than its attributes. Two entities with the same
    identifier are considered equal, regardless of their other attributes.

    Concrete subclasses are automatically frozen (selective freeze on '_id') after ``__init__``
    completes. Intermediate abstract classes remain unfrozen so their concrete leaf subclasses
    can finish setting up via ``super().__init__()``.
    """

    _id: TId | None

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Automatically apply selective freeze to concrete subclasses."""
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            auto_freeze(attrs=["_id"])(cls)

    def __init__(self, entity_id: TId | None) -> None:
        object.__setattr__(self, "_id", entity_id)

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent modification of '_id' once set to a non-None value."""
        frozen_attrs = getattr(self, "_autofreeze__frozen_attrs", None)

        if (
            frozen_attrs is not None
            and name in frozen_attrs
            and name == "_id"
            and getattr(self, "_id", None) is not None
            and value != self._id
        ):
            raise EntityIdModificationError(
                class_name=self.__class__.__name__,
                attribute_name=name,
                current_value=self._id,
            )

        object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        """Prevent deletion of '_id'."""
        if name == "_id":
            raise EntityIdDeletionError(class_name=self.__class__.__name__)
        object.__delattr__(self, name)

    def __eq__(self, other: object) -> bool:
        """Check equality based on type and identifier."""
        if type(self) is not type(other):
            return False

        other_entty = cast(Entity[TId], other)

        if self._id is None or other_entty._id is None:
            return self is other_entty

        return self._id == other_entty._id

    def __hash__(self) -> int:
        """Return the hash based on the entity's identifier.

        Raises:
            DraftEntityIsNotHashableError: If the entity is a draft (id is None).
        """
        if self._id is None:
            raise DraftEntityIsNotHashableError.from_class_name(self.__class__.__name__)
        return hash((self.__class__, self._id))

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
