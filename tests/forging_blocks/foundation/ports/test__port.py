"""Tests for the Port root marker ABC."""

from abc import ABC

import pytest

from forging_blocks.foundation.ports import Port


@pytest.mark.unit
class TestPortSubclasshook:
    def test_returns_not_implemented(self) -> None:
        """__subclasshook__ returns NotImplemented so structural checks defer."""
        assert Port.__subclasshook__(int) is NotImplemented

    def test_issubclass_defers_to_default(self) -> None:
        """issubclass() uses default mechanism when __subclasshook__ returns NotImplemented."""
        assert not issubclass(int, Port)


@pytest.mark.unit
class TestPortInitSubclass:
    def test_concrete_subclass_creates_without_error(self) -> None:
        """A concrete Port subclass validates without error."""

        class MyPort(Port[None, None]): ...

        assert issubclass(MyPort, Port)

    def test_abstract_subclass_creates_without_error(self) -> None:
        """An abstract Port subclass validates without error."""

        class AbstractPort(Port[None, None], ABC): ...

        assert issubclass(AbstractPort, Port)
