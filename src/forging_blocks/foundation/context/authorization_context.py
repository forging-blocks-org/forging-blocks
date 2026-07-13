"""Authorization context bundled for a single authorization decision."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from forging_blocks.foundation.autofreeze import auto_freeze


@auto_freeze
@dataclass
class AuthorizationContext:
    """Bundles the information needed for a single authorization decision.

    Args:
        user_id: The unique identifier of the user requesting access.
        roles: Roles assigned to the user (e.g. ``["admin", "editor"]``).
        resource_id: Optional identifier of the resource being accessed.
        resource_type: Optional discriminator for the resource kind
            (e.g. ``"document"``, ``"project"``).
        action: Optional name of the action being performed
            (e.g. ``"publish"``, ``"archive"``).
        metadata: Arbitrary key-value pairs that checkers may inspect.
    """

    user_id: str
    roles: list[str] | None = None
    resource_id: str | None = None
    resource_type: str | None = None
    action: str | None = None
    metadata: dict[str, Any] | None = None
