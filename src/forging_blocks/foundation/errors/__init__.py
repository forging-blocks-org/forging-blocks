"""ForgingBlocks foundation.errors package initialization."""

from .base import Error, NoneNotAllowedError
from .cant_modify_immutable_attribute_error import CantModifyImmutableAttributeError
from .core import ErrorMessage, ErrorMetadata, FieldReference
from .rule_violation_error import RuleViolationError
from .validation_error import (
    CombinedValidationErrors,
    ValidationError,
    ValidationFieldErrors,
)

__all__ = [
    "Error",
    "NoneNotAllowedError",
    "CantModifyImmutableAttributeError",
    "ErrorMessage",
    "ErrorMetadata",
    "FieldReference",
    "RuleViolationError",
    "ValidationError",
    "ValidationFieldErrors",
    "CombinedValidationErrors",
]
