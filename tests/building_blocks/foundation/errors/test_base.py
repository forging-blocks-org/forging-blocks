from building_blocks.foundation.errors.base import CombinedErrors, Error, FieldErrors
from building_blocks.foundation.errors.core import (
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

    def test_context_when_context_defined_then_returns_context_as_dict(self) -> None:
        message = ErrorMessage("An error occurred")
        error = Error(message, ErrorMetadata({"key": "value"}))

        actual_context = error.context

        expected_context = {"key": "value"}
        assert actual_context == expected_context

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

        error = Error(error_message)

        expected = "Error: An error occurred"
        assert str(error) == expected

    def test__str__when_message_is_empty_string_then_returns_empty_string(self) -> None:
        error_message = ErrorMessage("")

        error = Error(error_message)

        expected = "Error: "
        assert str(error) == expected

    def test__format_context_when_called_then_return_context_as_string(self) -> None:
        message = "An error occurred"
        error_message = ErrorMessage(message)
        context = {"key": "value"}
        error = Error(error_message, ErrorMetadata(context))

        formatted_context = error._format_context()

        expected_context = " | Context: {'key': 'value'}"
        assert formatted_context == expected_context

    def test__repr__when_message_defined_then_returns_repr_string(self) -> None:
        message = "An error occurred"
        error_message = ErrorMessage(message)
        error = Error(error_message)

        expected_repr = "<Error message='An error occurred' context={}>"
        assert repr(error) == expected_repr

    def test_debug_string_(self) -> None:
        message = "An error occurred"
        error_message = ErrorMessage(message)
        error = Error(error_message)

        debug_string = error.as_debug_string()

        expected_debug_string = (
            "Error(\n"
            "  message=ErrorMessage(value='An error occurred'),\n"
            "  metadata=ErrorMetadata(context={})\n"
            ")"
        )
        assert debug_string == expected_debug_string


class TestFieldErrors:
    def test_field_when_field_defined_then_returns_field_name(self) -> None:
        field = FieldReference("username")
        errors = FieldErrors(field=field, errors=[])

        actual_field = errors.field

        expected_field = FieldReference("username")
        assert actual_field == expected_field

    def test_errors_when_errors_defined_then_returns_errors(self) -> None:
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        errors = FieldErrors(errors=[error], field=FieldReference("username"))

        actual_errors = errors.errors

        expected_errors = (error,)
        assert actual_errors == expected_errors

    def test_errors_len_when_errors_defined_then_returns_length_of_errors(self) -> None:
        error_message1 = ErrorMessage("An error occurred1")
        error_message2 = ErrorMessage("An error occurred2")
        error1 = Error(error_message1)
        error2 = Error(error_message2)
        errors = FieldErrors(errors=[error1, error2], field=FieldReference("username"))

        actual_length = len(errors)

        expected_length = 2
        assert actual_length == expected_length

    def test__iter__when_errors_defined_then_iterates_over_errors(self) -> None:
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        errors = FieldErrors(errors=[error], field=FieldReference("username"))

        actual_errors = list(errors)

        expected_errors = [error]
        assert actual_errors == expected_errors

    def test__iter__when_no_errors_then_iterates_over_empty_list(self) -> None:
        errors = FieldErrors(errors=[], field=FieldReference("username"))

        actual_errors = list(errors)

        expected_errors = []
        assert actual_errors == expected_errors

    def test__str__when_errors_defined_then_returns_string_representation(self) -> None:
        field = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        errors = FieldErrors(errors=[error], field=field)

        actual_str = str(errors)

        expected_str = f"FieldErrors for field '{field.value}':\n - Error: An error occurred"
        assert actual_str == expected_str

    def test__repr__when_errors_defined_then_returns_repr_string(self) -> None:
        field = FieldReference("username")
        error_message1 = ErrorMessage("An error occurred1")
        error_message2 = ErrorMessage("An error occurred2")
        error1 = Error(error_message1)
        error2 = Error(error_message2)
        errors = FieldErrors(errors=[error1, error2], field=field)

        actual_repr = repr(errors)

        expected_repr = f"<FieldErrors field={field.value!r} errors=2>"
        assert actual_repr == expected_repr

    def test_as_debug_string_when_errors_defined_then_returns_debug_string(
        self,
    ) -> None:
        field = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        errors = FieldErrors(errors=[error], field=field)

        actual_debug_string = errors.as_debug_string()

        expected_debug_string = (
            "FieldErrors(\n"
            "  field=FieldReference(value='username'),\n"
            "  errors=[\n"
            "    Error(\n"
            "  message=ErrorMessage(value='An error occurred'),\n"
            "  metadata=ErrorMetadata(context={})\n"
            ")\n"
            "  ]\n"
            ")"
        )
        assert actual_debug_string == expected_debug_string


class TestCombinedErrors:
    def test_errors_when_errors_defined_then_returns_errors(self) -> None:
        field = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        field_errors = FieldErrors(errors=[error], field=field)
        combined_errors = CombinedErrors(errors=[field_errors])

        actual_errors = combined_errors.errors

        expected_errors = (field_errors,)
        assert actual_errors == expected_errors

    def test__str__when_errors_defined_then_returns_string_representation(self) -> None:
        field = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        field_errors = FieldErrors(errors=[error], field=field)
        combined_errors = CombinedErrors(errors=[field_errors])

        actual_str = str(combined_errors)

        expected_str = (
            "CombinedErrors:\n- FieldErrors for field 'username':\n - Error: An error " "occurred"
        )
        assert actual_str == expected_str

    def test__repr__when_errors_defined_then_returns_repr_string(self) -> None:
        field = FieldReference("username")
        error_message1 = ErrorMessage("An error occurred1")
        error_message2 = ErrorMessage("An error occurred2")
        error1 = Error(error_message1)
        error2 = Error(error_message2)
        field_errors1 = FieldErrors(errors=[error1, error2], field=field)
        field_errors2 = FieldErrors(errors=[error1, error2], field=field)
        combined_errors = CombinedErrors(errors=[field_errors1, field_errors2])

        actual_repr = repr(combined_errors)

        expected_repr = "<CombinedErrors errors=2>"
        assert actual_repr == expected_repr

    def test_as_debug_string_when_errors_defined_then_returns_debug_string(
        self,
    ) -> None:
        field = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        field_errors = FieldErrors(errors=[error], field=field)
        combined_errors = CombinedErrors(errors=[field_errors])

        actual_debug_string = combined_errors.as_debug_string()

        expected_debug_string = (
            "CombinedErrors(\n"
            "  errors=[\n"
            "    FieldErrors(\n"
            "      field=FieldReference(value='username'),\n"
            "      errors=[\n"
            "        Error(\n"
            "      message=ErrorMessage(value='An error occurred'),\n"
            "      metadata=ErrorMetadata(context={})\n"
            "    )\n"
            "      ]\n"
            "    )\n"
            "  ]\n"
            ")"
        )
        assert actual_debug_string == expected_debug_string

    def test__iter__when_errors_defined_then_iterates_over_errors(self) -> None:
        field = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        field_errors = FieldErrors(errors=[error], field=field)
        combined_errors = CombinedErrors(errors=[field_errors])

        actual_errors = list(combined_errors)

        expected_errors = [field_errors]
        assert actual_errors == expected_errors

    def test__iter__when_no_errors_then_iterates_over_empty_list(self) -> None:
        errors = FieldErrors(errors=[], field=FieldReference("username"))

        actual_errors = list(errors)

        expected_errors = []
        assert actual_errors == expected_errors
