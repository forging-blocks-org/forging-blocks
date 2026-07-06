# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.domain.permissions.role_based_permission_checker import (
    RoleBasedPermissionChecker,
)
from forging_blocks.foundation.context import AuthorizationContext
from forging_blocks.foundation.permission import Permission


@pytest.mark.unit
@pytest.mark.asyncio
class TestRoleBasedPermissionChecker:
    async def test_when_role_has_permission_then_grants(self) -> None:
        checker = RoleBasedPermissionChecker({"admin": [Permission.READ, Permission.WRITE]})
        context = AuthorizationContext(user_id="user-1", roles=["admin"])

        assert await checker.check(context, Permission.READ) is True

    async def test_when_role_lacks_permission_then_denies(self) -> None:
        checker = RoleBasedPermissionChecker({"user": [Permission.READ]})
        context = AuthorizationContext(user_id="user-1", roles=["user"])

        assert await checker.check(context, Permission.DELETE) is False

    async def test_when_no_roles_then_denies(self) -> None:
        checker = RoleBasedPermissionChecker({"admin": [Permission.READ]})
        context = AuthorizationContext(user_id="user-1")

        assert await checker.check(context, Permission.READ) is False
