"""Tests for the AbstractEventBus base class and InMemoryAbstractEventBus implementation."""

from __future__ import annotations

import pytest

from forging_blocks.application.ports.inbound.message_handler import CommandHandler, EventHandler
from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.infrastructure.event_buses.abstract_event_bus import AbstractEventBus
from forging_blocks.infrastructure.event_buses.in_memory_event_bus_abc import (
    InMemoryAbstractEventBus,
)
from tests.fixtures.fake_event_with_value import FakeEventWithValue
from tests.fixtures.simple_fake_command_with_value import SimpleFakeCommandWithValue

TestPayload = dict[str, object]


class TestAbstractEventBus:
    """Tests for the AbstractEventBus abstract base class."""

    def test_event_bus_is_abstract(self) -> None:
        """AbstractEventBus should be an abstract base class."""
        assert hasattr(AbstractEventBus, "__abstractmethods__")
        assert "publish" in AbstractEventBus.__abstractmethods__
        assert "send" in AbstractEventBus.__abstractmethods__
        assert "register_handler" in AbstractEventBus.__abstractmethods__


class TestInMemoryAbstractEventBus:
    """Tests for the InMemoryAbstractEventBus implementation."""

    @pytest.fixture
    def event_bus(self) -> InMemoryAbstractEventBus[TestPayload, TestPayload]:
        """Create a fresh InMemoryAbstractEventBus for each test."""
        return InMemoryAbstractEventBus[TestPayload, TestPayload]()

    async def test_publish_event(
        self,
        event_bus: InMemoryAbstractEventBus[TestPayload, TestPayload],
    ) -> None:
        """Test publishing an event to subscribers."""
        received_events: list[FakeEventWithValue] = []

        class Handler(EventHandler[TestPayload]):
            async def handle(self, message: Event[TestPayload]) -> None:
                received_events.append(message)  # type: ignore[arg-type]

        event_bus.register_handler(FakeEventWithValue, Handler())

        event = FakeEventWithValue("test-value")
        result = await event_bus.publish(event)
        assert result.is_ok

        assert len(received_events) == 1
        assert isinstance(received_events[0], FakeEventWithValue)
        assert received_events[0].value["value"] == "test-value"

    async def test_publish_to_multiple_subscribers(
        self,
        event_bus: InMemoryAbstractEventBus[TestPayload, TestPayload],
    ) -> None:
        """Test publishing an event to multiple subscribers."""
        received_1: list[str] = []
        received_2: list[str] = []

        class Handler1(EventHandler[TestPayload]):
            async def handle(self, message: Event[TestPayload]) -> None:
                received_1.append("1")

        class Handler2(EventHandler[TestPayload]):
            async def handle(self, message: Event[TestPayload]) -> None:
                received_2.append("2")

        event_bus.register_handler(FakeEventWithValue, Handler1())
        event_bus.register_handler(FakeEventWithValue, Handler2())

        event = FakeEventWithValue("test-value")
        result = await event_bus.publish(event)
        assert result.is_ok

        assert len(received_1) == 1
        assert len(received_2) == 1

    async def test_publish_no_subscribers(
        self,
        event_bus: InMemoryAbstractEventBus[TestPayload, TestPayload],
    ) -> None:
        """Test publishing an event with no subscribers."""
        event = FakeEventWithValue("test-value")
        result = await event_bus.publish(event)
        assert result.is_ok

    async def test_send_command(
        self,
        event_bus: InMemoryAbstractEventBus[TestPayload, TestPayload],
    ) -> None:
        """Test sending a command to its handler."""
        received_commands: list[SimpleFakeCommandWithValue] = []

        class Handler(CommandHandler[TestPayload]):
            async def handle(self, message: Command[TestPayload]) -> None:
                received_commands.append(message)  # type: ignore[arg-type]

        event_bus.register_handler(SimpleFakeCommandWithValue, Handler())

        command = SimpleFakeCommandWithValue("test-value")
        result = await event_bus.send(command)
        assert result.is_ok

        assert len(received_commands) == 1
