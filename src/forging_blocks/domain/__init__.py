"""ForgingBlocks for domain-specific modules."""

from forging_blocks.foundation.specification import (
    AndSpecification,
    ExpressionSpecification,
    NotSpecification,
    OrSpecification,
    Specification,
)

from .aggregate_root import AggregateRoot, AggregateVersion
from .entity import Entity
from .errors import (
    DraftEntityIsNotHashableError,
    EntityIdDeletionError,
    EntityIdModificationError,
    EntityIdNoneError,
)
from .value_object import ValueObject

__all__ = [
    "DraftEntityIsNotHashableError",
    "EntityIdDeletionError",
    "EntityIdModificationError",
    "EntityIdNoneError",
    "Entity",
    "AggregateRoot",
    "AggregateVersion",
    "ValueObject",
    "Specification",
    "ExpressionSpecification",
    "AndSpecification",
    "OrSpecification",
    "NotSpecification",
]
