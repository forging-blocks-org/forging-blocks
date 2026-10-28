"""FinalABCMeta metaclass.

Combines `FinalMeta` runtime-final enforcement with
`ABCMeta` abstract-base-class support into a single metaclass.
"""

from abc import ABCMeta
from typing import Any

from .final_meta import FinalMeta, validate_no_runtime_final_override


class FinalABCMeta(FinalMeta, ABCMeta):
    """Metaclass combining `FinalMeta` and `ABCMeta`.

    Enables both abstract base class functionality via `ABCMeta`
    and runtime enforcement of methods decorated with `runtime_final`.

    Example:
        ```python
        def runtime_final(fn):
            return fn


        def abstractmethod(fn):
            return fn


        class MyBase(metaclass=FinalABCMeta):
            @runtime_final
            def sealed_method(self) -> None: ...

            @abstractmethod
            def abstract_method(self) -> None: ...
        ```

    """

    def __new__(
        mcls: type[Any],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> type[Any]:
        """Enforce runtime-final checks then delegate to ABCMeta for abstract collection."""
        validate_no_runtime_final_override(name, bases, namespace)
        return ABCMeta.__new__(mcls, name, bases, namespace, **kwargs)
