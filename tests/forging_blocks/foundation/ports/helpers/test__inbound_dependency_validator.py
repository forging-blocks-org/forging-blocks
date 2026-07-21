"""Tests for the InboundDependencyValidator helper.

Targets the ArchitectureError raise path (line 30).
"""

import pytest

from forging_blocks.foundation.errors.architecture_error import ArchitectureError
from forging_blocks.foundation.ports import InboundPort, OutboundPort
from forging_blocks.foundation.ports.helpers._inbound_dependency_validator import (
    InboundDependencyValidator,
)


@pytest.mark.unit
class TestInboundDependencyValidator:
    def test_validate_passes_for_outbound_dependency(self) -> None:
        """Concrete InboundPort with only OutboundPort deps passes validation."""

        class Repo(OutboundPort): ...

        class UseCase(InboundPort):
            def __init__(self, repo: Repo) -> None: ...

        InboundDependencyValidator(UseCase, target_port=InboundPort).validate()

    def test_validate_raises_for_inbound_dependency(self) -> None:
        """Concrete InboundPort depending on InboundPort raises ArchitectureError (line 30)."""

        class BadInbound(InboundPort): ...

        with pytest.raises(ArchitectureError) as exc_info:

            class _(InboundPort):
                def __init__(self, dep: BadInbound) -> None: ...

        assert "_" in str(exc_info.value)
