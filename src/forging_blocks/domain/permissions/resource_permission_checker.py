"""Resource-based permission checker implementation."""

from forging_blocks.foundation.context import AuthorizationContext
from forging_blocks.foundation.permission import Permission


class ResourcePermissionChecker:
    """Grants permissions based on a resource-type-to-permission mapping.

    Args:
        resource_permissions: A dictionary mapping resource-type names
            (``str``) to the list of :class:`Permission` values allowed
            for that resource type.
    """

    __match_args__ = ("_resource_permissions",)

    def __init__(self, resource_permissions: dict[str, list[Permission]]) -> None:
        self._resource_permissions = resource_permissions

    async def check(self, context: AuthorizationContext, permission: Permission) -> bool:
        if not context.resource_type:
            return False
        allowed = self._resource_permissions.get(context.resource_type)
        if allowed is None:
            return False
        return permission in allowed
