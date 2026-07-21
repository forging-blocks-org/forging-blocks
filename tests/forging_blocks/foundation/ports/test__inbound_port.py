"""Tests for the InboundPort ABC with dependency-direction enforcement."""

from abc import ABC, abstractmethod

import pytest

from forging_blocks.foundation.ports import InboundPort, OutboundPort


@pytest.mark.unit
class TestInboundPortSubclasshook:
    def test_returns_not_implemented(self) -> None:
        """__subclasshook__ returns NotImplemented so structural checks defer."""
        assert InboundPort.__subclasshook__(int) is NotImplemented


@pytest.mark.unit
class TestInboundPortInitSubclass:
    def test_abstract_intermediate_skips_validation(self) -> None:
        """Abstract intermediates with __abstractmethods__ skip validation."""

        class AbstractUseCase(InboundPort[None, None], ABC):
            @abstractmethod
            def execute(self) -> None: ...

        assert AbstractUseCase.__abstractmethods__

    def test_concrete_no_init_passes(self) -> None:
        """Concrete InboundPort without __init__ passes validation."""

        class NoInitUseCase(InboundPort[None, None]): ...

        assert issubclass(NoInitUseCase, InboundPort)

    def test_concrete_with_outbound_dep_passes(self) -> None:
        """Concrete InboundPort depending on OutboundPort passes validation."""

        class MyRepo(OutboundPort[None, None]): ...

        class MyUseCase(InboundPort[None, None]):
            def __init__(self, repo: MyRepo) -> None: ...

        assert issubclass(MyUseCase, InboundPort)
