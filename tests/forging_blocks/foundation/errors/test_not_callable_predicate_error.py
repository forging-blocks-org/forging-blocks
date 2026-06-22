# pyright: reportPrivateUsage=false
# pyright: reportMissingTypeArgument=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingParameterType=false
# pyright: reportIncompatibleMethodOverride=false
# pyright: reportUnusedClass=false
import pytest

from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata
from forging_blocks.foundation.errors.not_callable_predicate_error import NotCallablePredicateError


@pytest.mark.unit
class TestNotCallablePredicateError:
    def test_initialization_with_integer_then_contains_type_name_in_message(self) -> None:
        """When initialized with an integer, the error message should contain 'int'."""
        # Arrange
        predicate = 42

        # Act
        error = NotCallablePredicateError(predicate)

        # Assert
        expected_message = ErrorMessage("predicate must be Callable and not int")
        assert error.message == expected_message

    def test_initialization_with_string_then_contains_type_name_in_message(self) -> None:
        """When initialized with a string, the error message should contain 'str'."""
        # Arrange
        predicate = "not_a_callable"

        # Act
        error = NotCallablePredicateError(predicate)

        # Assert
        expected_message = ErrorMessage("predicate must be Callable and not str")
        assert error.message == expected_message

    def test_initialization_with_list_then_contains_type_name_in_message(self) -> None:
        """When initialized with a list, the error message should contain 'list'."""
        # Arrange
        predicate = [1, 2, 3]

        # Act
        error = NotCallablePredicateError(predicate)

        # Assert
        expected_message = ErrorMessage("predicate must be Callable and not list")
        assert error.message == expected_message

    def test_initialization_with_dict_then_contains_type_name_in_message(self) -> None:
        """When initialized with a dict, the error message should contain 'dict'."""
        # Arrange
        predicate = {"key": "value"}

        # Act
        error = NotCallablePredicateError(predicate)

        # Assert
        expected_message = ErrorMessage("predicate must be Callable and not dict")
        assert error.message == expected_message

    def test_initialization_with_none_then_contains_type_name_in_message(self) -> None:
        """When initialized with None, the error message should contain 'NoneType'."""
        # Arrange
        predicate = None

        # Act
        error = NotCallablePredicateError(predicate)

        # Assert
        expected_message = ErrorMessage("predicate must be Callable and not NoneType")
        assert error.message == expected_message

    def test_metadata_when_no_metadata_provided_then_defaults_to_empty(self) -> None:
        """When no metadata is provided, it should default to empty ErrorMetadata."""
        # Arrange
        predicate = 123

        # Act
        error = NotCallablePredicateError(predicate)

        # Assert
        expected_metadata = ErrorMetadata[dict[str, object]]({})
        assert error.metadata == expected_metadata
        assert error.context == {}

    def test_str_when_called_then_returns_formatted_error_string(self) -> None:
        """The string representation should include the error class name and message."""
        # Arrange
        predicate = "invalid"
        error = NotCallablePredicateError(predicate)

        # Act
        result = str(error)

        # Assert
        assert "NotCallablePredicateError" in result
        assert "predicate must be Callable and not str" in result

    def test_repr_when_called_then_returns_detailed_representation(self) -> None:
        """The repr should include the class name, message, and context."""
        # Arrange
        predicate = 42
        error = NotCallablePredicateError(predicate)

        # Act
        result = repr(error)

        # Assert
        assert "NotCallablePredicateError" in result
        assert "message='predicate must be Callable and not int'" in result
        assert "context={}" in result

    def test_as_debug_string_when_called_then_returns_multiline_debug_format(self) -> None:
        """The debug string should return a detailed, multiline representation."""
        # Arrange
        predicate = True
        error = NotCallablePredicateError(predicate)

        # Act
        result = error.as_debug_string()

        # Assert
        assert "NotCallablePredicateError(" in result
        assert "message=ErrorMessage(value='predicate must be Callable and not bool')" in result
        assert "metadata=ErrorMetadata(context={})" in result

    def test_is_exception_subclass(self) -> None:
        """NotCallablePredicateError should be a subclass of Exception."""
        # Arrange & Act & Assert
        assert issubclass(NotCallablePredicateError, Exception)

    def test_can_be_raised_and_caught(self) -> None:
        """NotCallablePredicateError can be raised and caught like a standard exception."""
        # Arrange
        predicate = []

        # Act & Assert
        with pytest.raises(NotCallablePredicateError) as exc_info:
            raise NotCallablePredicateError(predicate)

        assert exc_info.value.message.value == "predicate must be Callable and not list"
