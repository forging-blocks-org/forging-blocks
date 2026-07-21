"""Outbound port contracts — the driven side of hexagonal architecture.

Outbound ports are called *by* the application core *out to* infrastructure.
They define the boundary where the application depends on external services.
"""

from forging_blocks.foundation.meta.final_meta import runtime_final
from forging_blocks.foundation.ports.helpers._abstract_port_classifier import (
    AbstractPortClassifier,
)
from forging_blocks.foundation.ports.helpers._outbound_dependency_validator import (
    OutboundDependencyValidator,
)

from ._inbound_port import InboundPort
from ._port import Port


class OutboundPort(Port):
    """ABC for outbound port contracts.

    Responsibilities:
        - Define the driven-side boundary of the application core.
        - Enforce that concrete outbound ports do not depend on inbound
          ports via ``__init_subclass__`` validation.

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
            OutboundDependencyValidator(cls, target_port=InboundPort).validate()
