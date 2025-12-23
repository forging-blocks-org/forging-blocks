from typing import Any
from forging_blocks.domain.messages.event import Event


class ReleasePreparedEvent(Event[dict[str, Any]]):
    def __init__(self, *, version: str, branch: str) -> None:
        self._version = version
        self._branch = branch
        self._value = {"version": self._version, "branch": self._branch}

        super().__init__()

    @property
    def value(self) -> dict[str, Any]:
        return self._value

    @property
    def _payload(self) -> dict[str, Any]:
        return self._value
