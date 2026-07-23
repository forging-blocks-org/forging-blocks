from typing import Self

from forging_blocks.domain.messages.event import Event
from forging_blocks.domain.messages.message import MessageMetadata


class FakeEventWithValue(Event[dict[str, object]]):
    """Simple event fixture carrying a ``value`` field.

    Shared by event bus and repository tests.
    """

    def __init__(self, value: str, metadata: MessageMetadata | None = None) -> None:
        super().__init__(metadata)
        self._value = value

    @property
    def _payload(self) -> dict[str, object]:
        return {"value": self._value}

    @property
    def value(self) -> dict[str, object]:
        return self._payload

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls(value=str(data.get("value", "")), metadata=metadata)
