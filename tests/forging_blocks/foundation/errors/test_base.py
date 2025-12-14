import pytest

from forging_blocks.foundation import (
    CombinedErrors,
    Error,
    ErrorMessage,
    ErrorMetadata,
    FieldErrors,
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
    def test__init__when_no_errors_but_field_then_raise_value_error(self) -> None:
        field_reference = FieldReference("username")

        with pytest.raises(ValueError):
            FieldErrors(field=field_reference, errors=[])

    def test__init__when_errors_but_no_field_then_raise_value_error(self) -> None:
        error_message = ErrorMessage("An error occurred")

        with pytest.raises(ValueError):
            FieldErrors(field=None, errors=[error_message])  # type: ignore

    def test_errors_when_errors_defined_then_returns_errors(self) -> None:
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        field_errors = FieldErrors(errors=[error], field=FieldReference("username"))

        actual_errors = field_errors.errors

        expected_errors = (error,)
        assert actual_errors == expected_errors

    def test_errors_len_when_errors_defined_then_returns_length_of_errors(self) -> None:
        error_message1 = ErrorMessage("An error occurred1")
        error_message2 = ErrorMessage("An error occurred2")
        error1 = Error(error_message1)
        error2 = Error(error_message2)
        field_errors = FieldErrors(
            errors=[error1, error2], field=FieldReference("username")
        )

        actual_length = len(field_errors)

        expected_length = 2
        assert actual_length == expected_length

    def test__iter__when_errors_defined_then_iterates_over_errors(self) -> None:
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        field_errors = FieldErrors(errors=[error], field=FieldReference("username"))

        actual_errors = list(field_errors)

        expected_errors = [error]
        assert actual_errors == expected_errors

    def test__str__when_errors_defined_then_returns_string_representation(self) -> None:
        field_reference = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        field_errors = FieldErrors(errors=[error], field=field_reference)

        actual_str = str(field_errors)

        expected_str = f"FieldErrors for field '{field_reference.value}':\n - Error: An error occurred"
        assert actual_str == expected_str

    def test__repr__when_errors_defined_then_returns_repr_string(self) -> None:
        field_reference = FieldReference("username")
        error_message1 = ErrorMessage("An error occurred1")
        error_message2 = ErrorMessage("An error occurred2")
        error1 = Error(error_message1)
        error2 = Error(error_message2)
        field_errors = FieldErrors(errors=[error1, error2], field=field_reference)

        actual_repr = repr(field_errors)

        expected_repr = f"<FieldErrors field={field_reference.value!r} errors=2>"
        assert actual_repr == expected_repr

    def test_as_debug_string_when_errors_defined_then_returns_debug_string(
        self,
    ) -> None:
        field_reference = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        field_errors = FieldErrors(errors=[error], field=field_reference)

        actual_debug_string = field_errors.as_debug_string()

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

    def test_field_when_defined_then_return_it(self) -> None:
        field_reference = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        field_errors = FieldErrors(errors=[error], field=field_reference)

        actual_field = field_errors.field

        expected_field_reference = FieldReference("username")
        assert expected_field_reference == actual_field


class TestCombinedErrors:
    def test_errors_when_errors_defined_then_returns_errors(self) -> None:
        field_reference = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        field_errors = FieldErrors(errors=[error], field=field_reference)
        combined_errors = CombinedErrors(errors=[field_errors])

        actual_errors = combined_errors.errors

        expected_errors = (field_errors,)
        assert actual_errors == expected_errors

    def test__str__when_errors_defined_then_returns_string_representation(self) -> None:
        field_reference = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        field_errors = FieldErrors(errors=[error], field=field_reference)
        combined_errors = CombinedErrors(errors=[field_errors])

        actual_str = str(combined_errors)

        expected_str = (
            "CombinedErrors:\n- FieldErrors for field 'username':\n - Error: An error "
            "occurred"
        )
        assert actual_str == expected_str

    def test__repr__when_errors_defined_then_returns_repr_string(self) -> None:
        field_reference = FieldReference("username")
        error_message1 = ErrorMessage("An error occurred1")
        error_message2 = ErrorMessage("An error occurred2")
        error1 = Error(error_message1)
        error2 = Error(error_message2)
        field_errors1 = FieldErrors(errors=[error1, error2], field=field_reference)
        field_errors2 = FieldErrors(errors=[error1, error2], field=field_reference)
        combined_errors = CombinedErrors(errors=[field_errors1, field_errors2])

        actual_repr = repr(combined_errors)

        expected_repr = "<CombinedErrors errors=2>"
        assert actual_repr == expected_repr

    def test_as_debug_string_when_errors_defined_then_returns_debug_string(
        self,
    ) -> None:
        field_reference = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        field_errors = FieldErrors(errors=[error], field=field_reference)
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
        field_reference = FieldReference("username")
        error_message = ErrorMessage("An error occurred")
        error = Error(error_message)
        field_errors = FieldErrors(errors=[error], field=field_reference)
        combined_errors = CombinedErrors(errors=[field_errors])

        actual_errors = list(combined_errors)

        expected_errors = [field_errors]
        assert actual_errors == expected_errors
