"""Role-based permission checker implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from forging_blocks.foundation.permission import Permission

if TYPE_CHECKING:
    from forging_blocks.foundation.context import AuthorizationContext


class RoleBasedPermissionChecker:
    """Grants permissions based on a static role-to-permission mapping.

    Args:
        role_permissions: A dictionary mapping role names (``str``) to the list
            of `Permission` values that role is allowed.

    """

    __match_args__ = ("_role_permissions",)

    def __init__(self, role_permissions: dict[str, list[Permission]]) -> None:
        self._role_permissions = role_permissions

    async def check(self, context: AuthorizationContext, permission: Permission) -> bool:
        if not context.roles:
            return False
        for role in context.roles:
            allowed = self._role_permissions.get(role)
            if allowed is not None and permission in allowed:
                return True
        return False
