"""Auto-freeze decorator for enforcing immutability on class instances.

Provides the `auto_freeze` decorator that automatically freezes instances
after ``__init__`` completes. The decorator injects a frozen state marker and
a ``__setattr__`` override to prevent attribute modifications.

Can be used as ``@auto_freeze``, ``@auto_freeze()``, or
``@auto_freeze(attrs=[...])`` for selective freezing.

Useful for: Value objects, immutable data types, and any class that
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

    With selective freezing:
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

from collections.abc import Callable, Sequence
from typing import overload

from forging_blocks.foundation.autofreeze.helpers.frozen_init_wrapper import (
    FrozenInitWrapper,
)
from forging_blocks.foundation.autofreeze.helpers.frozen_setattr_handler import (
    FrozenSetattrHandler,
)
from forging_blocks.foundation.autofreeze.helpers.frozen_state import (
    FrozenStateManager,
)


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
        if FrozenStateManager.is_decorated(class_.__init__):
            return class_

        init_wrapper = FrozenInitWrapper(class_.__init__, class_, self._attrs)
        class_.__init__ = init_wrapper.wrap()

        setattr_handler = FrozenSetattrHandler(class_)
        if setattr_handler.should_override_setattr():
            class_.__setattr__ = setattr_handler.create_frozen_setattr()

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
