"""Immutable context carried through every application-service call."""

import uuid
from collections.abc import Hashable

from forging_blocks.foundation.value_object import ValueObject


class ServiceContext(ValueObject[tuple[Hashable, ...]]):
    """Immutable context carried through every application-service call.

    Args:
        correlation_id: A unique identifier that traces the entire
            request/response lifecycle.  Auto-generated when omitted.
        user_id: The identifier of the authenticated user, if any.
        permissions: The permissions held by the current user.
        metadata: Arbitrary key-value pairs for cross-cutting concerns
            (tracing, feature flags, tenant id, etc.).

    """

    __slots__ = (
        "_correlation_id",
        "_user_id",
        "_permissions",
        "_metadata",
    )

    def __init__(
        self,
        *,
        correlation_id: uuid.UUID | None = None,
        user_id: str | None = None,
        permissions: tuple[str, ...] | None = None,
        metadata: tuple[tuple[str, Hashable], ...] | None = None,
    ) -> None:
        super().__init__()
        self._correlation_id = correlation_id if correlation_id is not None else uuid.uuid4()
        self._user_id = user_id
        self._permissions = permissions if permissions is not None else ()
        self._metadata = metadata if metadata is not None else ()

    @property
    def correlation_id(self) -> uuid.UUID:
        """A unique identifier that traces the entire request/response lifecycle."""
        return self._correlation_id

    @property
    def user_id(self) -> str | None:
        """The identifier of the authenticated user, if any."""
        return self._user_id

    @property
    def permissions(self) -> tuple[str, ...]:
        """The permissions held by the current user."""
        return self._permissions

    @property
    def metadata(self) -> tuple[tuple[str, Hashable], ...]:
        """Arbitrary key-value pairs for cross-cutting concerns."""
        return self._metadata

    @property
    def value(self) -> tuple[Hashable, ...]:
        """Composite value: all fields as a tuple."""
        return self._equality_components

    @property
    def _equality_components(self) -> tuple[Hashable, ...]:
        return (
            self._correlation_id,
            self._user_id,
            self._permissions,
            self._metadata,
        )
