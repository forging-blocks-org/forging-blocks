"""FinalABCMeta metaclass.

Combines :class:`FinalMeta` runtime-final enforcement with
:class:`ABCMeta` abstract-base-class support into a single metaclass.
"""

from __future__ import annotations

from abc import ABCMeta
from typing import Any, Type

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

    def __new__(
        mcls: Type[type],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> type:
        """Enforce runtime-final checks then delegate to ABCMeta for abstract collection."""
        # Collect all runtime-final methods from base classes and their ancestors
        final_methods: set[str] = {
            attr_name
            for base in bases
            for cls in base.__mro__
            for attr_name, attr_value in cls.__dict__.items()
            if getattr(attr_value, "__is_runtime_final__", False)
        }

        # Check for any forbidden overrides in the subclass namespace
        for method_name in final_methods:
            if method_name in namespace:
                raise TypeError(
                    f"Cannot override runtime-final method '{method_name}' in subclass '{name}'."
                )

        # Delegate to ABCMeta.__new__ so __abstractmethods__ is collected
        return ABCMeta.__new__(mcls, name, bases, namespace, **kwargs)
