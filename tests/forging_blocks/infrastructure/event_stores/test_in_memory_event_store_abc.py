"""Tests for the AbstractEventStore base class."""

from __future__ import annotations

from forging_blocks.infrastructure.event_stores.abstract_event_store import AbstractEventStore


class TestAbstractEventStore:
    """Tests for the AbstractEventStore abstract base class."""

    def test_event_store_is_abstract(self) -> None:
        """AbstractEventStore should be an abstract base class."""
        assert hasattr(AbstractEventStore, "__abstractmethods__")
        assert "append_events" in AbstractEventStore.__abstractmethods__
        assert "get_events" in AbstractEventStore.__abstractmethods__
        assert "get_current_version" in AbstractEventStore.__abstractmethods__
