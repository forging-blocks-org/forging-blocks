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

from abc import abstractmethod
from types import TracebackType
from typing import Self

from forging_blocks.foundation.ports import OutboundPort


class UnitOfWorkPort(OutboundPort):
    """Contract for a transactional boundary.

    A UnitOfWorkPort coordinates repository operations and event publication.
    Implementations define the persistence and publication guarantees they can
    provide. Subclasses provide the concrete context-manager behaviour
    (``__aenter__`` / ``__aexit__``).

    Example:
        ```python
        async with MyUnitOfWork() as uow:
            repo = uow.accounts
            account = await repo.get_by_id("42")
            account.deposit(100.0)
            await uow.commit()
        ```
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

    @abstractmethod
    async def commit(self) -> None:
        """Commit the changes coordinated by the Unit of Work.

        Implementations must publish queued events and establish a terminal
        committed or rolled-back state. If publication fails, queued events
        must be discarded and modified-aggregate tracking cleared before the
        failure is raised. Events already published cannot be undone by this
        contract.

        Raises:
            UnitOfWorkError: If commit fails.

        """

    @abstractmethod
    async def rollback(self) -> None:
        """Roll back the transaction and discard uncommitted changes."""
