"""Auto-freeze decorator for enforcing immutability on class instances."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from functools import wraps
from typing import Any, overload

_AUTO_FREEZE_MARKER = "__auto_freeze_applied"


class _AutoFreezeDecorator:
    def __init__(
        self,
        *,
        attrs: Sequence[str] | None = None,
    ) -> None:
        self._attrs = attrs

    def __call__[T](self, class_: type[T]) -> type[T]:
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

            if class_.should_use_internal_freezing():
                if attrs is None:
                    instance.freeze_instance()
                else:
                    instance.freeze_attributes(attrs)

        object.__setattr__(wrapped_init, _AUTO_FREEZE_MARKER, True)

        class_.__init__ = wrapped_init  # type: ignore[method-assign]

        return class_

    @staticmethod
    def _validate_protocol[T](class_: type[T]) -> None:
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
    decorator = _AutoFreezeDecorator(attrs=attrs)

    if class_ is not None:
        return decorator(class_)

    return decorator
