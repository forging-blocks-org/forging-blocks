from abc import abstractmethod
from typing import Callable

from forging_blocks.application.ports.outbound.unit_of_work import UnitOfWork
from scripts.release.application.workflow import ReleaseStep


class ReleaseTransaction(UnitOfWork):
    """
    Coordinates commit / rollback of a release preparation.

    Guarantees:
    - rollback on any exception
    - reverse-order compensation
    """

    @abstractmethod
    def register_step(self, step: ReleaseStep) -> None: ...
