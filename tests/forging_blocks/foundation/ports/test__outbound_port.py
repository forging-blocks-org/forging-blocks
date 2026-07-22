"""Tests for the OutboundPort ABC with dependency-direction enforcement."""

from abc import ABC, abstractmethod

import pytest

from forging_blocks.foundation.ports import InboundPort, OutboundPort


@pytest.mark.unit
class TestOutboundPortInitSubclass:
    def test_abstract_intermediate_skips_validation(self) -> None:
        """Abstract intermediates with __abstractmethods__ skip validation."""

        class AbstractRepo(OutboundPort, ABC):
            @abstractmethod
            def save(self) -> None: ...

        assert AbstractRepo.__abstractmethods__

    def test_concrete_no_init_passes(self) -> None:
        """Concrete OutboundPort without __init__ passes validation."""

        class NoInitRepo(OutboundPort): ...

        assert issubclass(NoInitRepo, OutboundPort)

    def test_concrete_with_outbound_dep_passes(self) -> None:
        """Concrete OutboundPort depending on another OutboundPort passes."""

        class Logger(OutboundPort): ...

        class MyRepo(OutboundPort):
            def __init__(self, logger: Logger) -> None: ...

        assert issubclass(MyRepo, OutboundPort)

    def test_outbound_depending_on_inbound_raises(self) -> None:
        """Concrete OutboundPort depending on an InboundPort raises ArchitectureError."""

        from forging_blocks.foundation.errors.architecture_error import ArchitectureError

        class BadHandler(InboundPort): ...

        with pytest.raises(ArchitectureError):

            class _(OutboundPort):
                def __init__(self, handler: BadHandler) -> None: ...

    def test_cannot_override_init_subclass(self) -> None:
        """Overriding __init_subclass__ raises TypeError — it is @runtime_final."""

        with pytest.raises(
            TypeError,
            match="Cannot override runtime-final method '__init_subclass__'",
        ):

            class _(OutboundPort):
                def __init_subclass__(cls, /) -> None:
                    pass
