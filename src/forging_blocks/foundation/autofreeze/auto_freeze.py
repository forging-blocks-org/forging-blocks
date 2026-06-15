"""Auto-freeze decorator for enforcing immutability on class instances.

Provides the :func:`auto_freeze` decorator that automatically freezes instances
after ``__init__`` completes. The decorator injects a frozen state marker and
a ``__setattr__`` override to prevent attribute modifications.

Can be used as ``@auto_freeze``, ``@auto_freeze()``, or
``@auto_freeze(attrs=[...])`` for selective freezing.

Useful for: Entities, value objects, and any domain type that
should be immutable after construction.

Example:
    ```python
    from forging_blocks.foundation.autofreeze import auto_freeze
    from forging_blocks.foundation.errors import CantModifyImmutableAttributeError


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

    With selective freezing (e.g., for Entities):
    ```python
    @auto_freeze(attrs=["_id"])
    class User:
        def __init__(self, user_id: str, name: str) -> None:
            self._id = user_id
            self._name = name

        @property
        def id(self) -> str:
            return self._id

        @property
        def name(self) -> str:
            return self._name
    ```
"""

from __future__ import annotations

import inspect
from collections.abc import Callable, Sequence
from functools import wraps
from typing import Any, overload

from forging_blocks.foundation.errors.cant_modify_immutable_attribute_error import (
    CantModifyImmutableAttributeError,
)

_AUTO_FREEZE_MARKER = "__auto_freeze_applied"
_FROZEN_FLAG = "_autofreeze__frozen"
_FROZEN_ATTRS_FLAG = "_autofreeze__frozen_attrs"
_INIT_DEPTH_FLAG = "_autofreeze__init_depth"


class _AutoFreezeDecorator:
    """Callable class that applies auto-freeze behaviour to a target class.

    Injects a ``__setattr__`` that prevents modifications to frozen attributes.
    No protocol implementation is required on the target class.
    """

    def __init__(
        self,
        *,
        attrs: Sequence[str] | None = None,
    ) -> None:
        """Initialise the decorator with optional selective-freeze attributes.

        Args:
            attrs: Attribute names to selectively freeze. When ``None``
                (the default), the entire instance is frozen. When provided,
                only those attributes are frozen.
        """
        self._attrs = attrs

    def __call__[T](self, class_: type[T]) -> type[T]:
        """Apply the auto-freeze behaviour to *class_*.

        Injects a frozen state marker and wraps ``__setattr__`` to enforce
        immutability. If *class_* has already been decorated (detected via
        an internal marker), returns the class unchanged to avoid double-wrapping.

        Args:
            class_: The target class to decorate.

        Returns:
            The decorated class (may be the original if already decorated).
        """
        if hasattr(class_.__init__, _AUTO_FREEZE_MARKER):
            return class_

        original_init = class_.__init__
        attrs = self._attrs

        original_setattr = class_.__setattr__
        has_custom_setattr = original_setattr is not object.__setattr__

        @wraps(original_init)
        def wrapped_init(
            instance: Any,
            *args: Any,
            **kwargs: Any,
        ) -> None:
            init_depth = getattr(instance, _INIT_DEPTH_FLAG, 0)
            object.__setattr__(instance, _INIT_DEPTH_FLAG, init_depth + 1)

            try:
                original_init(instance, *args, **kwargs)
            finally:
                new_depth = getattr(instance, _INIT_DEPTH_FLAG, 1) - 1
                if new_depth <= 0:
                    object.__delattr__(instance, _INIT_DEPTH_FLAG)
                else:
                    object.__setattr__(instance, _INIT_DEPTH_FLAG, new_depth)

                if new_depth == 0 and not inspect.isabstract(class_):
                    if attrs is None:
                        object.__setattr__(instance, _FROZEN_FLAG, True)
                    else:
                        object.__setattr__(instance, _FROZEN_ATTRS_FLAG, set(attrs))

        object.__setattr__(wrapped_init, _AUTO_FREEZE_MARKER, True)
        class_.__init__ = wrapped_init  # type: ignore[method-assign]

        if not has_custom_setattr:

            def frozen_setattr(instance: Any, name: str, value: Any) -> None:
                # Check for full freeze
                if getattr(instance, _FROZEN_FLAG, False):
                    raise CantModifyImmutableAttributeError(
                        class_name=instance.__class__.__name__,
                        attribute_name=name,
                    )

                frozen_attrs = getattr(instance, _FROZEN_ATTRS_FLAG, None)
                if frozen_attrs is not None and name in frozen_attrs:
                    raise CantModifyImmutableAttributeError(
                        class_name=instance.__class__.__name__,
                        attribute_name=name,
                    )

                object.__setattr__(instance, name, value)

            class_.__setattr__ = frozen_setattr  # type: ignore[method-assign]

        return class_


@overload
def auto_freeze[T](class_: type[T]) -> type[T]: ...


@overload
def auto_freeze[T](
    class_: type[T],
    *,
    attrs: Sequence[str] | None = None,
) -> type[T]: ...


@overload
def auto_freeze[T](
    class_: None = None,
    *,
    attrs: Sequence[str] | None = None,
) -> Callable[[type[T]], type[T]]: ...


def auto_freeze[T](
    class_: type[T] | None = None,
    *,
    attrs: Sequence[str] | None = None,
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

    Returns:
        The decorated class if *class_* is provided; otherwise a callable
        that can be used as a decorator.
    """
    decorator = _AutoFreezeDecorator(attrs=attrs)

    if class_ is not None:
        return decorator(class_)

    return decorator
