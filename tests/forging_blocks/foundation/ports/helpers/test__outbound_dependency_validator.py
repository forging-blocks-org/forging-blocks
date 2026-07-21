"""Tests for the OutboundDependencyValidator helper.

Targets the ArchitectureError raise path (line 30).
"""

import pytest

from forging_blocks.foundation.errors.architecture_error import ArchitectureError
from forging_blocks.foundation.ports import InboundPort, OutboundPort
from forging_blocks.foundation.ports.helpers._outbound_dependency_validator import (
    OutboundDependencyValidator,
)


@pytest.mark.unit
class TestOutboundDependencyValidator:
    def test_validate_passes_for_outbound_dependency(self) -> None:
        """Concrete OutboundPort with only OutboundPort deps passes validation."""

        class Logger(OutboundPort): ...

        class Repo(OutboundPort):
            def __init__(self, logger: Logger) -> None: ...

        OutboundDependencyValidator(Repo, target_port=InboundPort).validate()

    def test_validate_raises_for_inbound_dependency(self) -> None:
        """OutboundPort depending on InboundPort raises ArchitectureError (line 30)."""

        class BadInbound(InboundPort): ...

        with pytest.raises(ArchitectureError) as exc_info:

            class _(OutboundPort):
                def __init__(self, dep: BadInbound) -> None: ...

        assert "_" in str(exc_info.value)
