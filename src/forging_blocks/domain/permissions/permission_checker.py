"""Protocol for permission-checking implementations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from forging_blocks.foundation.permission import Permission

if TYPE_CHECKING:
    from forging_blocks.foundation.context import AuthorizationContext


@runtime_checkable
class PermissionChecker(Protocol):
    """Protocol for any callable that decides whether a permission is granted."""

    async def check(self, context: AuthorizationContext, permission: Permission) -> bool:
        """Return ``True`` if *permission* is granted in *context*."""
        ...
