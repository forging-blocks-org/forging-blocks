"""Tests for the PortReferenceDetector helper.

Targets uncovered line 26 (direct MRO match) alongside the existing paths.
"""

import pytest

from forging_blocks.foundation.ports import Port
from forging_blocks.foundation.ports.helpers._port_reference_detector import (
    PortReferenceDetector,
)


@pytest.mark.unit
class TestPortReferenceDetector:
    # -- Already-covered paths (regression safety) ----------------------------------

    def test_detects_port_in_union(self) -> None:
        """Returns True when a Union contains a Port subtype."""

        class MyPort(Port[None, None]): ...

        detector = PortReferenceDetector(Port)
        assert detector.detects_in(MyPort | int) is True

    def test_no_port_in_union(self) -> None:
        """Returns False when no element in the Union is a Port subtype."""

        detector = PortReferenceDetector(Port)
        assert detector.detects_in(int | str) is False

    # -- Uncovered path: direct type in MRO (line 26) -------------------------------

    def test_detects_direct_subclass_in_mro(self) -> None:
        """Returns True when parameter type is a direct subclass of the target port."""

        class MyPort(Port[None, None]): ...

        detector = PortReferenceDetector(Port)
        assert detector.detects_in(MyPort) is True

    def test_no_match_for_unrelated_class(self) -> None:
        """Returns False when parameter type is not a port subclass."""

        detector = PortReferenceDetector(Port)
        assert detector.detects_in(int) is False

    # -- Uncovered path: parameterised generic containing a port (line 29) ---------

    def test_detects_port_inside_parameterized_generic(self) -> None:
        """Returns True when a list[...] wraps a Port subtype (line 29)."""

        class MyPort(Port[None, None]): ...

        detector = PortReferenceDetector(Port)
        assert detector.detects_in(list[MyPort]) is True

    def test_no_port_in_parameterized_generic(self) -> None:
        """Returns False when a list[...] wraps a non-Port type."""

        detector = PortReferenceDetector(Port)
        assert detector.detects_in(list[int]) is False
