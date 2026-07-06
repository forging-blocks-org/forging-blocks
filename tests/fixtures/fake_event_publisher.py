"""Fake EventPublisher implementation for infrastructure tests.

Tracks published events so tests can verify behaviour through
state inspection rather than mock interaction assertions.
"""

from typing import Any


class FakeEventPublisher:
    """State-based EventPublisherPort fake.

    Records every published event for later assertion. Optionally
    raises a configured error on publish to test error handling.
    """

    def __init__(self, should_raise: Exception | None = None) -> None:
        self.published_events: list[Any] = []
        self._should_raise = should_raise

    async def publish(self, event: Any) -> None:
        if self._should_raise is not None:
            raise self._should_raise
        self.published_events.append(event)
