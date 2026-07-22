"""Architecture error for dependency direction violations.

Defines ``ArchitectureError``, raised at class-definition time when a port
subclass violates Clean Architecture dependency rules.
"""

from collections.abc import Mapping

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error


class ArchitectureError(Error[Mapping[str, object]]):
    """Raised when a port subclass violates dependency direction rules.

    Inbound ports may only depend on OutboundPort instances; Outbound ports
    may only depend on other OutboundPort instances. This error fires at
    class creation time via ``__init_subclass__`` on ``InboundPort`` and
    ``OutboundPort``.
    """

    def __init__(self, message: str) -> None:
        """Initialise with a descriptive violation message.

        Args:
            message: Human-readable description of the violation,
                including the class name, the offending parameter,
                and the applicable rule.
        """
        super().__init__(ErrorMessage(message))
