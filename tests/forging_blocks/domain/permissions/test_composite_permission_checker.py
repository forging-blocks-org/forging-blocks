import pytest

from forging_blocks.domain.permissions.composite_permission_checker import (
    CompositePermissionChecker,
)
from forging_blocks.foundation.permission import Permission


class _AlwaysGrant:
    async def check(self, context: object, permission: Permission) -> bool:
        del context, permission
        return True


class _AlwaysDeny:
    async def check(self, context: object, permission: Permission) -> bool:
        del context, permission
        return False


@pytest.mark.unit
class TestCompositePermissionChecker:
    async def test_when_any_inner_grants_then_grants(self) -> None:
        checker = CompositePermissionChecker([_AlwaysGrant(), _AlwaysDeny()])

        assert await checker.check(object(), Permission.READ) is True

    async def test_when_all_deny_then_denies(self) -> None:
        checker = CompositePermissionChecker([_AlwaysDeny()])

        assert await checker.check(object(), Permission.READ) is False

    async def test_when_empty_checkers_then_denies(self) -> None:
        checker = CompositePermissionChecker([])

        assert await checker.check(object(), Permission.READ) is False
