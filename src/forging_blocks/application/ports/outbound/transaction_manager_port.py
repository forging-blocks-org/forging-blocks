"""Outbound port for transactional boundaries."""

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any

from forging_blocks.foundation.context import TransactionContext
from forging_blocks.foundation.result import Result


class TransactionManagerPort[TransactionErrorType](ABC):
    """Abstract transaction manager for the application layer."""

    @abstractmethod
    async def begin(self, context: TransactionContext) -> Result[None, TransactionErrorType]:
        """Start a new transaction."""
        ...

    @abstractmethod
    async def commit(self) -> Result[None, TransactionErrorType]:
        """Commit the current transaction."""
        ...

    @abstractmethod
    async def rollback(self) -> Result[None, TransactionErrorType]:
        """Roll back the current transaction."""
        ...

    @abstractmethod
    async def execute_in_transaction[ResponseType](
        self,
        fn: Callable[..., Awaitable[ResponseType]],
        context: TransactionContext,
        *args: Any,
        **kwargs: Any,
    ) -> Result[ResponseType, TransactionErrorType]:
        """Execute *fn* inside a begin/commit boundary."""
        ...
