from typing import Any, Self

import pytest

from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.message import MessageMetadata
from forging_blocks.foundation.messages.query import Query
from forging_blocks.infrastructure.message_bus.in_memory_message_bus import (
    InMemoryMessageBus,
)


class FakeCommand(Command[str]):
    """A fake command for testing."""

    def __init__(self, data: str, metadata: MessageMetadata | None = None) -> None:
        super().__init__(metadata)
        self._data = data

    @property
    def value(self) -> str:
        return self._data

    @property
    def _payload(self) -> dict[str, Any]:
        return {"data": self._data}

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls(data=str(data.get("data", "")), metadata=metadata)


class FakeQuery(Query[dict[str, Any]]):
    def __init__(self, data: str, metadata: MessageMetadata | None = None) -> None:
        super().__init__(metadata)
        self._data = data

    @property
    def value(self) -> dict[str, Any]:
        return self._payload

    @property
    def _payload(self) -> dict[str, Any]:
        return {"data": self._data}

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls(data=str(data.get("data", "")), metadata=metadata)


@pytest.mark.integration
class TestInMemoryMessageBus:
    def test_init_when_created_then_has_empty_handler_registry(self) -> None:
        bus: InMemoryMessageBus[Command[object], object] = InMemoryMessageBus[
            Command[object], object
        ]()

        assert len(getattr(bus, "_handlers")) == 0

    def test_register_when_new_message_type_then_registers_handler(self) -> None:
        bus: InMemoryMessageBus[Command[object], object] = InMemoryMessageBus[
            Command[object], object
        ]()

        def handler(cmd: FakeCommand) -> None:
            return None

        bus.register(FakeCommand, handler)

        assert FakeCommand in getattr(bus, "_handlers")
        assert getattr(bus, "_handlers")[FakeCommand] is handler

    def test_register_when_message_type_already_registered_then_raises_value_error(
        self,
    ) -> None:
        bus: InMemoryMessageBus[Command[object], object] = InMemoryMessageBus[
            Command[object], object
        ]()

        def handler(cmd: FakeCommand) -> None:
            return None

        bus.register(FakeCommand, handler)

        with pytest.raises(ValueError, match="already registered"):
            bus.register(FakeCommand, handler)

    async def test_dispatch_when_handler_registered_then_calls_handler_with_message(
        self,
    ) -> None:
        bus: InMemoryMessageBus[Command[object], object] = InMemoryMessageBus[
            Command[object], object
        ]()
        call_log: list[FakeCommand] = []

        def handler(cmd: FakeCommand) -> None:
            call_log.append(cmd)

        bus.register(FakeCommand, handler)
        command = FakeCommand("test")

        await bus.dispatch(command)

        assert len(call_log) == 1

    async def test_dispatch_when_handler_returns_value_then_returns_result(
        self,
    ) -> None:
        bus: InMemoryMessageBus[Query[dict[str, Any]], str] = InMemoryMessageBus[
            Query[dict[str, Any]], str
        ]()

        def handler(query: FakeQuery) -> str:
            return query.value["data"].upper()

        bus.register(FakeQuery, handler)
        query = FakeQuery("hello")

        await bus.dispatch(query)

    async def test_dispatch_when_no_handler_registered_then_raises_key_error(
        self,
    ) -> None:
        bus: InMemoryMessageBus[Command[object], object] = InMemoryMessageBus[
            Command[object], object
        ]()
        command = FakeCommand("test")

        with pytest.raises(KeyError):
            await bus.dispatch(command)

    async def test_dispatch_routes_by_type_not_by_value(self) -> None:
        bus: InMemoryMessageBus[Command[object], object] = InMemoryMessageBus[
            Command[object], object
        ]()
        handler_results: list[str] = []

        def handler(cmd: FakeCommand) -> None:
            handler_results.append(cmd.value)

        bus.register(FakeCommand, handler)

        await bus.dispatch(FakeCommand("first"))
        await bus.dispatch(FakeCommand("second"))

        assert handler_results == ["first", "second"]

    async def test_dispatch_when_handler_is_async_then_awaits_and_returns_result(
        self,
    ) -> None:
        bus: InMemoryMessageBus[Command[object], str] = InMemoryMessageBus[Command[object], str]()

        async def handler(cmd: FakeCommand) -> str:
            return cmd.value.upper()

        bus.register(FakeCommand, handler)
        result = await bus.dispatch(FakeCommand("hello"))

        assert result == "HELLO"
