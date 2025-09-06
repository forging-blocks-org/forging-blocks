from building_blocks.foundation.errors.core import ErrorMessage, FieldReference
from building_blocks.foundation.errors.validation_error import (
    CombinedValidationErrors,
    ValidationError,
    ValidationFieldErrors,
)


class TestValidationError:
    def test_constructor(self) -> None:
        message = ErrorMessage("Validation failed")

        error = ValidationError(message)

        assert isinstance(error, ValidationError)


class TestValidationFieldErrors:
    def test_constructor(self) -> None:
        message = ErrorMessage("Username validation failed")
        error = ValidationError(message)
        field = FieldReference("username")

        errors = ValidationFieldErrors(field, [error])

        assert isinstance(errors, ValidationFieldErrors)


class TesCombinedValidationErrors:
    def test_constructor(self) -> None:
        message = ErrorMessage("Username validation failed")
        error = ValidationError(message)
        field = FieldReference("username")
        field_errors = ValidationFieldErrors(field, [error])

        errors = CombinedValidationErrors([field_errors])

        assert isinstance(errors, CombinedValidationErrors)
