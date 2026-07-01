"""
Tests for the EventBusPort port and InMemoryEventBus implementation.
"""

from typing import Any, Self

import pytest

from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.message import MessageMetadata
from forging_blocks.infrastructure.event_bus import EventBusPort, NoHandlerError
from forging_blocks.infrastructure.in_memory_event_bus import InMemoryEventBus
from tests.fixtures.fake_event_with_value import FakeEventWithValue
from tests.fixtures.simple_fake_command import SimpleFakeCommand
from tests.fixtures.simple_fake_command_with_value import SimpleFakeCommandWithValue


class TestEventBus:
    """Tests for the EventBusPort port interface."""

    def test_event_bus_is_abstract(self):
        """EventBusPort should be an abstract base class."""
        assert hasattr(EventBusPort, "__abstractmethods__")
        assert "publish" in EventBusPort.__abstractmethods__
        assert "send" in EventBusPort.__abstractmethods__
        assert "subscribe" in EventBusPort.__abstractmethods__
        assert "register_command_handler" in EventBusPort.__abstractmethods__


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

        event_bus.subscribe(FakeEventWithValue, handler)

        event = FakeEventWithValue("test-value")
        await event_bus.publish(event)

        assert len(received_events) == 1
        event = received_events[0]
        assert isinstance(event, FakeEventWithValue)
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

        event_bus.subscribe(FakeEventWithValue, handler1)
        event_bus.subscribe(FakeEventWithValue, handler2)

        event = FakeEventWithValue("test-value")
        await event_bus.publish(event)

        assert len(received_1) == 1
        assert len(received_2) == 1
        e1 = received_1[0]
        assert isinstance(e1, FakeEventWithValue)
        assert e1.value["value"] == "test-value"
        e2 = received_2[0]
        assert isinstance(e2, FakeEventWithValue)
        assert e2.value["value"] == "test-value"

    @pytest.mark.asyncio
    async def test_publish_no_subscribers(self, event_bus: InMemoryEventBus) -> None:
        """Test publishing an event with no subscribers."""
        event = FakeEventWithValue("test-value")
        # Should not raise
        await event_bus.publish(event)

    @pytest.mark.asyncio
    async def test_send_command(self, event_bus: InMemoryEventBus) -> None:
        """Test sending a command to its handler."""
        received_commands: list[Command[Any]] = []

        async def handler(command: Command[Any]) -> None:
            received_commands.append(command)

        event_bus.register_command_handler(SimpleFakeCommandWithValue, handler)

        command = SimpleFakeCommandWithValue("test-value")
        await event_bus.send(command)

        assert len(received_commands) == 1
        c = received_commands[0]
        assert isinstance(c, SimpleFakeCommandWithValue)
        assert c.value["value"] == "test-value"

    @pytest.mark.asyncio
    async def test_send_command_no_handler(self, event_bus: InMemoryEventBus) -> None:
        """Test sending a command with no handler raises NoHandlerError."""
        command = SimpleFakeCommand("test-value")

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

        event_bus.register_command_handler(SimpleFakeCommand, handler1)
        event_bus.register_command_handler(SimpleFakeCommand, handler2)

        command = SimpleFakeCommand("test-value")
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
