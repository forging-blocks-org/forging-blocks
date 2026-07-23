"""Auto-hash decorator for generating ``__hash__`` on class instances.

Provides the :func:`auto_hash` decorator that generates ``__hash__``
based on class fields.  Works with ``@dataclass`` (``@auto_hash`` must be
the outermost decorator -- apply it *above* ``@dataclass``) and on plain
classes with ``__slots__`` or ``__annotations__``::

    @auto_hash
    @dataclass
    class MyType:
        user_id: str
        name: str | None = None

Can be used as ``@auto_hash``, ``@auto_hash()``, or
``@auto_hash(fields=[...])`` to hash only specific attributes.

Does NOT generate ``__eq__`` -- combine with :func:`auto_eq` when structural
equality is needed alongside hashing:

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
    from forging_blocks.foundation.autofreeze import auto_freeze
    from forging_blocks.foundation.autohash import auto_hash


    @auto_hash
    @auto_eq
    @auto_freeze
    @dataclass
    class Money:
        amount: int
        currency: str


    m1 = Money(100, "USD")
    m2 = Money(100, "USD")
    assert hash(m1) == hash(m2)
    assert m1 == m2  # from @auto_eq
    ```

"""

import dataclasses
from collections.abc import Callable, Sequence
from typing import Any, overload

from forging_blocks.foundation.autohash.helpers.hashable_converter import (
    HashableConverter,
)


class _AutoHashDecorator:
    """Callable class that applies auto-hash behaviour to a target class.

    Generates ``__hash__`` only, based on the class's fields.
    The hash is computed by converting each field value to a hashable form and
    then hashing the resulting tuple.

    """

    def __init__(self, *, fields: Sequence[str] | None = None) -> None:
        """Initialise the decorator with optional field selector.

        Args:
            fields: Specific field names to hash. When ``None``, all
                dataclass fields (or ``__slots__``/``__annotations__`` keys) are
                used.

        """
        self._fields = fields

    def __call__[T](self, class_: type[T]) -> type[T]:
        """Apply auto-hash behaviour to *class_*.

        Args:
            class_: The target class to decorate.

        Returns:
            The decorated class with ``__hash__`` generated from its fields.
            Equality (``__eq__``) is NOT generated — use :func:`auto_eq`
            separately for structural equality comparisons.

        """
        field_names = self._resolve_field_names(class_)
        _field_names = tuple(field_names)

        def _hash_impl(self: Any) -> int:
            values = tuple(getattr(self, f) for f in _field_names)
            return hash(tuple(HashableConverter.convert(v) for v in values))

        _hash_impl.__name__ = "__hash__"
        _hash_impl.__qualname__ = f"{class_.__name__}.__hash__"

        class_.__hash__ = _hash_impl
        class_.__auto_hash_fields__ = _field_names
        return class_

    def _resolve_field_names(self, class_: type[object]) -> list[str]:
        """Determine which field names contribute to ``__hash__``.

        Priority:
        1. Explicit *fields* argument passed to the decorator.
        2. Dataclass fields (via ``dataclasses.fields``).
        3. ``__slots__`` across the full MRO, excluding dunder names.
        4. ``__annotations__`` if defined.

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

        slots = self._collect_slots(class_)
        if slots:
            return sorted(slots)

        annotations: dict[str, object] | None = getattr(class_, "__annotations__", None)
        if annotations:
            return [k for k in annotations if not k.startswith("__")]

        msg = (
            f"Cannot determine hash fields for non-dataclass {class_.__name__}. "
            f"Pass fields= explicitly, e.g. @auto_hash(fields=['x', 'y'])."
        )
        raise TypeError(msg)

    @staticmethod
    def _collect_slots(class_: type[object]) -> set[str]:
        """Collect all ``__slots__`` from *class_* and its MRO.

        Handles the rare case where ``__slots__`` is defined as a single
        string (``__slots__ = "x"``) rather than an iterable of strings.
        """
        all_slots: set[str] = set()
        for cls in class_.__mro__:
            slots = getattr(cls, "__slots__", ())
            if isinstance(slots, str):
                slots = (slots,)
            for slot in slots:
                if not slot.startswith("__"):
                    all_slots.add(slot)
        return all_slots


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


def auto_hash[T](
    class_: type[T] | None = None,
    *,
    fields: Sequence[str] | None = None,
) -> type[T] | Callable[[type[T]], type[T]]:
    """Generate ``__hash__`` for a class based on its fields.

    Generates ``__hash__`` only — does NOT generate ``__eq__``.
    Use :func:`auto_eq` for structural equality comparisons.

    Args:
        class_: The class to decorate.
        fields: Optional sequence of field names to include in the hash.
            When ``None``, all dataclass fields (or ``__slots__``/
            ``__annotations__`` keys) are used.

    Returns:
        The decorated class with ``__hash__`` generated. Equality
        (``__eq__``) is not changed — apply ``@auto_eq`` separately
        when needed.

    """
    decorator = _AutoHashDecorator(fields=fields)

    if class_ is not None:
        return decorator(class_)
    return decorator
