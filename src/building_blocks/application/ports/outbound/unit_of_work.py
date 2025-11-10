"""Unit of Work interface for managing transactions and consistency boundaries."""

from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any

from building_blocks.foundation.errors.base import Error


class UnitOfWorkError(Error):
    """Exception raised for errors in the unit of work."""

    pass


class UnitOfWork(ABC):
    """Abstract base class for a Unit of Work pattern.

    The Unit of Work pattern is used to maintain a list of objects affected by a  business
    transaction and to coordinate the writing out of changes and the resolution of concurrency
    problems.
    """

    async def __aenter__(self) -> UnitOfWork:
        """Enter the unit of work context."""
        return self

    async def __aexit__(
        self,
        exc_type: type | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the unit of work context. Commit or rollback based on exceptions."""
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    @property
    @abstractmethod
    def session(self) -> Any | None:
        """Get the underlying session or transaction context.

        Returns:
            The session or transaction context, or None if not applicable.
        """
        ...

    @abstractmethod
    async def commit(self) -> None:
        """Commit all changes in the unit of work.

        This should:
        - Persist all registered changes across repositories
        - Publish domain events after a successful commit
        - Handle transaction coordination

        Raises:
            UnitOfWorkError: If commit fails
        """
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback changes in transaction."""
        ...
