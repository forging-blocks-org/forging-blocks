"""Tests for the OutboundPort ABC with dependency-direction enforcement."""

from abc import ABC, abstractmethod

import pytest

from forging_blocks.foundation.ports import InboundPort, OutboundPort


@pytest.mark.unit
class TestOutboundPortSubclasshook:
    def test_returns_not_implemented(self) -> None:
        """__subclasshook__ returns NotImplemented so structural checks defer."""
        assert OutboundPort.__subclasshook__(int) is NotImplemented


@pytest.mark.unit
class TestOutboundPortInitSubclass:
    def test_abstract_intermediate_skips_validation(self) -> None:
        """Abstract intermediates with __abstractmethods__ skip validation."""

        class AbstractRepo(OutboundPort[None, None], ABC):
            @abstractmethod
            def save(self) -> None: ...

        assert AbstractRepo.__abstractmethods__

    def test_concrete_no_init_passes(self) -> None:
        """Concrete OutboundPort without __init__ passes validation."""

        class NoInitRepo(OutboundPort[None, None]): ...

        assert issubclass(NoInitRepo, OutboundPort)

    def test_concrete_with_outbound_dep_passes(self) -> None:
        """Concrete OutboundPort depending on another OutboundPort passes."""

        class Logger(OutboundPort[None, None]): ...

        class MyRepo(OutboundPort[None, None]):
            def __init__(self, logger: Logger) -> None: ...

        assert issubclass(MyRepo, OutboundPort)

    def test_outbound_depending_on_inbound_raises(self) -> None:
        """Concrete OutboundPort depending on an InboundPort raises ArchitectureError."""

        from forging_blocks.foundation.errors.architecture_error import ArchitectureError

        class BadHandler(InboundPort[None, None]): ...

        with pytest.raises(ArchitectureError):

            class BadRepo(OutboundPort[None, None]):
                def __init__(self, handler: BadHandler) -> None: ...
