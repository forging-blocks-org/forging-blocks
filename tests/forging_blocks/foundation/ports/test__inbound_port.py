"""Tests for the InboundPort ABC with dependency-direction enforcement."""

from abc import ABC, abstractmethod

import pytest

from forging_blocks.foundation.ports import InboundPort, OutboundPort


@pytest.mark.unit
class TestInboundPortInitSubclass:
    def test_abstract_intermediate_skips_validation(self) -> None:
        """Abstract intermediates with __abstractmethods__ skip validation."""

        class AbstractUseCase(InboundPort, ABC):
            @abstractmethod
            def execute(self) -> None: ...

        assert AbstractUseCase.__abstractmethods__

    def test_concrete_no_init_passes(self) -> None:
        """Concrete InboundPort without __init__ passes validation."""

        class NoInitUseCase(InboundPort): ...

        assert issubclass(NoInitUseCase, InboundPort)

    def test_concrete_with_outbound_dep_passes(self) -> None:
        """Concrete InboundPort depending on OutboundPort passes validation."""

        class MyRepo(OutboundPort): ...

        class MyUseCase(InboundPort):
            def __init__(self, repo: MyRepo) -> None: ...

        assert issubclass(MyUseCase, InboundPort)

    def test_cannot_override_init_subclass(self) -> None:
        """Overriding __init_subclass__ raises TypeError — it is @runtime_final."""

        with pytest.raises(
            TypeError,
            match="Cannot override runtime-final method '__init_subclass__'",
        ):

            class _(InboundPort):
                def __init_subclass__(cls, /) -> None:
                    pass
