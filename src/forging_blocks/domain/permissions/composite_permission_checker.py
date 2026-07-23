"""Composite permission checker with OR logic."""

from forging_blocks.domain.permissions.permission_checker import PermissionChecker
from forging_blocks.foundation.context import AuthorizationContext
from forging_blocks.foundation.permission import Permission


class CompositePermissionChecker:
    """Combines multiple `PermissionChecker` instances with OR logic."""

    __match_args__ = ("_checkers",)

    def __init__(self, checkers: list[PermissionChecker]) -> None:
        self._checkers = checkers

    async def check(self, context: AuthorizationContext, permission: Permission) -> bool:
        for checker in self._checkers:
            if await checker.check(context, permission):
                return True
        return False
