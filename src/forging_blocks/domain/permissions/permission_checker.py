"""Protocol for permission-checking implementations."""

from typing import Protocol, runtime_checkable

from forging_blocks.foundation.context import AuthorizationContext
from forging_blocks.foundation.permission import Permission


@runtime_checkable
class PermissionChecker(Protocol):
    """Protocol for any callable that decides whether a permission is granted."""

    async def check(self, context: AuthorizationContext, permission: Permission) -> bool:
        """Return ``True`` if *permission* is granted in *context*."""
        ...
