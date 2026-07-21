"""ForgingBlocks foundation.errors package initialization."""

from .architecture_error import ArchitectureError
from .cant_modify_immutable_attribute_error import CantModifyImmutableAttributeError
from .combined_errors import CombinedErrors
from .core import ErrorMessage, ErrorMetadata, FieldReference
from .error import Error
from .field_errors import FieldErrors
from .non_hashable_value_error import NonHashableValueError
from .none_not_allowed_error import NoneNotAllowedError
from .result_access_error import ResultAccessError
from .rule_violation_error import CombinedRuleViolationErrors, RuleViolationError
from .validation_error import (
    CombinedValidationErrors,
    ValidationError,
    ValidationFieldErrors,
)

__all__ = [
    "ArchitectureError",
    "CombinedErrors",
    "CombinedRuleViolationErrors",
    "Error",
    "NonHashableValueError",
    "FieldErrors",
    "NoneNotAllowedError",
    "CantModifyImmutableAttributeError",
    "ErrorMessage",
    "ErrorMetadata",
    "FieldReference",
    "ResultAccessError",
    "RuleViolationError",
    "ValidationError",
    "ValidationFieldErrors",
    "CombinedValidationErrors",
]
