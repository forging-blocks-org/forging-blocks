"""Fake MessageBus implementation for infrastructure tests.

Tracks dispatched messages so tests can verify behaviour through
state inspection rather than mock interaction assertions.
"""

from typing import Any


class FakeMessageBus:
    """State-based MessageBusPort fake.

    Records every dispatched message for later assertion. No mocking
    framework — just a plain object that honours the protocol.
    """

    def __init__(self, dispatch_result: Any = None) -> None:
        self.dispatched_messages: list[Any] = []
        self._dispatch_result = dispatch_result

    async def dispatch(self, message: Any) -> Any:
        self.dispatched_messages.append(message)
        return self._dispatch_result

    def pop_message(self) -> Any | None:
        """Return and remove the most recent dispatched message, or None."""
        return self.dispatched_messages.pop() if self.dispatched_messages else None
