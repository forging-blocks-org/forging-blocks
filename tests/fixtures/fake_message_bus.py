"""Fake MessageBus implementation for infrastructure tests.

Tracks dispatched messages so tests can verify behaviour through
state inspection rather than mock interaction assertions.
"""

from forging_blocks.application.ports.outbound.message_bus_port import MessageBusPort


class FakeMessageBus(MessageBusPort[object, object]):
    """State-based MessageBusPort fake.

    Records every dispatched message for later assertion. No mocking
    framework — just a plain object that explicitly inherits the port.
    """

    def __init__(self, dispatch_result: object = None) -> None:
        self.dispatched_messages: list[object] = []
        self._dispatch_result = dispatch_result

    async def dispatch(self, message: object) -> object:
        self.dispatched_messages.append(message)
        return self._dispatch_result

    def pop_message(self) -> object | None:
        """Return and remove the most recent dispatched message, or None."""
        return self.dispatched_messages.pop() if self.dispatched_messages else None
