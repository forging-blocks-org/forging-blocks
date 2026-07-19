# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.infrastructure.errors.repository_errors import (
    RepositoryError,
    RepositoryNotFoundError,
)


@pytest.mark.integration
class TestRepositoryError:
    def test_init_when_message_defined_then_stores_message(self) -> None:
        message = ErrorMessage("Save failed")
        error = RepositoryError(message)

        assert error.message == message
        assert "RepositoryError" in str(error)

    def test_is_instance_of_base_error(self) -> None:
        message = ErrorMessage("An error")
        error = RepositoryError(message)

        assert isinstance(error, Exception)

    def test_subclass_of_repository_not_found_error(self) -> None:
        error = RepositoryNotFoundError(ErrorMessage("Not found"))

        assert isinstance(error, RepositoryError)


@pytest.mark.integration
class TestRepositoryNotFoundError:
    def test_for_id_when_called_then_returns_error_with_descriptive_message(self) -> None:
        error = RepositoryNotFoundError.for_id("abc-123")

        assert "abc-123" in str(error)
        assert "not found" in str(error).lower()

    def test_for_id_when_called_with_int_id_then_returns_error_with_id_in_message(self) -> None:
        error = RepositoryNotFoundError.for_id(42)

        assert "42" in str(error)
        assert "not found" in str(error).lower()

    def test_for_id_when_called_then_returns_repository_not_found_error_instance(self) -> None:
        error = RepositoryNotFoundError.for_id("my-id")

        assert isinstance(error, RepositoryNotFoundError)
        assert isinstance(error, RepositoryError)
