"""Validate that an OutboundPort does not depend on InboundPorts.

Raised at class-definition time via ``OutboundPort.__init_subclass__``.
"""

from forging_blocks.foundation.errors.architecture_error import ArchitectureError

from ._init_parameter_extractor import InitParameterExtractor
from ._port_reference_detector import PortReferenceDetector


class OutboundDependencyValidator:
    """Validates that an OutboundPort's ``__init__`` parameters follow
    the architectural rule: OutboundPorts may only depend on other OutboundPorts.
    """

    def __init__(self, cls: type, *, target_port: type) -> None:
        self._cls = cls
        self._target_port = target_port

    def validate(self) -> None:
        """Raise ``ArchitectureError`` if any parameter references an InboundPort."""
        parameters = InitParameterExtractor(self._cls).extract()
        detector = PortReferenceDetector(self._target_port)

        for parameter_name, parameter_type in parameters.items():
            if detector.detects_in(parameter_type):
                raise ArchitectureError(
                    f"{self._cls.__qualname__} is an OutboundPort but depends on "
                    f"{parameter_type!r} (an InboundPort) via parameter "
                    f"'{parameter_name}'. OutboundPorts may only depend on other "
                    f"OutboundPort instances."
                )
