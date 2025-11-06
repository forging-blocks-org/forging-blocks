"""FinalMeta and runtime_final decorators.

This module provides runtime enforcement for methods marked as `@runtime_final`.
It complements the static `@final` decorator from `typing` by preventing
subclasses from overriding these methods at runtime.
"""

from __future__ import annotations

from typing import Any, Callable, Type, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class FinalMeta(type):
    """Metaclass that enforces runtime immutability of methods marked as `@runtime_final`.

    Any attempt to override a `@runtime_final` method in a subclass raises `TypeError`
    at class creation time.
    """

    def __new__(
        mcls: Type[type],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> type:
        """Prevent overriding of runtime-final methods in subclasses."""
        # Collect all runtime-final methods from base classes and their ancestors
        final_methods: set[str] = {
            attr_name
            for base in bases
            for cls in base.__mro__  # Walk the entire inheritance chain
            for attr_name, attr_value in cls.__dict__.items()
            if getattr(attr_value, "__is_runtime_final__", False)
        }

        # Check for any forbidden overrides in the subclass namespace
        for method_name in final_methods:
            if method_name in namespace:
                raise TypeError(
                    f"Cannot override runtime-final method '{method_name}' in subclass '{name}'."
                )

        return type.__new__(mcls, name, bases, namespace)


def runtime_final(func: F) -> F:
    """Decorator that marks a method as runtime-final and type-hint final.

    Adds both static (`__final__`) and runtime (`__is_runtime_final__`) flags.
    """
    func.__final__ = True  # type: ignore[attr-defined]
    func.__is_runtime_final__ = True  # type: ignore[attr-defined]
    return func
