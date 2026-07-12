"""Tests for the EventStoreBase base class."""

from __future__ import annotations

from forging_blocks.infrastructure.event_stores.event_store_base import EventStoreBase


class TestEventStoreBase:
    """Tests for the EventStoreBase abstract base class."""

    def test_event_store_is_abstract(self) -> None:
        """EventStoreBase should be an abstract base class."""
        assert hasattr(EventStoreBase, "__abstractmethods__")
        assert "append_events" in EventStoreBase.__abstractmethods__
        assert "get_events" in EventStoreBase.__abstractmethods__
        assert "get_current_version" in EventStoreBase.__abstractmethods__
