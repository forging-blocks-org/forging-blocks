"""ForgingBlocks for domain-specific modules."""

from .aggregate_root import AggregateRoot, AggregateVersion
from .entity import Entity
from .errors import (
    DraftEntityIsNotHashableError,
    EntityIdDeletionError,
    EntityIdModificationError,
    EntityIdNoneError,
)
from .specifications import (
    AndSpecification,
    ExpressionSpecification,
    NotSpecification,
    OrSpecification,
    Specification,
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
