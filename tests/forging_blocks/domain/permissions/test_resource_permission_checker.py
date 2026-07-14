# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.domain.permissions.resource_permission_checker import ResourcePermissionChecker
from forging_blocks.foundation.context import AuthorizationContext
from forging_blocks.foundation.permission import Permission


@pytest.mark.unit
class TestResourcePermissionChecker:
    async def test_when_resource_type_allows_permission_then_grants(self) -> None:
        checker = ResourcePermissionChecker({"document": [Permission.READ, Permission.WRITE]})
        context = AuthorizationContext(user_id="user-1", resource_type="document")

        assert await checker.check(context, Permission.READ) is True

    async def test_when_resource_type_lacks_permission_then_denies(self) -> None:
        checker = ResourcePermissionChecker({"image": [Permission.READ]})
        context = AuthorizationContext(user_id="user-1", resource_type="image")

        assert await checker.check(context, Permission.DELETE) is False

    async def test_when_resource_type_missing_then_denies(self) -> None:
        checker = ResourcePermissionChecker({"document": [Permission.READ]})
        context = AuthorizationContext(user_id="user-1")

        assert await checker.check(context, Permission.READ) is False

    async def test_when_resource_type_unknown_then_denies(self) -> None:
        checker = ResourcePermissionChecker({"document": [Permission.READ]})
        context = AuthorizationContext(user_id="user-1", resource_type="unknown_type")

        assert await checker.check(context, Permission.READ) is False
