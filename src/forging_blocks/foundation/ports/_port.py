"""Abstract base class for the port hierarchy.

Defines the root ``Port`` class, which all ports ultimately inherit from.
Application code should subclass ``InboundPort`` or ``OutboundPort``
instead of ``Port`` directly, as ``Port`` itself enforces no
dependency-direction rules.
"""

from abc import ABC, abstractmethod

from forging_blocks.foundation.meta.final_abc_meta import FinalABCMeta


class Port(ABC, metaclass=FinalABCMeta):
    """Root abstract base class for all port contracts.
    Responsibilities:
        - Serve as the root abstract base for all port contracts.
        - Define the contract that ``InboundPort`` and ``OutboundPort``
          concretize.

    Non-Responsibilities:
        - Does NOT enforce dependency-direction rules — that is delegated
          to ``InboundPort`` and ``OutboundPort`` via ``__init_subclass__``.
    """

    @classmethod
    @abstractmethod
    def __init_subclass__(cls, /) -> None:
        super().__init_subclass__()
