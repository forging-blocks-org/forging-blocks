"""
Validation error classes for handling validation-related issues.

These classes provide a structured way to represent validation errors,
including field-specific errors and aggregated validation errors.

Classes:
- ValidationError: Base class for validation errors.
- ValidationFieldErrors: Validation errors associated with a specific field.
- CombinedValidationErrors: Aggregates multiple validation errors for easier handling
and reporting.
"""

from building_blocks.foundation.errors.base import CombinedErrors, Error, FieldErrors


class ValidationError(Error):
    """
    Base class for validation errors.
    """


class ValidationFieldErrors(FieldErrors):
    """
    Validation errors associated with a specific field.
    """


class CombinedValidationErrors(CombinedErrors[ValidationFieldErrors]):
    """
    Aggregates multiple validation errors for easier handling and reporting.
    """
