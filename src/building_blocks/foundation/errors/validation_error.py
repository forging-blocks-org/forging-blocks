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
