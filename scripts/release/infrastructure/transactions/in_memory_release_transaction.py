from typing import Any, Callable
import logging

from scripts.release.application.ports.outbound import ReleaseTransaction
from scripts.release.application.workflow import ReleaseStep


class InMemoryReleaseTransaction(ReleaseTransaction):
    def __init__(self) -> None:
        self._undo_stack: list[Callable[[], None]] = []
        self._logger = logging.getLogger(__name__)

    @property
    def session(self) -> Any | None:
        pass

    def register_step(self, step: ReleaseStep) -> None:
        self._undo_stack.append(step.undo)

    async def commit(self) -> None:
        return

    async def rollback(self) -> None:
        for undo in reversed(self._undo_stack):
            try:
                undo()
                self._logger.info("Successfully undone step.")
            except Exception:
                self._logger.exception("Failed to undo step.")
