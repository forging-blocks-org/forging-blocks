"""Root marker ABC for all port contracts.

Subclass ``InboundPort`` or ``OutboundPort`` instead of this class
directly — this base class itself enforces no dependency rules.
"""

from abc import ABC


class Port[InputType, OutputType](ABC):  # noqa: B024
    """Root marker ABC for all port contracts.

    Non-Responsibilities:
        - Does NOT perform structural duck-typing — returns
          ``NotImplemented`` from ``__subclasshook__``.
    """

    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return NotImplemented

    # Fixes pyright structural-contract errors from
    # Protocol.__init_subclass__'s (*args, **kwargs) signature.
    def __init_subclass__(cls, /) -> None:
        super().__init_subclass__()
