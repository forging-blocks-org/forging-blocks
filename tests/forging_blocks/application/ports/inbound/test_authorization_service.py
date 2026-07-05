# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.application.ports.inbound.authorization_service import AuthorizationService
from forging_blocks.foundation.context import AuthorizationContext
from forging_blocks.foundation.permission import Permission


@pytest.mark.unit
@pytest.mark.asyncio
class TestAuthorizationService:
    async def test_when_check_permission_granted_then_returns_true(self) -> None:
        class PermissiveAuthorizationService(AuthorizationService):
            async def check_permission(
                self,
                context: AuthorizationContext,
                permission: Permission,
            ) -> bool:
                del context, permission
                return True

            async def check_resource_permission(
                self,
                context: AuthorizationContext,
                resource: str,
                action: str,
            ) -> bool:
                del context, resource, action
                return True

            async def get_user_permissions(self, user_id: str) -> list[Permission]:
                del user_id
                return [Permission.READ]

            async def get_user_roles(self, user_id: str) -> list[str]:
                del user_id
                return ["admin"]

        service = PermissiveAuthorizationService()
        context = AuthorizationContext(user_id="user-1")

        assert await service.check_permission(context, Permission.READ) is True

    async def test_when_check_permission_denied_then_returns_false(self) -> None:
        class RestrictiveAuthorizationService(AuthorizationService):
            async def check_permission(
                self,
                context: AuthorizationContext,
                permission: Permission,
            ) -> bool:
                del context, permission
                return False

            async def check_resource_permission(
                self,
                context: AuthorizationContext,
                resource: str,
                action: str,
            ) -> bool:
                del context, resource, action
                return False

            async def get_user_permissions(self, user_id: str) -> list[Permission]:
                del user_id
                return []

            async def get_user_roles(self, user_id: str) -> list[str]:
                del user_id
                return []

        service = RestrictiveAuthorizationService()

        assert (
            await service.check_permission(
                AuthorizationContext(user_id="user-1"),
                Permission.ADMIN,
            )
            is False
        )
