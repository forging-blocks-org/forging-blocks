"""
Tests for the EventBus port and InMemoryEventBus implementation.
"""

import pytest

from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.infrastructure.event_bus import EventBus, NoHandlerError
from forging_blocks.infrastructure.in_memory_event_bus import InMemoryEventBus


class TestEvent(Event[dict[str, object]]):
    """Test event for testing."""

    def __init__(self, value: str):
        super().__init__()
        self._value = value

    @property
    def _payload(self) -> dict[str, object]:
        return {"value": self._value}

    @property
    def value(self) -> dict[str, object]:
        return self._payload


class TestCommand(Command[dict[str, object]]):
    """Test command for testing."""

    def __init__(self, value: str):
        super().__init__()
        self._value = value

    @property
    def _payload(self) -> dict[str, object]:
        return {"value": self._value}

    @property
    def value(self) -> dict[str, object]:
        return self._payload


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
    def event_bus(self):
        """Create a fresh InMemoryEventBus for each test."""
        return InMemoryEventBus()

    @pytest.mark.asyncio
    async def test_publish_event(self, event_bus):
        """Test publishing an event to subscribers."""
        received_events = []

        async def handler(event: TestEvent):
            received_events.append(event)

        event_bus.subscribe(TestEvent, handler)

        event = TestEvent("test-value")
        await event_bus.publish(event)

        assert len(received_events) == 1
        assert received_events[0].value["value"] == "test-value"

    @pytest.mark.asyncio
    async def test_publish_to_multiple_subscribers(self, event_bus):
        """Test publishing an event to multiple subscribers."""
        received_1 = []
        received_2 = []

        async def handler1(event: TestEvent):
            received_1.append(event)

        async def handler2(event: TestEvent):
            received_2.append(event)

        event_bus.subscribe(TestEvent, handler1)
        event_bus.subscribe(TestEvent, handler2)

        event = TestEvent("test-value")
        await event_bus.publish(event)

        assert len(received_1) == 1
        assert len(received_2) == 1
        assert received_1[0].value["value"] == "test-value"
        assert received_2[0].value["value"] == "test-value"

    @pytest.mark.asyncio
    async def test_publish_no_subscribers(self, event_bus):
        """Test publishing an event with no subscribers."""
        event = TestEvent("test-value")
        # Should not raise
        await event_bus.publish(event)

    @pytest.mark.asyncio
    async def test_send_command(self, event_bus):
        """Test sending a command to its handler."""
        received_commands = []

        async def handler(command: TestCommand):
            received_commands.append(command)

        event_bus.register_command_handler(TestCommand, handler)

        command = TestCommand("test-value")
        await event_bus.send(command)

        assert len(received_commands) == 1
        assert received_commands[0].value["value"] == "test-value"

    @pytest.mark.asyncio
    async def test_send_command_no_handler(self, event_bus):
        """Test sending a command with no handler raises NoHandlerError."""
        command = TestCommand("test-value")

        with pytest.raises(NoHandlerError):
            await event_bus.send(command)

    @pytest.mark.asyncio
    async def test_send_command_replaces_handler(self, event_bus):
        """Test that registering a handler twice replaces the previous one."""
        received_1 = []
        received_2 = []

        async def handler1(command: TestCommand):
            received_1.append(command)

        async def handler2(command: TestCommand):
            received_2.append(command)

        event_bus.register_command_handler(TestCommand, handler1)
        event_bus.register_command_handler(TestCommand, handler2)

        command = TestCommand("test-value")
        await event_bus.send(command)

        assert len(received_1) == 0
        assert len(received_2) == 1

    @pytest.mark.asyncio
    async def test_different_event_types(self, event_bus):
        """Test that different event types have separate handlers."""

        class EventA(Event[dict[str, object]]):
            @property
            def _payload(self) -> dict[str, object]:
                return {"type": "A"}

            @property
            def value(self) -> dict[str, object]:
                return self._payload

        class EventB(Event[dict[str, object]]):
            @property
            def _payload(self) -> dict[str, object]:
                return {"type": "B"}

            @property
            def value(self) -> dict[str, object]:
                return self._payload

        received_a = []
        received_b = []

        async def handler_a(event: EventA):
            received_a.append(event)

        async def handler_b(event: EventB):
            received_b.append(event)

        event_bus.subscribe(EventA, handler_a)
        event_bus.subscribe(EventB, handler_b)

        await event_bus.publish(EventA())
        await event_bus.publish(EventB())

        assert len(received_a) == 1
        assert len(received_b) == 1
