from typing import Self

from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.message import MessageMetadata


class SimpleFakeCommandWithValue(Command[dict[str, object]]):
    """Minimal fake command with a ``value`` field for testing."""

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
