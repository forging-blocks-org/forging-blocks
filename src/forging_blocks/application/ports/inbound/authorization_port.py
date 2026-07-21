"""Inbound port for authorization and permission checking."""

from abc import ABC, abstractmethod

from forging_blocks.foundation.context import AuthorizationContext
from forging_blocks.foundation.permission import Permission
from forging_blocks.foundation.ports import InboundPort


class AuthorizationPort(InboundPort[AuthorizationContext, bool], ABC):
    """Inbound port that authorizes user actions."""

    @abstractmethod
    async def check_permission(
        self,
        context: AuthorizationContext,
        permission: Permission,
    ) -> bool:
        """Evaluate whether *permission* is granted in *context*."""
        ...

    @abstractmethod
    async def check_resource_permission(
        self,
        context: AuthorizationContext,
        resource: str,
        action: str,
    ) -> bool:
        """Evaluate whether *action* on *resource* is permitted in *context*."""
        ...

    @abstractmethod
    async def get_user_permissions(self, user_id: str) -> list[Permission]:
        """Return the effective permissions for *user_id*."""
        ...

    @abstractmethod
    async def get_user_roles(self, user_id: str) -> list[str]:
        """Return the roles assigned to *user_id*."""
        ...
