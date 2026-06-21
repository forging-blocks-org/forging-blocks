from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.message import MessageMetadata


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
