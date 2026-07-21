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

        class Repo(OutboundPort[None, None]): ...

        class UseCase(InboundPort[None, None]):
            def __init__(self, repo: Repo) -> None: ...

        InboundDependencyValidator(UseCase, target_port=InboundPort).validate()

    def test_validate_raises_for_inbound_dependency(self) -> None:
        """Concrete InboundPort depending on InboundPort raises ArchitectureError (line 30)."""

        class BadInbound(InboundPort[None, None]): ...

        with pytest.raises(ArchitectureError) as exc_info:

            class BadUseCase(InboundPort[None, None]):
                def __init__(self, dep: BadInbound) -> None: ...

        assert "BadUseCase" in str(exc_info.value)
