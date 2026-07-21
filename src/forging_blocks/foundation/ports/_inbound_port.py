"""ABC for inbound port contracts (use cases, application services).

At class-definition time, concrete subclasses are validated: their
``__init__`` parameters must not reference any ``InboundPort`` type.
"""

from abc import ABC

from forging_blocks.foundation.ports.helpers._abstract_port_classifier import (
    AbstractPortClassifier,
)
from forging_blocks.foundation.ports.helpers._inbound_dependency_validator import (
    InboundDependencyValidator,
)

from ._port import Port


class InboundPort[InputType, OutputType](Port[InputType, OutputType], ABC):
    """ABC for inbound port contracts (use cases, application services).

    Non-Responsibilities:
        - Does NOT perform structural duck-typing — returns
          ``NotImplemented`` from ``__subclasshook__``.
    """

    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return NotImplemented

    def __init_subclass__(cls, /) -> None:
        super().__init_subclass__()
        if not AbstractPortClassifier(cls).is_abstract() and "__init__" in cls.__dict__:
            InboundDependencyValidator(cls, target_port=InboundPort).validate()
