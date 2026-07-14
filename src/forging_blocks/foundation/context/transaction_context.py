"""Metadata for a single transactional boundary."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from forging_blocks.foundation.autofreeze import auto_freeze
from forging_blocks.foundation.autohash import auto_hash
from forging_blocks.foundation.isolation_level import IsolationLevel


@auto_freeze
@auto_hash
@dataclass
class TransactionContext:
    """Metadata for a single transactional boundary.

    Args:
        transaction_id: Unique identifier for the transaction.
            Auto-generated when omitted.
        started_at: UTC timestamp marking when the transaction began.
            Defaults to the current time.
        isolation_level: The isolation level requested for this
            transaction.  Defaults to ``READ_COMMITTED``.
        metadata: Arbitrary key-value pairs for cross-cutting concerns.
    """

    transaction_id: uuid.UUID = field(default_factory=uuid.uuid4)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    isolation_level: IsolationLevel = IsolationLevel.READ_COMMITTED
    metadata: dict[str, Any] | None = None
