# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.application.errors.transaction_error import TransactionError
from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata


@pytest.mark.unit
class TestTransactionError:
    def test_when_created_with_message_then_extends_error(self) -> None:
        error = TransactionError(ErrorMessage("commit failed"))

        assert isinstance(error, TransactionError)
        assert str(error) == "TransactionError: commit failed"

    def test_when_created_with_message_and_metadata_then_stores_both(self) -> None:
        metadata = ErrorMetadata[dict[str, object]](context={"transaction_identifier": "abc"})
        error = TransactionError(ErrorMessage("rollback"), metadata)

        assert error.message.value == "rollback"
        assert error.metadata.context == {"transaction_identifier": "abc"}
