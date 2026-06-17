"""Modules defining validation error classes.

Defines error classes related to validation failures within the system.
"""

from forging_blocks.foundation.errors.combined_errors import CombinedErrors
from forging_blocks.foundation.errors.error import Error
from forging_blocks.foundation.errors.field_errors import FieldErrors


class ValidationError(Error[dict[str, object]]):
    """Base class for validation errors."""


class ValidationFieldErrors(FieldErrors[Error[dict[str, object]]]):
    """Validation errors associated with a specific field."""


class CombinedValidationErrors(CombinedErrors[ValidationFieldErrors]):
    """Aggregates multiple validation errors for easier handling and reporting."""
