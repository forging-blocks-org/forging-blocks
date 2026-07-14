"""Immutable context carried through every application-service call."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from forging_blocks.foundation.autofreeze import auto_freeze
from forging_blocks.foundation.autohash import auto_hash


@auto_freeze
@auto_hash
@dataclass
class ServiceContext:
    """Immutable context carried through every application-service call.

    Args:
        correlation_id: A unique identifier that traces the entire
            request/response lifecycle.  Auto-generated when omitted.
        user_id: The identifier of the authenticated user, if any.
        permissions: The permissions held by the current user.
        metadata: Arbitrary key-value pairs for cross-cutting concerns
            (tracing, feature flags, tenant id, etc.).
    """

    correlation_id: uuid.UUID = field(default_factory=uuid.uuid4)
    user_id: str | None = None
    permissions: list[str] = field(default_factory=list[str])
    metadata: dict[str, Any] = field(default_factory=dict[str, Any])
