import pytest
from unittest.mock import AsyncMock

from forging_blocks.application.ports.inbound.message_handler import CommandHandler
from forging_blocks.domain.messages.command import Command
from scripts.release.infrastructure.bus.in_memory_release_command_bus import (
    InMemoryReleaseCommandBus,
)


@pytest.mark.unit
class TestInMemoryReleaseCommandBus:
    def test_init_when_called_then_instance_created(self) -> None:
        bus = InMemoryReleaseCommandBus()

        assert isinstance(bus, InMemoryReleaseCommandBus)

    @pytest.mark.asyncio
    async def test_register_when_called_then_handler_is_registered(self) -> None:
        bus = InMemoryReleaseCommandBus()
        handler = AsyncMock(spec=CommandHandler)
        command_type = type(AsyncMock(spec=Command))

        await bus.register(command_type, handler)

        assert bus._subscribers[command_type] == handler

    @pytest.mark.asyncio
    async def test_send_when_no_subscribers_then_key_error(self) -> None:
        bus = InMemoryReleaseCommandBus()
        command = AsyncMock(spec=Command)

        with pytest.raises(KeyError):
            await bus.send(command)

    @pytest.mark.asyncio
    async def test_send_when_handler_registered_then_handler_handle_called(
        self,
    ) -> None:
        bus = InMemoryReleaseCommandBus()
        handler = AsyncMock(spec=CommandHandler)
        command = AsyncMock(spec=Command)
        command_type = type(command)

        await bus.register(command_type, handler)

        await bus.send(command)

        handler.handle.assert_awaited_once_with(command)

    @pytest.mark.asyncio
    async def test_send_when_handler_registered_for_different_type_then_key_error(
        self,
    ) -> None:
        bus = InMemoryReleaseCommandBus()
        handler = AsyncMock(spec=CommandHandler)
        registered_command = AsyncMock(spec=Command)
        different_command = AsyncMock(spec=Command)

        await bus.register(type(registered_command), handler)

        with pytest.raises(KeyError):
            await bus.send(different_command)
