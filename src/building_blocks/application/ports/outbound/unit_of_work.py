"""Unit of Work interface for managing transactions.

The Unit of Work pattern maintains a list of objects affected by a business
transaction and coordinates writing out changes and resolving concurrency problems.
"""

from __future__ import annotations

import types
from abc import ABC, abstractmethod
from typing import Optional


class AsyncUnitOfWork(ABC):
    """Unit of Work interface for managing transactions.

    The Unit of Work pattern maintains a list of objects affected by a business
    transaction and coordinates writing out changes and resolving concurrency problems.

    This is particularly useful when multiple repositories need to participate
    in a single transaction to maintain consistency.
    """

    async def __aenter__(self) -> AsyncUnitOfWork:
        """Enter the unit of work context.

        This method should be called at the beginning of a unit of work.
        It can be used to initialize resources or set up the transaction context.
        """
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[BaseException],
        traceback: Optional[types.TracebackType],
    ) -> None:
        """Exit the unit of work context.

        This method should be called at the end of a unit of work.
        It can be used to clean up resources or handle exceptions.
        If an exception occurs, it can decide whether to commit or rollback.
        """
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        """Commit all changes in the unit of work.

        This should:
        - Persist all registered changes
        - Publish domain events
        - Handle transaction coordination

        Raises:
            UnitOfWorkException: If commit fails
        """

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback all changes in the unit of work.

        Raises:
            UnitOfWorkException: If rollback fails
        """


class SyncUnitOfWork(ABC):
    """Unit of Work interface for managing transactions.

    The Unit of Work pattern maintains a list of objects affected by a business
    transaction and coordinates writing out changes and resolving concurrency problems.

    This is particularly useful when multiple repositories need to participate
    in a single transaction to maintain consistency.
    """

    def __enter__(self) -> SyncUnitOfWork:
        """Enter the unit of work context.

        This method should be called at the beginning of a unit of work.
        It can be used to initialize resources or set up the transaction context.
        """
        return self

    def __aexit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[BaseException],
        traceback: Optional[types.TracebackType],
    ) -> None:
        """Exit the unit of work context.

        This method should be called at the end of a unit of work.
        It can be used to clean up resources or handle exceptions.
        If an exception occurs, it can decide whether to commit or rollback.
        """
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    @abstractmethod
    def commit(self) -> None:
        """Commit all changes in the unit of work.

        This should:
        - Persist all registered changes
        - Publish domain events
        - Handle transaction coordination

        Raises:
            UnitOfWorkException: If commit fails
        """

    @abstractmethod
    def rollback(self) -> None:
        """Rollback all changes in the unit of work.

        Raises:
            UnitOfWorkException: If rollback fails
        """
