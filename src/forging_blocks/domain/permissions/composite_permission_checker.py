"""Composite permission checker with OR logic."""

from __future__ import annotations

from typing import TYPE_CHECKING

from forging_blocks.domain.permissions.permission_checker import PermissionChecker
from forging_blocks.foundation.permission import Permission

if TYPE_CHECKING:
    from forging_blocks.foundation.context import AuthorizationContext


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
