"""ForgingBlocks for domain-specific modules."""

from .aggregate_root import AggregateRoot, AggregateVersion
from .entity import Entity
from .errors import (
    DraftEntityIsNotHashableError,
    EntityIdDeletionError,
    EntityIdModificationError,
    EntityIdNoneError,
)
from .messages import Command, Event, Message, Query
from .permissions.composite_permission_checker import CompositePermissionChecker
from .permissions.permission_checker import PermissionChecker
from .permissions.resource_permission_checker import ResourcePermissionChecker
from .permissions.role_based_permission_checker import RoleBasedPermissionChecker
from .specification import (
    AndSpecification,
    ExpressionSpecification,
    NotSpecification,
    OrSpecification,
    Specification,
)
from .validators.composite_validation_rule import CompositeValidationRule
from .validators.email_validator import EmailValidator
from .validators.length_validator import LengthValidator
from .validators.range_validator import RangeValidator
from .validators.required_validator import RequiredValidator
from .value_object import ValueObject

__all__ = [
    "AggregateRoot",
    "AggregateVersion",
    "AndSpecification",
    "Command",
    "CompositePermissionChecker",
    "CompositeValidationRule",
    "DraftEntityIsNotHashableError",
    "EmailValidator",
    "Entity",
    "EntityIdDeletionError",
    "EntityIdModificationError",
    "EntityIdNoneError",
    "Event",
    "ExpressionSpecification",
    "LengthValidator",
    "Message",
    "NotSpecification",
    "OrSpecification",
    "PermissionChecker",
    "Query",
    "RangeValidator",
    "RequiredValidator",
    "ResourcePermissionChecker",
    "RoleBasedPermissionChecker",
    "Specification",
    "ValueObject",
]
