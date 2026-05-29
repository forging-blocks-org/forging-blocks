"""FinalABCMeta metaclass.

Combines :class:`FinalMeta` runtime-final enforcement with
:class:`ABCMeta` abstract-base-class support into a single metaclass.
"""

from __future__ import annotations

from abc import ABCMeta

from .final_meta import FinalMeta


class FinalABCMeta(FinalMeta, ABCMeta):
    """Metaclass combining :class:`FinalMeta` and :class:`ABCMeta`.

    Enables both abstract base class functionality via :class:`ABCMeta`
    and runtime enforcement of methods decorated with :func:`runtime_final`.

    Usage::

        class MyBase(metaclass=FinalABCMeta):
            @runtime_final
            def sealed_method(self) -> None:
                ...

            @abstractmethod
            def abstract_method(self) -> None:
                ...
    """
