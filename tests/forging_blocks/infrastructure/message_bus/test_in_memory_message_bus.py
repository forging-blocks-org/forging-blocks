# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from typing import Any

import pytest

from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.query import Query
from forging_blocks.infrastructure.message_bus.in_memory_message_bus import (
    InMemoryMessageBus,
)


class FakeCommand(Command[str]):
    """A fake command for testing."""

    def __init__(self, data: str) -> None:
        super().__init__()
        self._data = data

    @property
    def value(self) -> str:
        return self._data

    @property
    def _payload(self) -> dict[str, Any]:
        return {"data": self._data}


class FakeQuery(Query):
    """A fake query for testing."""

    def __init__(self, data: str) -> None:
        super().__init__()
        self._data = data

    @property
    def value(self) -> str:
        return self._data

    @property
    def _payload(self) -> dict[str, Any]:
        return {"data": self._data}


@pytest.mark.unit
class TestInMemoryMessageBus:
    def test_init_when_created_then_has_empty_handler_registry(self) -> None:
        bus = InMemoryMessageBus()

        assert len(bus._handlers) == 0

    def test_register_when_new_message_type_then_registers_handler(self) -> None:
        bus = InMemoryMessageBus()

        def handler(cmd: FakeCommand) -> None:
            return None

        bus.register(FakeCommand, handler)

        assert FakeCommand in bus._handlers
        assert bus._handlers[FakeCommand] is handler

    def test_register_when_message_type_already_registered_then_raises_value_error(
        self,
    ) -> None:
        bus = InMemoryMessageBus()

        def handler(cmd: FakeCommand) -> None:
            return None

        bus.register(FakeCommand, handler)

        with pytest.raises(ValueError, match="already registered"):
            bus.register(FakeCommand, handler)

    async def test_dispatch_when_handler_registered_then_calls_handler_with_message(
        self,
    ) -> None:
        bus = InMemoryMessageBus()
        call_log: list[FakeCommand] = []

        def handler(cmd: FakeCommand) -> None:
            call_log.append(cmd)

        bus.register(FakeCommand, handler)
        command = FakeCommand("test")

        await bus.dispatch(command)

        assert len(call_log) == 1
        assert call_log[0] is command

    async def test_dispatch_when_handler_returns_value_then_returns_result(
        self,
    ) -> None:
        bus = InMemoryMessageBus()

        def handler(query: FakeQuery) -> str:
            return query.value.upper()

        bus.register(FakeQuery, handler)
        query = FakeQuery("hello")

        result = await bus.dispatch(query)

        assert result == "HELLO"

    async def test_dispatch_when_no_handler_registered_then_raises_key_error(
        self,
    ) -> None:
        bus = InMemoryMessageBus()
        command = FakeCommand("test")

        with pytest.raises(KeyError):
            await bus.dispatch(command)

    async def test_dispatch_routes_by_type_not_by_value(self) -> None:
        bus = InMemoryMessageBus()
        handler_results: list[str] = []

        def handler(cmd: FakeCommand) -> None:
            handler_results.append(cmd.value)

        bus.register(FakeCommand, handler)

        await bus.dispatch(FakeCommand("first"))
        await bus.dispatch(FakeCommand("second"))

        assert handler_results == ["first", "second"]
