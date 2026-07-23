"""Contract tests for EventPublisherPort.

These tests verify that a concrete implementation of ``EventPublisherPort``
correctly exposes the ``publish`` contract.  The port itself declares an
``@abstractmethod`` — the ``FakeEventPublisher`` fixture provides a real
implementation so tests exercise behaviour, not mock expectations.
"""

from __future__ import annotations

from typing import Self

import pytest

from forging_blocks.application import EventPublisherPort
from forging_blocks.foundation import OutboundPort
from forging_blocks.foundation.messages import Event, MessageMetadata


class FakeEvent(Event[str]):
    @property
    def value(self) -> str:
        return "baz"

    @property
    def _payload(self) -> dict[str, object]:
        return {"foo": "bar"}

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls()


class FakeEventPublisher(EventPublisherPort[str]):
    """Concrete fixture that implements ``publish`` and records published events."""

    def __init__(self) -> None:
        self.published: list[Event[str]] = []

    async def publish(self, event: Event[str]) -> None:
        self.published.append(event)


@pytest.mark.unit
class TestEventPublisherPortContract:
    """Any object with an async ``publish`` accepting an ``Event`` satisfies this port."""

    def test_fake_publisher_is_instance_of_outbound_port(self) -> None:
        """Concrete implementation passes structural isinstance checks."""
        publisher = FakeEventPublisher()
        assert isinstance(publisher, OutboundPort)
        assert isinstance(publisher, EventPublisherPort)

    async def test_publish_dispatches_event_to_fixture(self) -> None:
        """The concrete publisher records the event it receives."""
        publisher = FakeEventPublisher()
        event = FakeEvent()

        await publisher.publish(event)

        assert event in publisher.published
        assert len(publisher.published) == 1
