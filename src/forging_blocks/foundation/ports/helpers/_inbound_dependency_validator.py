"""Validate that an InboundPort does not depend on other InboundPorts.

Raised at class-definition time via ``InboundPort.__init_subclass__``.
"""

from forging_blocks.foundation.errors.architecture_error import ArchitectureError

from ._init_parameter_extractor import InitParameterExtractor
from ._port_reference_detector import PortReferenceDetector


class InboundDependencyValidator:
    """Validates that an InboundPort's ``__init__`` parameters follow
    the architectural rule: InboundPorts may only depend on OutboundPorts.
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
                    f"{self._cls.__qualname__} is an InboundPort but depends on "
                    f"{parameter_type!r} (an InboundPort) via parameter "
                    f"'{parameter_name}'. InboundPorts may only depend on "
                    f"OutboundPort instances."
                )
