"""Outbound port for transactional boundaries.

Defines the ``TransactionManagerPort`` contract for explicit transaction
control (begin, commit, rollback) and transactional function execution.

Responsibilities:
    - Begin, commit, and roll back transactions.
    - Execute arbitrary functions within transactional boundaries.

Non-Responsibilities:
    - Implement business logic.
    - Manage connection pooling or resource cleanup.
"""

from abc import abstractmethod
from collections.abc import Awaitable, Callable

from forging_blocks.foundation.ports import OutboundPort
from forging_blocks.foundation.result import Result


class TransactionManagerPort[TransactionSessionContext, TransactionErrorType](OutboundPort):
    """Outbound port for explicit transaction management.

    Type Args:
        TransactionSessionContext: The application-defined session context for transactions.
        TransactionErrorType: The error type for transactional failures.

    Responsibilities:
        - Begin, commit, and roll back transactions.
        - Execute arbitrary functions within transactional boundaries.

    Non-Responsibilities:
        - Implement business logic.
        - Manage connection pooling or resource cleanup.
    """

    @abstractmethod
    async def begin(self, context: TransactionSessionContext) -> Result[None, TransactionErrorType]:
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
        context: TransactionSessionContext,
        *args: object,
        **kwargs: object,
    ) -> Result[ResponseType, TransactionErrorType]:
        """Execute *fn* inside a begin/commit boundary."""
        ...
