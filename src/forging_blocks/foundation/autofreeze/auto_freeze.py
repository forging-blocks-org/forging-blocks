"""Auto-freeze decorator for enforcing immutability on class instances.

Provides the :func:`auto_freeze` decorator that automatically freezes instances
after ``__init__`` completes. Classes decorated with ``@auto_freeze`` must satisfy
:class:`~forging_blocks.foundation.autofreeze.SupportsAutoFreeze` (i.e. implement
:meth:`freeze_instance` and optionally :meth:`freeze_attributes`). The decorator
injects a wrapper around ``__init__`` that calls the freezing protocol at the
end of construction.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from functools import wraps
from typing import Any, overload

_AUTO_FREEZE_MARKER = "__auto_freeze_applied"


class _AutoFreezeDecorator:
    """Callable class that applies auto-freeze behaviour to a target class.

    Validates that the target implements the :class:`SupportsAutoFreeze` protocol,
    then wraps its ``__init__`` so that :meth:`freeze_instance` (or selectively
    :meth:`freeze_attributes`) is called at the end of construction.
    """

    def __init__(
        self,
        *,
        attrs: Sequence[str] | None = None,
    ) -> None:
        """Initialise the decorator with optional selective-freeze attributes.

        Args:
            attrs: Attribute names to selectively freeze. When ``None``
                (the default), the entire instance is frozen via
                :meth:`freeze_instance`. When provided, only those
                attributes are frozen via :meth:`freeze_attributes`.
        """
        self._attrs = attrs

    def __call__[T](self, class_: type[T]) -> type[T]:
        """Apply the auto-freeze behaviour to *class_*.

        Validates the protocol contract on *class_*, then replaces
        ``__init__`` with a wrapper that calls the freeze protocol after
        the original initialiser runs. If *class_* has already been
        decorated (detected via an internal marker), returns the class
        unchanged to avoid double-wrapping.

        Args:
            class_: The target class to decorate.

        Returns:
            The decorated class (may be the original if already decorated).

        Raises:
            TypeError: If *class_* does not implement the required
                :class:`SupportsAutoFreeze` protocol methods.
        """
        self._validate_protocol(class_)

        if hasattr(class_.__init__, _AUTO_FREEZE_MARKER):
            return class_

        original_init = class_.__init__
        attrs = self._attrs

        @wraps(original_init)
        def wrapped_init(
            instance: Any,
            *args: Any,
            **kwargs: Any,
        ) -> None:
            original_init(instance, *args, **kwargs)

            if attrs is None:
                instance.freeze_instance()
            else:
                instance.freeze_attributes(attrs)

        object.__setattr__(wrapped_init, _AUTO_FREEZE_MARKER, True)

        class_.__init__ = wrapped_init  # type: ignore[method-assign]

        return class_

    @staticmethod
    def _validate_protocol[T](class_: type[T]) -> None:
        """Verify that *class_* implements the :class:`SupportsAutoFreeze` protocol.

        Checks for the presence of the required methods:
        :meth:`freeze_instance` and optionally :meth:`freeze_attributes`.

        Args:
            class_: The class to validate.

        Raises:
            TypeError: If any required protocol method is missing.
        """
        if not hasattr(class_, "freeze_instance"):
            raise TypeError(
                f"{class_.__name__} does not implement SupportsAutoFreeze protocol.\n"
                f"Missing: freeze_instance"
            )


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
    ``@auto_freeze(attrs=[...])``. The decorated class must implement
    :class:`~forging_blocks.foundation.autofreeze.SupportsAutoFreeze`.

    Useful for: Entities, value objects, and any domain type that
    should be immutable after construction.

    Args:
        class_: The target class (when used directly as ``@auto_freeze``).
            ``None`` when used with parentheses (``@auto_freeze()``).
        attrs: Optional attribute names for selective freezing. If ``None``,
            the whole instance is frozen via :meth:`freeze_instance`. When
            provided, only those attributes are frozen via
            :meth:`freeze_attributes`.

    Returns:
        The decorated class if *class_* is provided; otherwise a callable
        that can be used as a decorator.

    Raises:
        TypeError: If the target class does not implement the required
            protocol methods (``freeze_instance``).

    Example:

        ```python
        from forging_blocks.foundation.autofreeze import auto_freeze
        from forging_blocks.foundation.errors import (
            CantModifyImmutableAttributeError,
        )


        @auto_freeze
        class Money:
            def __init__(self, amount: int, currency: str) -> None:
                if amount < 0:
                    raise ValueError("Amount cannot be negative")
                self._amount = amount
                self._currency = currency

            def freeze_instance(self) -> None:
                object.__setattr__(self, "_Money__frozen", True)

            def __setattr__(self, name: str, value: object) -> None:
                if getattr(self, "_Money__frozen", False):
                    raise CantModifyImmutableAttributeError(
                        class_name=self.__class__.__name__,
                        attribute_name=name,
                    )
                object.__setattr__(self, name, value)
        ```

        With selective freezing:

        ```python
        from forging_blocks.foundation.autofreeze import auto_freeze
        from forging_blocks.foundation.errors import (
            CantModifyImmutableAttributeError,
        )


        @auto_freeze(attrs=["_user_id", "_email"])
        class User:
            def __init__(self, user_id: str, email: str, name: str) -> None:
                self._user_id = user_id
                self._email = email
                self._name = name

            def freeze_attributes(self, attrs: Sequence[str]) -> None:
                frozen_attrs = getattr(self, "_User__frozen_attrs", set())
                frozen_attrs.update(attrs)
                object.__setattr__(self, "_User__frozen_attrs", frozen_attrs)

            def __setattr__(self, name: str, value: object) -> None:
                frozen_attrs = getattr(self, "_User__frozen_attrs", set())
                if name in frozen_attrs:
                    raise CantModifyImmutableAttributeError(
                        class_name=self.__class__.__name__,
                        attribute_name=name,
                    )
                object.__setattr__(self, name, value)
        ```
    """
    decorator = _AutoFreezeDecorator(attrs=attrs)

    if class_ is not None:
        return decorator(class_)

    return decorator
