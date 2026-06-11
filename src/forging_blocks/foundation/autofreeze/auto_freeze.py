"""Auto-freeze decorator for enforcing immutability on class instances.

Provides the :func:`auto_freeze` decorator that automatically freezes instances
after ``__init__`` completes. Classes decorated with ``@auto_freeze`` must satisfy
:class:`~forging_blocks.foundation.autofreeze.SupportsAutoFreeze` (i.e. implement
:meth:`freeze_instance`, :meth:`unfreeze_instance`, and
:meth:`should_use_internal_freezing`). The decorator injects a wrapper around
``__init__`` that calls the freezing protocol at the end of construction.
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

    Args:
        attrs: Optional sequence of attribute names to selectively freeze.
            When ``None`` (the default) the entire instance is frozen via
            :meth:`freeze_instance`. When provided, only the named attributes
            are frozen via :meth:`freeze_attributes`.
    """

    def __init__(
        self,
        *,
        attrs: Sequence[str] | None = None,
    ) -> None:
        """Initialise the decorator with optional selective-freeze attributes.

        Args:
            attrs: Attribute names to selectively freeze. ``None`` means
                freeze the entire instance.
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

            if class_.should_use_internal_freezing():  # type: ignore[attr-defined]
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

        Checks for the presence of the three required methods:
        :meth:`should_use_internal_freezing`, :meth:`freeze_instance`, and
        :meth:`unfreeze_instance`.

        Args:
            class_: The class to validate.

        Raises:
            TypeError: If any required protocol method is missing.
        """
        required = {
            "should_use_internal_freezing": "classmethod",
            "freeze_instance": "instance method",
            "unfreeze_instance": "instance method",
        }

        missing = [name for name in required if not hasattr(class_, name)]

        if missing:
            raise TypeError(
                f"{class_.__name__} does not implement SupportsAutoFreeze protocol.\n"
                f"Missing: {', '.join(missing)}"
            )


@overload
def auto_freeze[T](class_: type[T]) -> type[T]:
    ...


@overload
def auto_freeze[T](
    class_: type[T],
    *,
    attrs: Sequence[str] | None = None,
) -> type[T]:
    ...


@overload
def auto_freeze[T](
    class_: None = None,
    *,
    attrs: Sequence[str] | None = None,
) -> Callable[[type[T]], type[T]]:
    ...


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
            protocol methods (``should_use_internal_freezing``,
            ``freeze_instance``, ``unfreeze_instance``).

    Example:

        ```python
        from forging_blocks.foundation.autofreeze import auto_freeze

        @auto_freeze
        class Money:
            def __init__(self, amount: int, currency: str) -> None:
                self._amount = amount
                self._currency = currency

            @classmethod
            def should_use_internal_freezing(cls) -> bool:
                return True

            def freeze_instance(self) -> None:
                object.__setattr__(self, "_Money__frozen", True)

            def unfreeze_instance(self) -> None:
                object.__setattr__(self, "_Money__frozen", False)
        ```

        With selective freezing:

        ```python
        @auto_freeze(attrs=["_id"])
        class User:
            def __init__(self, user_id: str, name: str) -> None:
                self._id = user_id
                self._name = name

            ...  # protocol methods + freeze_attributes
        ```
    """
    decorator = _AutoFreezeDecorator(attrs=attrs)

    if class_ is not None:
        return decorator(class_)

    return decorator
