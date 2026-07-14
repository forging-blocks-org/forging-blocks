# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import uuid

import pytest

from forging_blocks.foundation.context import ServiceContext


@pytest.mark.unit
class TestServiceContext:
    def test_when_created_without_arguments_then_auto_generates_correlation_identifier(
        self,
    ) -> None:
        context = ServiceContext()

        assert isinstance(context.correlation_id, uuid.UUID)
        assert context.user_id is None
        assert context.permissions == ()
        assert context.metadata == ()

    def test_when_created_with_arguments_then_stores_values(self) -> None:
        context = ServiceContext(
            correlation_id=uuid.UUID("12345678-1234-5678-1234-567812345678"),
            user_id="user-1",
            permissions=("read", "write"),
            metadata=(("tenant", "acme"),),
        )

        assert context.correlation_id == uuid.UUID("12345678-1234-5678-1234-567812345678")
        assert context.user_id == "user-1"
        assert context.permissions == ("read", "write")
        assert context.metadata == (("tenant", "acme"),)

    def test_when_two_default_contexts_then_have_different_identifiers(self) -> None:
        first = ServiceContext()
        second = ServiceContext()

        assert first.correlation_id != second.correlation_id
