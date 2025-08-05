from typing import List

from building_blocks.abstractions.errors.core import ErrorMessage, FieldReference
from building_blocks.abstractions.errors.validation_error import (
    ValidationError,
    ValidationErrors,
)


class TestValidationError:
    def test__str__when_message_is_empty(self):
        error_message = ErrorMessage("")

        error = ValidationError(error_message)

        expected_error_string = "Validation Error: "
        assert str(error) == expected_error_string

    def test___str__when_message_is_defined_then_(self):
        error_message = ErrorMessage("This is a validation error.")

        error = ValidationError(error_message)

        assert str(error) == "Validation Error: This is a validation error."


class TestValidationErrors:
    def test__str__when_errors_are_empty(self):
        field = FieldReference("test_field")
        errors: List[ValidationError] = []

        validation_errors = ValidationErrors(field=field, errors=errors)

        assert str(validation_errors) == "Validation errors for field 'test_field':\n"

    def test__str__when_errors_are_defined(self):
        field = FieldReference("test_field")
        errors: List[ValidationError] = [
            ValidationError(ErrorMessage("Error 1")),
            ValidationError(ErrorMessage("Error 2")),
        ]

        validation_errors = ValidationErrors(field=field, errors=errors)

        expected = (
            "Validation errors for field 'test_field':\n"
            " - Validation Error: Error 1\n"
            " - Validation Error: Error 2"
        )
        assert str(validation_errors) == expected
