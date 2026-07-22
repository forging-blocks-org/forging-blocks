"""Tests for the Port root marker ABC."""

from abc import ABC

import pytest

from forging_blocks.foundation.ports import Port


@pytest.mark.unit
class TestPortInitSubclass:
    def test_concrete_subclass_creates_without_error(self) -> None:
        """A concrete Port subclass validates without error."""

        class MyPort(Port): ...

        assert issubclass(MyPort, Port)

    def test_abstract_subclass_creates_without_error(self) -> None:
        """An abstract Port subclass validates without error."""

        class AbstractPort(Port, ABC): ...

        assert issubclass(AbstractPort, Port)
