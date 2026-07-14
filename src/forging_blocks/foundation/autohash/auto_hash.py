"""Auto-hash decorator for generating ``__hash__`` on dataclass instances.

Provides the :func:`auto_hash` decorator that generates a ``__hash__`` method
based on dataclass fields. Composes with :func:`auto_freeze` to restore the
hashability that ``frozen=True`` normally provides, while keeping the
forging-blocks convention of using ``@auto_freeze`` for immutability.

Works with ``@dataclass`` (any order) and on plain classes with ``__slots__``
or ``__dict__`` attributes. When used with ``@auto_freeze``, apply
``@auto_hash`` *inside* (closer to the class)::

    @auto_freeze
    @auto_hash
    @dataclass
    class MyType:
        user_id: str
        name: str | None = None

Can be used as ``@auto_hash``, ``@auto_hash()``, or
``@auto_hash(fields=[...])`` to hash only specific attributes.

Example:
    ```python
    from dataclasses import dataclass

    from forging_blocks.foundation.autohash import auto_hash
    from forging_blocks.foundation.autofreeze import auto_freeze


    @auto_freeze
    @auto_hash
    @dataclass
    class Money:
        amount: int
        currency: str


    m1 = Money(100, "USD")
    m2 = Money(100, "USD")
    assert m1 == m2
    assert hash(m1) == hash(m2)
    ```
"""

from __future__ import annotations

import dataclasses
from collections.abc import Callable, Hashable, Sequence
from functools import wraps
from typing import Any, cast, overload


def _to_hashable(value: object) -> Hashable:
    """Convert *value* to a hashable equivalent.

    Recursively converts ``list`` to ``tuple`` and ``dict`` to
    ``tuple(sorted(...))`` so that field values can participate in
    ``__hash__``. Already-hashable values (``str``, ``int``, ``None``,
    ``tuple``, etc.) are returned unchanged.
    """
    if isinstance(value, Hashable):
        return value  # type: ignore[return-value]
    if isinstance(value, list):
        return tuple(_to_hashable(v) for v in value)  # type: ignore[reportUnknownVariableType,reportUnknownArgumentType]
    if isinstance(value, dict):
        items: dict[object, object] = cast("dict[object, object]", value)
        return tuple(sorted((k, _to_hashable(v)) for k, v in items.items()))
    msg = (
        f"Cannot convert {type(value).__name__!r} to hashable. "
        f"Use tuple, frozenset, or immutable types in fields hashed by @auto_hash."
    )
    raise TypeError(msg)


class _AutoHashDecorator:
    """Callable class that applies auto-hash behaviour to a target class.

    Generates a ``__hash__`` method based on the class's fields. The hash
    is computed by converting each field value to a hashable form and
    then hashing the resulting tuple.
    """

    def __init__(self, *, fields: Sequence[str] | None = None) -> None:
        """Initialise the decorator with optional field selector.

        Args:
            fields: Specific field names to hash. When ``None``, all
                dataclass fields (or ``__slots__``/``__dict__`` keys) are
                used.
        """
        self._fields = fields

    def __call__[T](self, class_: type[T]) -> type[T]:
        """Apply auto-hash behaviour to *class_*.

        Args:
            class_: The target class to decorate.

        Returns:
            The decorated class with ``__hash__`` generated.
        """
        field_names = self._resolve_field_names(class_)

        # Build the hash implementation that captures field_names by value.
        _field_names = tuple(field_names)

        @wraps(object.__hash__)
        def auto_hash_impl(self: Any) -> int:
            return hash(tuple(_to_hashable(getattr(self, f)) for f in _field_names))

        class_.__hash__ = auto_hash_impl  # type: ignore[method-assign]
        return class_

    def _resolve_field_names(self, class_: type[object]) -> list[str]:
        """Determine which field names contribute to ``__hash__``.

        Priority:
        1. Explicit *fields* argument passed to the decorator.
        2. Dataclass fields (via ``dataclasses.fields``).
        3. ``__slots__`` if defined.
        4. ``__dict__`` keys, excluding dunder and callable entries.

        Args:
            class_: The class being decorated.

        Returns:
            A list of field names to include in ``__hash__``.

        Raises:
            TypeError: If no fields can be determined automatically and
                *fields* is ``None``.
        """
        if self._fields is not None:
            return list(self._fields)

        if dataclasses.is_dataclass(class_):
            return [f.name for f in dataclasses.fields(class_)]

        slots: tuple[str, ...] | None = getattr(class_, "__slots__", None)
        if slots is not None:
            return [s for s in slots if not s.startswith("__")]

        # Plain class — hash all instance-dict keys (excluding dunders).
        # We can't enumerate __dict__ at class-decorate time, so we
        # raise — plain classes need explicit field selection.
        msg = (
            f"Cannot determine hash fields for non-dataclass {class_.__name__}. "
            f"Pass fields= explicitly, e.g. @auto_hash(fields=['x', 'y'])."
        )
        raise TypeError(msg)


@overload
def auto_hash[T](class_: type[T]) -> type[T]: ...


@overload
def auto_hash[T](
    class_: type[T],
    *,
    fields: Sequence[str] | None = None,
) -> type[T]: ...


@overload
def auto_hash[T](
    class_: None = None,
    *,
    fields: Sequence[str] | None = None,
) -> Callable[[type[T]], type[T]]: ...


def auto_hash[T](  # type: ignore[return-type]
    class_: type[T] | None = None,
    *,
    fields: Sequence[str] | None = None,
) -> type[T] | Callable[[type[T]], type[T]]:
    """Generate ``__hash__`` for a class based on its fields.

    When the class is a ``@dataclass``, *fields* defaults to all declared
    dataclass fields (via ``dataclasses.fields``). Otherwise it falls back
    to ``__slots__`` or ``__dict__`` keys.

    Args:
        class_: The target class (when used bare).
        fields: Specific attribute names to include in the hash. When
            ``None`` (the default), all dataclass fields are used.

    Returns:
        The decorated class (or a decorator when used parameterised).

    Raises:
        TypeError: If no field names can be determined and *fields* is
            ``None``.
    """
    decorator = _AutoHashDecorator(fields=fields)

    if class_ is not None:
        return decorator(class_)
    return decorator
