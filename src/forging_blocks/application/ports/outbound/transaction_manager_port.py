"""Outbound port for transactional boundaries."""

from collections.abc import Awaitable, Callable
from typing import Any, Protocol

from forging_blocks.foundation.context import TransactionContext
from forging_blocks.foundation.result import Result


class TransactionManagerPort[TransactionErrorType](Protocol):
    """Protocol for transaction management in the application layer."""

    async def begin(self, context: TransactionContext) -> Result[None, TransactionErrorType]:
        """Start a new transaction."""
        ...

    async def commit(self) -> Result[None, TransactionErrorType]:
        """Commit the current transaction."""
        ...

    async def rollback(self) -> Result[None, TransactionErrorType]:
        """Roll back the current transaction."""
        ...

    async def execute_in_transaction[ResponseType](
        self,
        fn: Callable[..., Awaitable[ResponseType]],
        context: TransactionContext,
        *args: Any,
        **kwargs: Any,
    ) -> Result[ResponseType, TransactionErrorType]:
        """Execute *fn* inside a begin/commit boundary."""
        ...
