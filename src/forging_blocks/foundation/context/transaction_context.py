"""Metadata for a single transactional boundary."""

import uuid
from collections.abc import Hashable
from datetime import datetime, timezone
from typing import Any

from forging_blocks.foundation.isolation_level import IsolationLevel
from forging_blocks.foundation.value_object import ValueObject


class TransactionContext(ValueObject[tuple[Hashable, ...]]):
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

    __slots__ = (
        "_transaction_id",
        "_started_at",
        "_isolation_level",
        "_metadata",
    )

    def __init__(
        self,
        *,
        transaction_id: uuid.UUID | None = None,
        started_at: datetime | None = None,
        isolation_level: IsolationLevel = IsolationLevel.READ_COMMITTED,
        metadata: tuple[tuple[str, Any], ...] | None = None,
    ) -> None:
        super().__init__()
        self._transaction_id = transaction_id if transaction_id is not None else uuid.uuid4()
        self._started_at = started_at if started_at is not None else datetime.now(timezone.utc)
        self._isolation_level = isolation_level
        self._metadata = metadata

    @property
    def transaction_id(self) -> uuid.UUID:
        """Unique identifier for the transaction."""
        return self._transaction_id

    @property
    def started_at(self) -> datetime:
        """UTC timestamp marking when the transaction began."""
        return self._started_at

    @property
    def isolation_level(self) -> IsolationLevel:
        """The isolation level requested for this transaction."""
        return self._isolation_level

    @property
    def metadata(self) -> tuple[tuple[str, Any], ...] | None:
        """Arbitrary key-value pairs for cross-cutting concerns."""
        return self._metadata

    @property
    def value(self) -> tuple[Hashable, ...]:
        """Composite value: all fields as a tuple."""
        return self._equality_components

    @property
    def _equality_components(self) -> tuple[Hashable, ...]:
        return (
            self._transaction_id,
            self._started_at,
            self._isolation_level,
            self._metadata,
        )
