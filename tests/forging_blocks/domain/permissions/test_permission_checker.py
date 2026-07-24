import pytest

from forging_blocks.domain.permissions.permission_checker import PermissionChecker
from forging_blocks.foundation.permission import Permission


@pytest.mark.unit
class TestPermissionCheckerProtocol:
    def test_when_implements_async_check_then_is_permission_checker(self) -> None:
        class CustomChecker:
            async def check(self, context: object, permission: Permission) -> bool:
                del context, permission
                return True

        assert isinstance(CustomChecker(), PermissionChecker)
