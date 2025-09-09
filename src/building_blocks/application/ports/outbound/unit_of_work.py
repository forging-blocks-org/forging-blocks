"""
Unit of Work interface for managing transactions.

The Unit of Work pattern maintains a list of objects affected by a business
transaction and coordinates writing out changes and resolving concurrency problems.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any


class UnitOfWorkError(Exception):
    """
    Exception raised for errors in the unit of work.
    """

    pass


class UnitOfWork(ABC):
    """
    Unit of Work interface for managing transactions and consistency boundaries.

    The Unit of Work:
    - Manages the transaction/session/context for a business operation.
    - Coordinates the commit or rollback of changes across multiple repositories.
    - Publishes domain events after successful commit (infrastructure responsibility).
    - Should be agnostic to repository types; repositories should receive the
    session/context from the UoW.

    Concrete implementations typically provide a `session` or `context` property
    to be injected into repositories.
    """

    @property
    @abstractmethod
    def session(self) -> Any | None:
        """
        The current transaction/session/context for this unit of work.
        Concrete implementations should override this if a session/context is used.
        """
        pass

    async def __aenter__(self) -> UnitOfWork:
        """
        Enter the unit of work context.
        This typically initializes resources or a transaction context.
        """
        return self

    async def __aexit__(
        self,
        exc_type: type | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Exit the unit of work context.
        Commits if no exception occurred, otherwise rolls back.
        """
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        """
        Commit all changes in the unit of work.

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
        """
        Rollback all changes in the unit of work.

        Raises:
            UnitOfWorkError: If rollback fails
        """
        ...
