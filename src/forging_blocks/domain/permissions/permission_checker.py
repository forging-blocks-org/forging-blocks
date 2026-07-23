"""Protocol for permission-checking implementations."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from forging_blocks.foundation.permission import Permission


@runtime_checkable
class PermissionChecker[PermissionCheckContext](Protocol):
    """Protocol for any callable that decides whether a permission is granted.

    Type Args:
        PermissionCheckContext: The application-defined context for permission checks.
    """

    async def check(self, context: PermissionCheckContext, permission: Permission) -> bool:
        """Return ``True`` if *permission* is granted in *context*."""
        ...
