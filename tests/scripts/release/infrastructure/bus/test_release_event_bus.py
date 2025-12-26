import pytest
from unittest.mock import AsyncMock

from forging_blocks.application.ports.inbound.message_handler import MessageHandler
from forging_blocks.domain.messages.message import Message
from scripts.release.infrastructure.bus.in_memory_release_event_bus import (
    InMemoryReleaseEventBus,
)


class TestInMemoryReleaseEventBus:
    def test_init_when_called_then_instance_created(self) -> None:
        bus = InMemoryReleaseEventBus()

        assert isinstance(bus, InMemoryReleaseEventBus)

    @pytest.mark.asyncio
    async def test_subscribe_when_called_then_handler_is_registered(self) -> None:
        bus = InMemoryReleaseEventBus()
        handler = AsyncMock(spec=MessageHandler)

        bus.subscribe(handler)

        assert handler in bus._subscribers  # acceptable for infra-level unit test

    @pytest.mark.asyncio
    async def test_publish_when_no_subscribers_then_no_error(self) -> None:
        bus = InMemoryReleaseEventBus()
        message = AsyncMock(spec=Message)

        await bus.publish(message)  # should not raise

    @pytest.mark.asyncio
    async def test_publish_when_single_subscriber_then_handler_handle_called(
        self,
    ) -> None:
        bus = InMemoryReleaseEventBus()
        handler = AsyncMock(spec=MessageHandler)
        message = AsyncMock(spec=Message)

        bus.subscribe(handler)

        await bus.publish(message)

        handler.handle.assert_awaited_once_with(message)

    @pytest.mark.asyncio
    async def test_publish_when_multiple_subscribers_then_all_handlers_called(
        self,
    ) -> None:
        bus = InMemoryReleaseEventBus()
        handler1 = AsyncMock(spec=MessageHandler)
        handler2 = AsyncMock(spec=MessageHandler)
        message = AsyncMock(spec=Message)

        bus.subscribe(handler1)
        bus.subscribe(handler2)

        await bus.publish(message)

        handler1.handle.assert_awaited_once_with(message)
        handler2.handle.assert_awaited_once_with(message)

    @pytest.mark.asyncio
    async def test_publish_preserves_subscription_order(self) -> None:
        bus = InMemoryReleaseEventBus()
        calls: list[str] = []

        async def handler_1(_: Message) -> None:
            calls.append("handler_1")

        async def handler_2(_: Message) -> None:
            calls.append("handler_2")

        handler1 = AsyncMock(spec=MessageHandler)
        handler2 = AsyncMock(spec=MessageHandler)
        handler1.handle.side_effect = handler_1
        handler2.handle.side_effect = handler_2

        bus.subscribe(handler1)
        bus.subscribe(handler2)

        await bus.publish(AsyncMock(spec=Message))

        assert calls == ["handler_1", "handler_2"]
