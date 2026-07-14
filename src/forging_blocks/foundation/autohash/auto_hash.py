"""Auto-hash decorator for generating ``__hash__`` on dataclass instances.

Provides the :func:`auto_hash` decorator that generates a ``__hash__`` method
based on dataclass fields and automatically composes :func:`auto_freeze` to
enforce immutability.  A hashable object must be immutable — ``@auto_hash``
ensures both by applying ``@auto_freeze`` internally, which forbids attribute
assignment after ``__init__`` completes.
Works with ``@dataclass`` (``@auto_hash`` must be the outermost decorator
— apply it *above* ``@dataclass``) and on plain classes with ``__slots__``
or ``__annotations__``::

    @auto_hash
    @dataclass
    class MyType:
        user_id: str
        name: str | None = None

Can be used as ``@auto_hash``, ``@auto_hash()``, or
``@auto_hash(fields=[...])`` to hash only specific attributes.

Explicit ``@auto_freeze`` is NOT required — ``@auto_hash`` applies it
automatically. Applying both is harmless (idempotent).

Example:
    ```python
    from dataclasses import dataclass

    from forging_blocks.foundation.autohash import auto_hash


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

import dataclasses
from collections.abc import Callable, Sequence
from typing import Any, overload

from forging_blocks.foundation.autofreeze import auto_freeze as _auto_freeze
from forging_blocks.foundation.autohash.helpers.hashable_converter import (
    HashableConverter,
)


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
                dataclass fields (or ``__slots__``/``__annotations__`` keys) are
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
        _field_names = tuple(field_names)

        def _hash_impl(self: Any) -> int:
            values = tuple(getattr(self, f) for f in _field_names)
            return hash(tuple(HashableConverter.convert(v) for v in values))

        _hash_impl.__name__ = "__hash__"
        _hash_impl.__qualname__ = f"{class_.__name__}.__hash__"

        class_.__hash__ = _hash_impl
        _auto_freeze(class_)
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

    Automatically applies :func:`auto_freeze` to enforce immutability.
    Hashable objects MUST be immutable — ``@auto_hash`` ensures both by
    applying ``@auto_freeze`` internally, which forbids attribute assignment
    after ``__init__`` completes.
    When the class is a ``@dataclass``, *fields* defaults to all declared
    dataclass fields (via ``dataclasses.fields``). Otherwise it falls back
    to ``__slots__`` (across the MRO) or ``__annotations__`` keys.

    Args:
        class_: The target class (when used bare).
        fields: Specific attribute names to include in the hash. When
            ``None`` (the default), all dataclass fields are used.

    Returns:
        The decorated class (or a decorator when used parameterised),
        with both ``__hash__`` and immutability applied.

    Raises:
        TypeError: If no field names can be determined and *fields* is
            ``None``.
    """
    decorator = _AutoHashDecorator(fields=fields)

    if class_ is not None:
        return decorator(class_)
    return decorator
