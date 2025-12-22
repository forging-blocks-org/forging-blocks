from typing import Any, Callable
from scripts.release.application.ports.outbound import ReleaseTransaction
from scripts.release.application.workflow import ReleaseStep


class InMemoryReleaseTransaction(ReleaseTransaction):
    def __init__(self) -> None:
        self._undo_stack: list[Callable[[], None]] = []

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
            except Exception:
                pass
