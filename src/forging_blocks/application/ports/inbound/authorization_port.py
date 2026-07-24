"""Inbound port for authorization and permission checking.

Responsibilities:
    - Check whether a user has a specific permission.
    - Evaluate resource-level access control.
    - Retrieve effective permissions and roles for a user.

Non-Responsibilities:
    - Authenticate users (handled externally).
    - Enforce business rules (handled by validation or domain).
"""

from abc import abstractmethod

from forging_blocks.foundation.permission import Permission
from forging_blocks.foundation.ports import InboundPort


class AuthorizationPort[AuthorizationCheckContext](InboundPort):
    """Inbound port for authorization decisions.

    Type Args:
        AuthorizationCheckContext: The application-defined context for authorization checks.

    Responsibilities:
        - Evaluate permissions against an authorization context.
        - Support resource-level and global permission checks.
        - Expose user roles and effective permissions.

    Non-Responsibilities:
        - Manage user identities or credentials.
        - Define permission hierarchies (delegated to domain or configuration).
    """

    @abstractmethod
    async def check_permission(
        self,
        context: AuthorizationCheckContext,
        permission: Permission,
    ) -> bool:
        """Evaluate whether *permission* is granted in *context*."""
        ...

    @abstractmethod
    async def check_resource_permission(
        self,
        context: AuthorizationCheckContext,
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
