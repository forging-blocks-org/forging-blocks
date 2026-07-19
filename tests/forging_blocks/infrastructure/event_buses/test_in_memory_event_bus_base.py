"""Tests for the EventBusBase base class and InMemoryEventBusBase implementation."""

from __future__ import annotations

import pytest

from forging_blocks.application.errors.event_bus_error import EventBusError
from forging_blocks.application.ports.inbound.message_handler import CommandHandler, EventHandler
from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.infrastructure.event_buses.event_bus_base import EventBusBase
from forging_blocks.infrastructure.event_buses.in_memory_event_bus_base import (
    InMemoryEventBusBase,
)
from tests.fixtures.fake_event_with_value import FakeEventWithValue
from tests.fixtures.simple_fake_command_with_value import SimpleFakeCommandWithValue

TestPayload = dict[str, object]


class TestEventBusBase:
    """Tests for the EventBusBase abstract base class."""

    def test_event_bus_is_abstract(self) -> None:
        """EventBusBase should be an abstract base class."""
        assert hasattr(EventBusBase, "__abstractmethods__")
        assert "publish" in EventBusBase.__abstractmethods__
        assert "send" in EventBusBase.__abstractmethods__
        assert "register_handler" in EventBusBase.__abstractmethods__


class TestInMemoryEventBusBase:
    """Tests for the InMemoryEventBusBase implementation."""

    @pytest.fixture
    def event_bus(self) -> InMemoryEventBusBase[TestPayload, TestPayload]:
        """Create a fresh InMemoryEventBusBase for each test."""
        return InMemoryEventBusBase[TestPayload, TestPayload]()

    async def test_publish_event(
        self,
        event_bus: InMemoryEventBusBase[TestPayload, TestPayload],
    ) -> None:
        """Test publishing an event to subscribers."""
        received_events: list[FakeEventWithValue] = []

        class TestHandler(EventHandler[TestPayload]):
            async def handle(self, message: Event[TestPayload]) -> None:
                received_events.append(message)  # type: ignore[arg-type]

        event_bus.register_handler(FakeEventWithValue, TestHandler())
        event = FakeEventWithValue("test-value")
        result = await event_bus.publish(event)
        assert result.is_ok
        assert len(received_events) == 1
        assert received_events[0].value["value"] == "test-value"

    async def test_publish_to_multiple_subscribers(
        self,
        event_bus: InMemoryEventBusBase[TestPayload, TestPayload],
    ) -> None:
        """Test publishing an event to multiple subscribers."""
        received_1: list[str] = []
        received_2: list[str] = []

        class Handler1(EventHandler[TestPayload]):
            async def handle(self, message: Event[TestPayload]) -> None:
                received_1.append("handler1")

        class Handler2(EventHandler[TestPayload]):
            async def handle(self, message: Event[TestPayload]) -> None:
                received_2.append("handler2")

        event_bus.register_handler(FakeEventWithValue, Handler1())
        event_bus.register_handler(FakeEventWithValue, Handler2())
        result = await event_bus.publish(FakeEventWithValue("test"))
        assert result.is_ok
        assert len(received_1) == 1
        assert len(received_2) == 1

    async def test_publish_no_subscribers(
        self,
        event_bus: InMemoryEventBusBase[TestPayload, TestPayload],
    ) -> None:
        """Test publishing an event with no subscribers."""
        event = FakeEventWithValue("test-value")
        result = await event_bus.publish(event)
        assert result.is_ok

    async def test_send_command(
        self,
        event_bus: InMemoryEventBusBase[TestPayload, TestPayload],
    ) -> None:
        """Test sending a command to its handler."""
        received_commands: list[SimpleFakeCommandWithValue] = []

        class TestCmdHandler(CommandHandler[TestPayload]):
            async def handle(self, message: Command[TestPayload]) -> None:
                received_commands.append(message)  # type: ignore[arg-type]

        event_bus.register_handler(SimpleFakeCommandWithValue, TestCmdHandler())
        command = SimpleFakeCommandWithValue("test-cmd")
        result = await event_bus.send(command)
        assert result.is_ok
        assert len(received_commands) == 1

    async def test_send_when_handler_raises_then_returns_error(
        self,
        event_bus: InMemoryEventBusBase[TestPayload, TestPayload],
    ) -> None:
        """Sending a command whose handler raises returns ``EventBusError``."""

        class FailingHandler(CommandHandler[TestPayload]):
            async def handle(self, message: Command[TestPayload]) -> None:
                raise RuntimeError("Handler exploded")

        event_bus.register_handler(SimpleFakeCommandWithValue, FailingHandler())
        command = SimpleFakeCommandWithValue("crash")
        result = await event_bus.send(command)
        assert result.is_err
        assert isinstance(result.error, EventBusError)
        assert "Handler exploded" in str(result.error.message)
