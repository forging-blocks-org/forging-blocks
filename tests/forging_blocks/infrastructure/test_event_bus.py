"""
Tests for the EventBus port and InMemoryEventBus implementation.
"""

from typing import Any, Self

import pytest

from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.message import MessageMetadata
from forging_blocks.infrastructure.event_bus import EventBus, NoHandlerError
from forging_blocks.infrastructure.in_memory_event_bus import InMemoryEventBus


class FakeEvent(Event[dict[str, object]]):
    """Fake event for testing."""

    def __init__(self, value: str, metadata: MessageMetadata | None = None):
        super().__init__(metadata)
        self._value = value

    @property
    def _payload(self) -> dict[str, object]:
        return {"value": self._value}

    @property
    def value(self) -> dict[str, object]:
        return self._payload

    @classmethod
    def _from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls(value=str(data.get("value", "")), metadata=metadata)


class FakeCommand(Command[dict[str, object]]):
    """Fake command for testing."""

    def __init__(self, value: str, metadata: MessageMetadata | None = None):
        super().__init__(metadata)
        self._value = value

    @property
    def _payload(self) -> dict[str, object]:
        return {"value": self._value}

    @property
    def value(self) -> dict[str, object]:
        return self._payload

    @classmethod
    def _from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls(value=str(data.get("value", "")), metadata=metadata)


class TestEventBus:
    """Tests for the EventBus port interface."""

    def test_event_bus_is_abstract(self):
        """EventBus should be an abstract base class."""
        assert hasattr(EventBus, "__abstractmethods__")
        assert "publish" in EventBus.__abstractmethods__
        assert "send" in EventBus.__abstractmethods__
        assert "subscribe" in EventBus.__abstractmethods__
        assert "register_command_handler" in EventBus.__abstractmethods__


class TestInMemoryEventBus:
    """Tests for the InMemoryEventBus implementation."""

    @pytest.fixture
    def event_bus(self) -> InMemoryEventBus:
        """Create a fresh InMemoryEventBus for each test."""
        return InMemoryEventBus()

    @pytest.mark.asyncio
    async def test_publish_event(self, event_bus: InMemoryEventBus) -> None:
        """Test publishing an event to subscribers."""
        received_events: list[Event[Any]] = []

        async def handler(event: Event[Any]) -> None:
            received_events.append(event)

        event_bus.subscribe(FakeEvent, handler)

        event = FakeEvent("test-value")
        await event_bus.publish(event)

        assert len(received_events) == 1
        event = received_events[0]
        assert isinstance(event, FakeEvent)
        assert event.value["value"] == "test-value"

    @pytest.mark.asyncio
    async def test_publish_to_multiple_subscribers(self, event_bus: InMemoryEventBus) -> None:
        """Test publishing an event to multiple subscribers."""
        received_1: list[Event[Any]] = []
        received_2: list[Event[Any]] = []

        async def handler1(event: Event[Any]) -> None:
            received_1.append(event)

        async def handler2(event: Event[Any]) -> None:
            received_2.append(event)

        event_bus.subscribe(FakeEvent, handler1)
        event_bus.subscribe(FakeEvent, handler2)

        event = FakeEvent("test-value")
        await event_bus.publish(event)

        assert len(received_1) == 1
        assert len(received_2) == 1
        e1 = received_1[0]
        assert isinstance(e1, FakeEvent)
        assert e1.value["value"] == "test-value"
        e2 = received_2[0]
        assert isinstance(e2, FakeEvent)
        assert e2.value["value"] == "test-value"

    @pytest.mark.asyncio
    async def test_publish_no_subscribers(self, event_bus: InMemoryEventBus) -> None:
        """Test publishing an event with no subscribers."""
        event = FakeEvent("test-value")
        # Should not raise
        await event_bus.publish(event)

    @pytest.mark.asyncio
    async def test_send_command(self, event_bus: InMemoryEventBus) -> None:
        """Test sending a command to its handler."""
        received_commands: list[Command[Any]] = []

        async def handler(command: Command[Any]) -> None:
            received_commands.append(command)

        event_bus.register_command_handler(FakeCommand, handler)

        command = FakeCommand("test-value")
        await event_bus.send(command)

        assert len(received_commands) == 1
        c = received_commands[0]
        assert isinstance(c, FakeCommand)
        assert c.value["value"] == "test-value"

    @pytest.mark.asyncio
    async def test_send_command_no_handler(self, event_bus: InMemoryEventBus) -> None:
        """Test sending a command with no handler raises NoHandlerError."""
        command = FakeCommand("test-value")

        with pytest.raises(NoHandlerError):
            await event_bus.send(command)

    @pytest.mark.asyncio
    async def test_send_command_replaces_handler(self, event_bus: InMemoryEventBus) -> None:
        """Test that registering a handler twice replaces the previous one."""
        received_1: list[Command[Any]] = []
        received_2: list[Command[Any]] = []

        async def handler1(command: Command[Any]) -> None:
            received_1.append(command)

        async def handler2(command: Command[Any]) -> None:
            received_2.append(command)

        event_bus.register_command_handler(FakeCommand, handler1)
        event_bus.register_command_handler(FakeCommand, handler2)

        command = FakeCommand("test-value")
        await event_bus.send(command)

        assert len(received_1) == 0
        assert len(received_2) == 1

    @pytest.mark.asyncio
    async def test_different_event_types(self, event_bus: InMemoryEventBus) -> None:
        """Test that different event types have separate handlers."""

        class EventA(Event[dict[str, object]]):
            @property
            def _payload(self) -> dict[str, object]:
                return {"type": "A"}

            @property
            def value(self) -> dict[str, object]:
                return self._payload

            @classmethod
            def _from_payload_fields(
                cls, data: dict[str, object], metadata: MessageMetadata
            ) -> Self:
                return cls()

        class EventB(Event[dict[str, object]]):
            @property
            def _payload(self) -> dict[str, object]:
                return {"type": "B"}

            @property
            def value(self) -> dict[str, object]:
                return self._payload

            @classmethod
            def _from_payload_fields(
                cls, data: dict[str, object], metadata: MessageMetadata
            ) -> Self:
                return cls()

        received_a: list[Event[Any]] = []
        received_b: list[Event[Any]] = []

        async def handler_a(event: Event[Any]) -> None:
            received_a.append(event)

        async def handler_b(event: Event[Any]) -> None:
            received_b.append(event)

        event_bus.subscribe(EventA, handler_a)
        event_bus.subscribe(EventB, handler_b)

        await event_bus.publish(EventA())
        await event_bus.publish(EventB())

        assert len(received_a) == 1
        assert len(received_b) == 1
