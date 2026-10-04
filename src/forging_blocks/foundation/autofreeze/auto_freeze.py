"""Auto-freeze decorator for enforcing immutability on class instances.

Provides the `auto_freeze` decorator that automatically freezes instances
after ``__init__`` completes. The decorator injects frozen state markers and
``__setattr__``/``__delattr__`` overrides to prevent attribute modifications.

Can be used as ``@auto_freeze``, ``@auto_freeze()``, or
``@auto_freeze(attrs=[...])`` for selective freezing.

Useful for: Immutable data types and any class that
should be immutable after construction.

Example:
    ```python
    @auto_freeze
    class Money:
        def __init__(self, amount: int, currency: str) -> None:
            if amount < 0:
                raise ValueError("Amount cannot be negative")
            self._amount = amount
            self._currency = currency.upper()

        @property
        def amount(self) -> int:
            return self._amount

        @property
        def currency(self) -> str:
            return self._currency
    ```

    With selective freezing:
    ```python
    @auto_freeze(attrs=["_key"])
    class CacheEntry:
        def __init__(self, key: str, value: str) -> None:
            self._key = key
            self._value = value

        @property
        def key(self) -> str:
            return self._key

        @property
        def value(self) -> str:
            return self._value
    ```

"""

from collections.abc import Callable, Sequence
from typing import overload

from forging_blocks.foundation.autofreeze.helpers._auto_freeze_decorator import (
    AutoFreezeDecorator as _AutoFreezeDecorator,
)


@overload
def auto_freeze[T](class_: type[T]) -> type[T]: ...


@overload
def auto_freeze[T](
    class_: type[T],
    *,
    attrs: Sequence[str] | None = None,
    custom_mutator_attrs: Sequence[str] | None = None,
) -> type[T]: ...


@overload
def auto_freeze[T](
    class_: None = None,
    *,
    attrs: Sequence[str] | None = None,
    custom_mutator_attrs: Sequence[str] | None = None,
) -> Callable[[type[T]], type[T]]: ...


def auto_freeze[T](
    class_: type[T] | None = None,
    *,
    attrs: Sequence[str] | None = None,
    custom_mutator_attrs: Sequence[str] | None = None,
) -> type[T] | Callable[[type[T]], type[T]]:
    """Automatically freeze class instances after ``__init__`` completes.

    Can be used as ``@auto_freeze``, ``@auto_freeze()``, or
    ``@auto_freeze(attrs=[...])``. No protocol implementation is required
    on the target class - the decorator handles freezing internally.

    Args:
        class_: The target class (when used directly as ``@auto_freeze``).
            ``None`` when used with parentheses (``@auto_freeze()``).
        attrs: Optional attribute names for selective freezing. If ``None``,
            the whole instance is frozen. When provided, only those attributes
            are frozen.
        custom_mutator_attrs: Attributes whose existing custom mutators own
            domain-specific validation before generic freeze checks. This is
            an internal policy used by domain types such as ``Entity``.

    Returns:
        The decorated class if *class_* is provided; otherwise a callable
        that can be used as a decorator.

    """
    decorator = _AutoFreezeDecorator(
        attrs=attrs,
        custom_mutator_attrs=custom_mutator_attrs,
    )

    if class_ is not None:
        return decorator(class_)

    return decorator
