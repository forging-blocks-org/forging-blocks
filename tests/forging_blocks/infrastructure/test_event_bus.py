"""Tests for the EventBusBase base class and InMemoryEventBusBase implementation."""

from __future__ import annotations

import pytest

from forging_blocks.application.errors.event_bus_error import EventBusError
from forging_blocks.application.ports.inbound.message_handler import CommandHandler, EventHandler
from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.message import MessageMetadata
from forging_blocks.infrastructure.event_buses.event_bus_base import EventBusBase
from forging_blocks.infrastructure.event_buses.in_memory_event_bus_base import InMemoryEventBusBase
from tests.fixtures.fake_event_with_value import FakeEventWithValue
from tests.fixtures.simple_fake_command import SimpleFakeCommand

TestPayload = dict[str, object]


class TestEventBusBase:
    """Tests for the EventBusBase base class."""

    def test_event_bus_is_abstract(self) -> None:
        assert hasattr(EventBusBase, "__abstractmethods__")
        assert "publish" in EventBusBase.__abstractmethods__
        assert "send" in EventBusBase.__abstractmethods__
        assert "register_handler" in EventBusBase.__abstractmethods__


class TestInMemoryEventBusBase:
    """Tests for the InMemoryEventBusBase implementation."""

    @pytest.fixture
    def event_bus(self) -> InMemoryEventBusBase:
        """Create a fresh InMemoryEventBusBase for each test."""
        return InMemoryEventBusBase()

    async def test_publish_event(
        self,
        event_bus: InMemoryEventBusBase,
    ) -> None:
        """Test publishing an event to subscribers."""
        received: list[str] = []

        class HandlerA(EventHandler[TestPayload]):
            async def handle(self, message: Event[TestPayload]) -> None:
                received.append("A")

        event_bus.register_handler(FakeEventWithValue, HandlerA())

        result = await event_bus.publish(FakeEventWithValue("test-value"))
        assert result.is_ok
        assert received == ["A"]

    async def test_publish_to_multiple_subscribers(
        self,
        event_bus: InMemoryEventBusBase,
    ) -> None:
        """Test publishing an event to multiple subscribers."""
        received: list[str] = []

        class HandlerA(EventHandler[TestPayload]):
            async def handle(self, message: Event[TestPayload]) -> None:
                received.append("A")

        class HandlerB(EventHandler[TestPayload]):
            async def handle(self, message: Event[TestPayload]) -> None:
                received.append("B")

        event_bus.register_handler(FakeEventWithValue, HandlerA())
        event_bus.register_handler(FakeEventWithValue, HandlerB())

        result = await event_bus.publish(FakeEventWithValue("test-value"))
        assert result.is_ok
        assert received == ["A", "B"]

    async def test_publish_no_handlers(
        self,
        event_bus: InMemoryEventBusBase,
    ) -> None:
        """Test publishing an event with no subscribers."""
        result = await event_bus.publish(FakeEventWithValue("test-value"))
        assert result.is_ok

    async def test_send_command(
        self,
        event_bus: InMemoryEventBusBase,
    ) -> None:
        """Test sending a command to its handler."""
        handled: list[str] = []

        class Handler(CommandHandler[TestPayload]):
            async def handle(self, message: Command[TestPayload]) -> None:
                handled.append("ok")

        event_bus.register_handler(SimpleFakeCommand, Handler())
        result = await event_bus.send(SimpleFakeCommand("test-value"))
        assert result.is_ok
        assert handled == ["ok"]

    async def test_send_command_no_handler(
        self,
        event_bus: InMemoryEventBusBase,
    ) -> None:
        """Test sending a command with no handler returns error."""
        result = await event_bus.send(SimpleFakeCommand("test-value"))
        assert result.is_err
        assert isinstance(result.error, EventBusError)

    async def test_send_command_replaces_handler(
        self,
        event_bus: InMemoryEventBusBase,
    ) -> None:
        """Test that registering a handler twice replaces the previous one."""
        received_1: list[Command[TestPayload]] = []
        received_2: list[Command[TestPayload]] = []

        class Handler1(CommandHandler[TestPayload]):
            async def handle(self, message: Command[TestPayload]) -> None:
                received_1.append(message)

        class Handler2(CommandHandler[TestPayload]):
            async def handle(self, message: Command[TestPayload]) -> None:
                received_2.append(message)

        event_bus.register_handler(SimpleFakeCommand, Handler1())
        event_bus.register_handler(SimpleFakeCommand, Handler2())

        command = SimpleFakeCommand("test-value")
        await event_bus.send(command)

        assert len(received_1) == 0
        assert len(received_2) == 1

    async def test_different_event_types(
        self,
        event_bus: InMemoryEventBusBase,
    ) -> None:
        """Test that different event types have separate handlers."""
        received_a: list[str] = []
        received_b: list[str] = []

        class HandlerA(EventHandler[TestPayload]):
            async def handle(self, message: Event[TestPayload]) -> None:
                received_a.append("A")

        class HandlerB(EventHandler[TestPayload]):
            async def handle(self, message: Event[TestPayload]) -> None:
                received_b.append("B")

        class EventA(Event[TestPayload]):
            @property
            def _payload(self) -> TestPayload:
                return {"type": "A"}

            @property
            def value(self) -> TestPayload:
                return self._payload

            @classmethod
            def _from_payload_fields(cls, data: TestPayload, metadata: MessageMetadata) -> EventA:
                return cls()

        class EventB(Event[TestPayload]):
            @property
            def _payload(self) -> TestPayload:
                return {"type": "B"}

            @property
            def value(self) -> TestPayload:
                return self._payload

            @classmethod
            def _from_payload_fields(cls, data: TestPayload, metadata: MessageMetadata) -> EventB:
                return cls()

        event_bus.register_handler(EventA, HandlerA())
        event_bus.register_handler(EventB, HandlerB())

        await event_bus.publish(EventA())
        await event_bus.publish(EventB())

        assert received_a == ["A"]
        assert received_b == ["B"]

    async def test_handler_error(
        self,
        event_bus: InMemoryEventBusBase,
    ) -> None:
        """Test that handler errors are captured as EventBusError."""

        class FailingHandler(EventHandler[TestPayload]):
            async def handle(self, message: Event[TestPayload]) -> None:
                raise ValueError("boom")

        event_bus.register_handler(FakeEventWithValue, FailingHandler())
        result = await event_bus.publish(FakeEventWithValue("x"))
        assert result.is_err
        assert isinstance(result.error, EventBusError)
