"""Unit of Work abstraction for transactional consistency.

A UnitOfWorkPort defines a transactional boundary for application operations.
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

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from forging_blocks.foundation.ports import OutboundPort


class UnitOfWorkPort(OutboundPort[object, None], ABC):
    """Protocol for managing transactional consistency.

    A UnitOfWorkPort coordinates operations across multiple repositories and
    outbound ports. It ensures that state changes and domain events are
    published atomically.  Subclasses provide the concrete context-manager
    behaviour (``__aenter__`` / ``__aexit__``).
    """

    @abstractmethod
    async def __aenter__(self) -> Self:
        """Enter the Unit of Work context.

        Returns:
            The active UnitOfWorkPort instance.
        """
        ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
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
