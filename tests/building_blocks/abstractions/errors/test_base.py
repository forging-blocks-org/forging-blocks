from building_blocks.abstractions.errors.base import Error, Errors
from building_blocks.abstractions.errors.core import (
    ErrorMessage,
    ErrorMetadata,
    FieldReference,
)


class TestError:
    def test_message_when_message_defined_then_returns_message(self) -> None:
        message = ErrorMessage("An error occurred")
        error = Error(message)

        actual_message_content = error.message

        expected_message_content = ErrorMessage("An error occurred")
        assert actual_message_content == expected_message_content

    def test_metadata_when_metadata_defined_then_returns_metadata(self) -> None:
        metadata = ErrorMetadata({"key": "value"})
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message, metadata)

        actual_metadata = error.metadata

        expected_metadata = ErrorMetadata({"key": "value"})
        assert actual_metadata == expected_metadata

    def test_metadata_when_metadata_not_defined_then_returns_context_as_empty_dict(
        self,
    ) -> None:
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)

        actual_metadata = error.metadata

        expected_metadata = ErrorMetadata({})
        assert actual_metadata == expected_metadata

    def test__str__when_message_defined_then_returns_message(self) -> None:
        message = "An error occurred"
        error_message = ErrorMessage(message)

        error_message = Error(error_message)

        expected = "An error occurred"
        assert str(error_message) == expected

    def test__str__when_message_is_empty_string_then_returns_empty_string(self) -> None:
        error_message = ErrorMessage("")

        error_message = Error(error_message)

        expected = ""
        assert str(error_message) == expected


class TestErrors:
    def test_field_when_field_defined_then_returns_field(self) -> None:
        field = FieldReference("username")
        errors = Errors(field=field, errors=[])

        actual_field = errors.field

        expected_field = FieldReference("username")
        assert actual_field == expected_field

    def test_errors_when_errors_defined_then_returns_errors(self) -> None:
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        errors = Errors(errors=[error], field=FieldReference("username"))

        actual_errors = errors.errors

        expected_errors = [error]
        assert actual_errors == expected_errors

    def test__iter__when_errors_defined_then_iterates_over_errors(self) -> None:
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        errors = Errors(errors=[error], field=FieldReference("username"))

        actual_errors = list(errors)

        expected_errors = [error]
        assert actual_errors == expected_errors

    def test__iter__when_no_errors_then_iterates_over_empty_list(self) -> None:
        errors = Errors(errors=[], field=FieldReference("username"))

        actual_errors = list(errors)

        expected_errors = []
        assert actual_errors == expected_errors

    def test__str__when_errors_defined_then_returns_string_representation(self) -> None:
        field = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        errors = Errors(errors=[error], field=field)

        actual_str = str(errors)

        expected_str = f"Errors for field '{field.value}':\n - An error occurred"
        assert actual_str == expected_str
