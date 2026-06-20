"""Tests for the InMemoryEventBus implementation."""

from typing import Any, cast

import pytest

from forging_blocks.application.errors.event_bus_error import EventBusError
from forging_blocks.application.ports.inbound.message_handler import (
    CommandHandler,
    EventHandler,
)
from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.message import MessageMetadata
from forging_blocks.infrastructure.event_buses.in_memory_event_bus import (
    InMemoryEventBus,
)


class FakeEvent(Event[dict[str, object]]):
    """A simple event for testing."""

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
    def _from_payload_fields(
        cls, data: dict[str, object], metadata: MessageMetadata
    ) -> "FakeEvent":
        return cls(name=str(data.get("name", "")), metadata=metadata)


class FakeCommand(Command[dict[str, object]]):
    """A simple command for testing."""

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
    def _from_payload_fields(
        cls, data: dict[str, object], metadata: MessageMetadata
    ) -> "FakeCommand":
        return cls(name=str(data.get("name", "")), metadata=metadata)


@pytest.mark.unit
class TestInMemoryEventBus:
    """InMemoryEventBus publish / send / register behaviour."""

    async def test_publish_sends_to_multiple_handlers(self) -> None:
        """Publishing an event dispatches to all registered handlers."""
        bus: InMemoryEventBus[dict[str, object], dict[str, object]] = InMemoryEventBus()
        received: list[str] = []

        class HandlerA(EventHandler[dict[str, object]]):
            async def handle(self, message: Event[dict[str, object]]) -> None:  # type: ignore[override]
                received.append("A")

        class HandlerB(EventHandler[dict[str, object]]):
            async def handle(self, message: Event[dict[str, object]]) -> None:  # type: ignore[override]
                received.append("B")

        bus.register_handler(FakeEvent, HandlerA())
        bus.register_handler(FakeEvent, HandlerB())

        result = await bus.publish(FakeEvent("test"))
        assert result.is_ok
        assert received == ["A", "B"]

    async def test_send_dispatches_to_single_handler(self) -> None:
        """Sending a command dispatches to its single registered handler."""
        bus: InMemoryEventBus[dict[str, object], dict[str, object]] = InMemoryEventBus()
        handled: list[str] = []

        class Handler(CommandHandler[dict[str, object]]):
            async def handle(self, message: Command[dict[str, object]]) -> None:  # type: ignore[override]
                handled.append(cast(Any, message)._name)

        bus.register_handler(FakeCommand, Handler())

        result = await bus.send(FakeCommand("do-something"))
        assert result.is_ok
        assert handled == ["do-something"]

    async def test_send_no_handler_returns_error(self) -> None:
        """Sending a command with no registered handler returns an error."""
        bus: InMemoryEventBus[dict[str, object], dict[str, object]] = InMemoryEventBus()
        result = await bus.send(FakeCommand("missing"))
        assert result.is_err
        assert isinstance(result.error, EventBusError)

    async def test_handler_error_propagation(self) -> None:
        """Exceptions in handlers propagate as EventBusError."""
        bus: InMemoryEventBus[dict[str, object], dict[str, object]] = InMemoryEventBus()

        class FailingHandler(EventHandler[dict[str, object]]):
            async def handle(self, message: Event[dict[str, object]]) -> None:  # type: ignore[override]
                raise ValueError("handler failure")

        bus.register_handler(FakeEvent, FailingHandler())

        result = await bus.publish(FakeEvent("boom"))
        assert result.is_err
        assert isinstance(result.error, EventBusError)
