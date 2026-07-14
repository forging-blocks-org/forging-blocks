# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.foundation.context import AuthorizationContext


@pytest.mark.unit
class TestAuthorizationContext:
    def test_when_created_with_user_identifier_then_stores_it(self) -> None:
        context = AuthorizationContext(user_id="user-1")

        assert context.user_id == "user-1"
        assert context.roles is None

    def test_when_created_with_full_arguments_then_stores_all(self) -> None:
        context = AuthorizationContext(
            user_id="user-1",
            roles=("admin", "editor"),
            resource_id="document-42",
            resource_type="document",
            action="publish",
            metadata=(("ip_address", "127.0.0.1"),),
        )

        assert context.user_id == "user-1"
        assert context.roles == ("admin", "editor")
        assert context.resource_id == "document-42"
        assert context.resource_type == "document"
        assert context.action == "publish"
        assert context.metadata == (("ip_address", "127.0.0.1"),)
