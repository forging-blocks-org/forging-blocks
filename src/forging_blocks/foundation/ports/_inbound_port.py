"""Inbound port contracts — the driving side of hexagonal architecture.

Inbound ports are called *by* infrastructure *into* the application core.
They define the boundary where external actors invoke application logic.
"""

from forging_blocks.foundation.meta.final_meta import runtime_final
from forging_blocks.foundation.ports.helpers._abstract_port_classifier import (
    AbstractPortClassifier,
)
from forging_blocks.foundation.ports.helpers._inbound_dependency_validator import (
    InboundDependencyValidator,
)

from ._port import Port


class InboundPort(Port):
    """ABC for inbound port contracts.

    Responsibilities:
        - Define the driving-side boundary of the application core.
        - Enforce that concrete inbound ports do not depend on other
          inbound ports via ``__init_subclass__`` validation.

    Non-Responsibilities:
        - Does NOT perform structural duck-typing — returns
          ``NotImplemented`` from ``__subclasshook__``.
    """

    @classmethod
    @runtime_final
    def __init_subclass__(cls, /) -> None:
        """ """
        super().__init_subclass__()

        if not AbstractPortClassifier(cls).is_abstract():
            InboundDependencyValidator(cls, target_port=InboundPort).validate()
