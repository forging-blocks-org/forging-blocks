"""In-memory write-only repository implementation.

Provides a concrete implementation of WriteOnlyRepository backed by a
dictionary for command-side operations in CQRS architectures.
"""

from __future__ import annotations

from typing import Any, Generic, MutableMapping, TypeVar, cast

from forging_blocks.application.ports.outbound.repository import WriteOnlyRepository
from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.identified import Identified
from forging_blocks.infrastructure.errors.repository_errors import (
    RepositoryError,
    RepositoryNotFoundError,
)

TWriteAggregateRoot = TypeVar("TWriteAggregateRoot", bound=Identified[Any])
TWriteId = TypeVar("TWriteId")


class InMemoryWriteRepository(
    Generic[TWriteAggregateRoot, TWriteId],
    WriteOnlyRepository[TWriteAggregateRoot, TWriteId],
):
    """In-memory implementation of WriteOnlyRepository for command operations.

    Stores aggregates in a dictionary keyed by their identifier. Designed
    for command-side usage in CQRS architectures.

    The storage mapping is injected via the constructor and copied on init
    to ensure independence from external mutation.
    """

    __slots__ = ("_storage",)

    def __init__(
        self,
        storage: MutableMapping[TWriteId, TWriteAggregateRoot] | None = None,
    ) -> None:
        """Initialize the write repository with optional external storage.

        Args:
            storage: An optional mutable mapping to use as backing storage.
                If None, a new empty dictionary is used.
        """
        self._storage: dict[TWriteId, TWriteAggregateRoot] = (
            dict(storage) if storage is not None else {}
        )

    async def delete_by_id(self, id: TWriteId) -> None:  # noqa: A002
        """Delete an aggregate by ID.

        Args:
            id: Unique identifier of the aggregate.

        Raises:
            RepositoryError: If the ID is None, an empty string,
                or the boolean False.
            RepositoryNotFoundError: If no aggregate exists with the given ID.
        """
        self._validate_id(id)
        if id not in self._storage:
            raise RepositoryNotFoundError.for_id(id)
        del self._storage[id]

    async def save(self, aggregate: TWriteAggregateRoot) -> None:
        """Persist an aggregate instance.

        Args:
            aggregate: The aggregate to save.

        Raises:
            RepositoryError: If the aggregate has no valid identifier
                (None, empty string, or boolean False).
        """
        aggregate_id: TWriteId = cast(TWriteId, aggregate.id)
        self._validate_id(aggregate_id)
        self._storage[aggregate_id] = aggregate

    @staticmethod
    def _validate_id(identifier: object) -> None:
        """Validate that an aggregate identifier is not None, empty, or False.

        Mirrors the validation performed by
        ``AggregateRoot._validate_identity`` so that the repository
        independently guards against invalid identifiers.

        Raises:
            RepositoryError: If *identifier* is ``None``, an empty string
                (``""``), or the boolean ``False``.
        """
        is_none = identifier is None
        is_empty_string = identifier == ""
        is_false = identifier is False

        if is_none or is_empty_string or is_false:
            raise RepositoryError(
                ErrorMessage("Cannot save aggregate without a valid identifier.")
            )
