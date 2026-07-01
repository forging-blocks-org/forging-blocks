from abc import abstractmethod
from types import TracebackType
from typing import Self

from forging_blocks.application.ports.outbound.unit_of_work import UnitOfWorkPort
from scripts.release.application.workflow import ReleaseStep


class ReleaseTransaction(UnitOfWorkPort):
    """Coordinates commit / rollback of a release preparation.

    Guarantees:
    - rollback on any exception
    - reverse-order compensation
    """

    async def __aenter__(self) -> Self:
        """Enter the transaction context."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the transaction context.

        Commits if no exception occurred; otherwise rolls back.
        """
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    @abstractmethod
    def register_step(self, step: ReleaseStep) -> None: ...
