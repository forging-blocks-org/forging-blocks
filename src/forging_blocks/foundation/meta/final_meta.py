"""FinalMeta and runtime_final decorators.

This module provides runtime enforcement for methods marked as `@runtime_final`.
It complements the static `@final` decorator from `typing` by preventing
subclasses from overriding these methods at runtime.
"""

from collections.abc import Callable
from typing import Any, cast


def _unwrap_descriptor(attr_value: object) -> object:
    """Unwrap ``classmethod`` / ``staticmethod`` to the underlying function."""
    try:
        return object.__getattribute__(attr_value, "__func__")
    except AttributeError:
        return attr_value


def validate_no_runtime_final_override(
    name: str,
    bases: tuple[type, ...],
    namespace: dict[str, Any],
) -> None:
    """Check that no subclass overrides a @runtime_final method.

    Raised at class creation time (inside metaclass ``__new__``) so the
    violation is caught immediately, before any instance is created.
    """
    final_methods: set[str] = {
        attr_name
        for base in bases
        for cls in base.__mro__
        for attr_name, attr_value in cls.__dict__.items()
        if getattr(_unwrap_descriptor(attr_value), "__is_runtime_final__", False)
    }

    for method_name in final_methods:
        if method_name in namespace:
            raise TypeError(
                f"Cannot override runtime-final method '{method_name}' in subclass '{name}'."
            )


class FinalMeta(type):
    """Metaclass that enforces runtime immutability of methods marked as `@runtime_final`.

    Any attempt to override a `@runtime_final` method in a subclass raises `TypeError`
    at class creation time.
    """

    def __new__(
        mcls: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> type:
        """Prevent overriding of runtime-final methods in subclasses."""
        validate_no_runtime_final_override(name, bases, namespace)
        return cast(type, type.__new__(mcls, name, bases, namespace, **kwargs))


type AnyCallable = Callable[..., Any]


def runtime_final[F: AnyCallable](func: F) -> F:
    """Decorator that marks a method as runtime-final and type-hint final.

    Adds both static (`__final__`) and runtime (`__is_runtime_final__`) flags.
    """
    object.__setattr__(func, "__final__", True)
    object.__setattr__(func, "__is_runtime_final__", True)
    return func
