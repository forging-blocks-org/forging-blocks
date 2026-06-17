"""FinalABCMeta metaclass.

Combines `FinalMeta` runtime-final enforcement with
`ABCMeta` abstract-base-class support into a single metaclass.
"""

from abc import ABCMeta
from typing import Any, Type

from .final_meta import FinalMeta, validate_no_runtime_final_override


class FinalABCMeta(FinalMeta, ABCMeta):
    """Metaclass combining `FinalMeta` and `ABCMeta`.

    Enables both abstract base class functionality via `ABCMeta`
    and runtime enforcement of methods decorated with :func:`runtime_final`.

    Usage::

        class MyBase(metaclass=FinalABCMeta):
            @runtime_final
            def sealed_method(self) -> None: ...

            @abstractmethod
            def abstract_method(self) -> None: ...
    """

    def __new__(
        mcls: Type[type],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> type:
        """Enforce runtime-final checks then delegate to ABCMeta for abstract collection."""
        validate_no_runtime_final_override(name, bases, namespace)
        return ABCMeta.__new__(mcls, name, bases, namespace, **kwargs)
