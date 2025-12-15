"""Unit of Work abstraction for transactional consistency.

A UnitOfWork defines a transactional boundary for application operations.
It coordinates the persistence of aggregate changes and the publication of
domain events, ensuring atomicity across these actions.

Responsibilities:
    - Manage a transactional context.
    - Commit or roll back changes.
    - Publish domain events upon successful commit.

Non-Responsibilities:
    - Execute business logic.
    - Interact directly with aggregates.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any

from forging_blocks.foundation.errors.base import Error


class UnitOfWorkError(Error):
    """Error raised when a Unit of Work operation fails."""

    pass


class UnitOfWork(ABC):
    """Abstract base class for managing transactional consistency.

    A UnitOfWork coordinates operations across multiple repositories and
    outbound ports. It ensures that state changes and domain events are
    published atomically.
    """

    async def __aenter__(self) -> UnitOfWork:
        """Enter the Unit of Work context.

        Returns:
            The active UnitOfWork instance.
        """
        return self

    async def __aexit__(
        self,
        exc_type: type | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the Unit of Work context.

        Commits if no exception occurred; otherwise rolls back.

        Args:
            exc_type: Raised exception type if any.
            exc_value: Exception instance.
            traceback: Execution traceback.
        """
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    @property
    @abstractmethod
    def session(self) -> Any | None:
        """Return the underlying session or transactional context.

        Returns:
            A context object representing the transaction, or None.

        Notes:
            This is infrastructure-defined (DB session, connection, etc.).
        """
        ...

    @abstractmethod
    async def commit(self) -> None:
        """Commit all changes in the Unit of Work.

        This operation should:
            - Persist all modified aggregates.
            - Publish domain events collected during the transaction.
            - Ensure atomicity.

        Raises:
            UnitOfWorkError: If commit fails.
        """
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """Roll back the transaction and discard uncommitted changes."""
        ...
