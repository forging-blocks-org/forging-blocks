from typing import Self

from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.message import MessageMetadata


class FakeEventWithName(Event[dict[str, object]]):
    """Simple event fixture carrying a ``name`` field.

    Shared by event bus and event store tests.
    """

    def __init__(self, name: str, metadata: MessageMetadata | None = None) -> None:
        super().__init__(metadata)
        self._name = name

    @property
    def _payload(self) -> dict[str, object]:
        return {"name": self._name}

    @property
    def value(self) -> dict[str, object]:
        return self._payload

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls(name=str(data.get("name", "")), metadata=metadata)
