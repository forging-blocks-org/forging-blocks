# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import uuid

import pytest

from forging_blocks.foundation import IsolationLevel
from forging_blocks.foundation.context import TransactionContext


@pytest.mark.unit
class TestTransactionContext:
    def test_when_created_without_arguments_then_auto_generates_identifier(self) -> None:
        context = TransactionContext()

        assert isinstance(context.transaction_id, uuid.UUID)
        assert context.isolation_level == IsolationLevel.READ_COMMITTED
        assert context.metadata is None

    def test_when_two_contexts_then_different_identifiers(self) -> None:
        first = TransactionContext()
        second = TransactionContext()

        assert first.transaction_id != second.transaction_id

    def test_when_custom_isolation_then_stores_it(self) -> None:
        context = TransactionContext(isolation_level=IsolationLevel.SERIALIZABLE)

        assert context.isolation_level == IsolationLevel.SERIALIZABLE

    def test_when_metadata_provided_then_stores_it(self) -> None:
        context = TransactionContext(metadata={"trace": "abc-123"})

        assert context.metadata == {"trace": "abc-123"}
