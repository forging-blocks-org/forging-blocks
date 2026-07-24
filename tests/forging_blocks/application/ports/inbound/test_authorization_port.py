import pytest

from forging_blocks.application.ports.inbound.authorization_port import AuthorizationPort
from forging_blocks.foundation.permission import Permission


@pytest.mark.unit
class TestAuthorizationPort:
    async def test_when_check_permission_granted_then_returns_true(self) -> None:
        class PermissiveAuthorizationPort(AuthorizationPort[object]):
            async def check_permission(
                self,
                context: object,
                permission: Permission,
            ) -> bool:
                del context, permission
                return True

            async def check_resource_permission(
                self,
                context: object,
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

        service = PermissiveAuthorizationPort()

        assert await service.check_permission(object(), Permission.READ) is True

    async def test_when_check_permission_denied_then_returns_false(self) -> None:
        class RestrictiveAuthorizationPort(AuthorizationPort[object]):
            async def check_permission(
                self,
                context: object,
                permission: Permission,
            ) -> bool:
                del context, permission
                return False

            async def check_resource_permission(
                self,
                context: object,
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

        service = RestrictiveAuthorizationPort()

        assert (
            await service.check_permission(
                object(),
                Permission.ADMIN,
            )
            is False
        )
