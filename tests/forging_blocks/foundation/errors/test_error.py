# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest

from forging_blocks.foundation import Error, ErrorMessage, ErrorMetadata


@pytest.mark.unit
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
