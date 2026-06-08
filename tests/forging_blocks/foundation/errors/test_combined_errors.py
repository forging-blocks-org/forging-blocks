# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest

from forging_blocks.foundation import CombinedErrors, Error, ErrorMessage, FieldErrors, FieldReference


@pytest.mark.unit
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
            "CombinedErrors:\n- FieldErrors for field 'username':\n - Error: An error occurred"
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
