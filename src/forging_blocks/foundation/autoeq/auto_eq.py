"""Auto-eq decorator for generating ``__eq__`` on class instances.

Provides the :func:`auto_eq` decorator that generates ``__eq__`` based on
class fields. Works with ``@dataclass`` (``@auto_eq`` must be the outermost
decorator) and on plain classes with ``__slots__`` or ``__annotations__``.

Can be used as ``@auto_eq``, ``@auto_eq()``, or ``@auto_eq(fields=[...])``
to compare only specific attributes.

Does NOT generate ``__hash__`` — combine with :func:`auto_hash` when
hashability is needed:

    @auto_hash
    @auto_eq
    @auto_freeze
    @dataclass
    class Money:
        amount: int
        currency: str

Example:
    ```python
    from dataclasses import dataclass
    from forging_blocks.foundation.autoeq import auto_eq


    @auto_eq
    @dataclass
    class Point:
        x: int
        y: int


    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(3, 4)
    assert p1 == p2
    assert p1 != p3
    ```
"""

from collections.abc import Callable, Sequence
from typing import Any, overload

from forging_blocks.foundation.autoeq.helpers.field_resolver import (
    FieldResolver,
)


class _AutoEqDecorator:
    """Callable class that applies auto-eq behaviour to a target class.

    Generates ``__eq__`` based on the class's fields. Does NOT generate
    ``__hash__`` — use :func:`auto_hash` separately when hashability
    is required.
    """

    def __init__(self, *, fields: Sequence[str] | None = None) -> None:
        self._fields = fields

    def __call__[T](self, class_: type[T]) -> type[T]:
        field_names = FieldResolver.resolve(class_, self._fields)
        _field_names = tuple(field_names)

        def _eq_impl(self: Any, other: object) -> bool:
            if type(self) is not type(other):
                return False
            return all(getattr(self, f) == getattr(other, f) for f in _field_names)

        _eq_impl.__name__ = "__eq__"
        _eq_impl.__qualname__ = f"{class_.__name__}.__eq__"

        class_.__eq__ = _eq_impl
        class_.__auto_eq_fields__ = _field_names
        return class_


@overload
def auto_eq[T](class_: type[T]) -> type[T]: ...


@overload
def auto_eq[T](
    class_: type[T],
    *,
    fields: Sequence[str] | None = None,
) -> type[T]: ...


@overload
def auto_eq[T](
    class_: None = None,
    *,
    fields: Sequence[str] | None = None,
) -> Callable[[type[T]], type[T]]: ...


def auto_eq[T](
    class_: type[T] | None = None,
    *,
    fields: Sequence[str] | None = None,
) -> type[T] | Callable[[type[T]], type[T]]:
    """Generate ``__eq__`` for a class based on its fields.

    Does NOT generate ``__hash__`` — combine with :func:`auto_hash`
    when hashability is required.
    When the class is a ``@dataclass``, *fields* defaults to all declared
    dataclass fields (via ``dataclasses.fields``). Otherwise it falls back
    to ``__slots__`` (across the MRO) or ``__annotations__`` keys.

    Args:
        class_: The target class (when used bare).
        fields: Specific attribute names to include in equality. When
            ``None`` (the default), all dataclass fields are used.

    Returns:
        The decorated class (or a decorator when used parameterised),
        with ``__eq__`` generated.

    Raises:
        TypeError: If no field names can be determined and *fields* is
            ``None``.
    """
    decorator = _AutoEqDecorator(fields=fields)

    if class_ is not None:
        return decorator(class_)
    return decorator
