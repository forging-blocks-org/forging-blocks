# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.domain.permissions.composite_permission_checker import (
    CompositePermissionChecker,
)
from forging_blocks.domain.permissions.role_based_permission_checker import (
    RoleBasedPermissionChecker,
)
from forging_blocks.foundation.context import AuthorizationContext
from forging_blocks.foundation.permission import Permission


@pytest.mark.unit
@pytest.mark.asyncio
class TestCompositePermissionChecker:
    async def test_when_any_inner_grants_then_grants(self) -> None:
        checker = CompositePermissionChecker(
            [
                RoleBasedPermissionChecker({"admin": [Permission.READ]}),
                RoleBasedPermissionChecker({"user": []}),
            ]
        )
        context = AuthorizationContext(user_id="user-1", roles=["admin"])

        assert await checker.check(context, Permission.READ) is True

    async def test_when_all_deny_then_denies(self) -> None:
        checker = CompositePermissionChecker(
            [
                RoleBasedPermissionChecker({"user": [Permission.READ]}),
            ]
        )
        context = AuthorizationContext(user_id="user-1", roles=["guest"])

        assert await checker.check(context, Permission.READ) is False

    async def test_when_empty_checkers_then_denies(self) -> None:
        checker = CompositePermissionChecker([])
        context = AuthorizationContext(user_id="user-1")

        assert await checker.check(context, Permission.READ) is False
