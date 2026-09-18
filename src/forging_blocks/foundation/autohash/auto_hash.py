"""Auto-hash decorator for generating ``__hash__`` on class instances.

Provides the `auto_hash` decorator that generates ``__hash__``
based on class fields. Works on plain classes with ``__slots__`` or
``__annotations__``.

Can be used as ``@auto_hash``, ``@auto_hash()``, or
``@auto_hash(fields=[...])`` to hash only specific attributes.

Does NOT generate ``__eq__`` — combine with `auto_eq` when structural
equality is needed alongside hashing.

Useful for: Hashable data types and any type that requires
consistent hashing for sets or dictionary keys.

Example:
    ```python
    @auto_hash
    class Point2D:
        __slots__ = ("x", "y")

        def __init__(self, x: float, y: float) -> None:
            self.x = x
            self.y = y


    p1 = Point2D(1.0, 2.0)
    p2 = Point2D(1.0, 2.0)
    assert hash(p1) == hash(p2)
    ```

    With selective fields:
    ```python
    @auto_hash(fields=["id"])
    class Record:
        __slots__ = ("id", "data")

        def __init__(self, id: str, data: str) -> None:
            self.id = id
            self.data = data


    r1 = Record("abc", "payload-a")
    r2 = Record("abc", "payload-b")
    assert hash(r1) == hash(r2)
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

    Example:
        ```python
        class Record:
            __slots__ = ("id",)

            def __init__(self, id: str) -> None:
                self.id = id


        decorator = _AutoHashDecorator(fields=["id"])
        Record = decorator(Record)
        assert hash(Record("abc")) == hash(Record("abc"))
        ```
    """

    def __init__(self, *, fields: Sequence[str] | None = None) -> None:
        """Initialise the decorator with optional field selector.

        Args:
            fields: Specific field names to hash. When ``None``, all
                all fields declared in ``__slots__`` or
                ``__annotations__`` are used.

        """
        self._fields = fields

    def __call__[T](self, class_: type[T]) -> type[T]:
        """Apply auto-hash behaviour to *class_*.

        Args:
            class_: The target class to decorate.

        Returns:
            The decorated class with ``__hash__`` generated from its fields.
            Equality (``__eq__``) is NOT generated — use `auto_eq`
            separately for structural equality comparisons.

        """
        field_names = self._resolve_field_names(class_)
        _field_names = tuple(field_names)

        def _hash_impl(self: Any) -> int:
            values = tuple(getattr(self, f) for f in _field_names)
            converted = (
                HashableConverter.convert(v, field_name=f)
                for f, v in zip(_field_names, values, strict=True)
            )
            return hash(tuple(converted))

        _hash_impl.__name__ = "__hash__"
        _hash_impl.__qualname__ = f"{class_.__name__}.__hash__"

        class_.__hash__ = _hash_impl
        type.__setattr__(class_, "__auto_hash_fields__", _field_names)
        return class_

    @staticmethod
    def _dataclass_field_names(class_: type[object]) -> list[str] | None:
        if dataclasses.is_dataclass(class_):
            return [f.name for f in dataclasses.fields(class_)]
        return None

    def _resolve_from_class(self, class_: type[object]) -> list[str] | None:
        dc_fields = self._dataclass_field_names(class_)
        if dc_fields is not None:
            return dc_fields

        slots = self._collect_slots(class_)
        if slots:
            return sorted(slots)

        annotations = self._collect_annotations(class_)
        if annotations:
            return sorted(annotations)

        return None

    def _resolve_field_names(self, class_: type[object]) -> list[str]:
        """Determine which field names contribute to ``__hash__``.

        Priority:
        1. Explicit *fields* argument passed to the decorator.
        2. ``__slots__`` across the full MRO, excluding dunder names.
        3. ``__annotations__`` if defined.

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

        resolved = self._resolve_from_class(class_)
        if resolved is not None:
            return resolved

        msg = (
            f"Cannot determine hash fields for {class_.__name__}. "
            f"Pass fields= explicitly, e.g. @auto_hash(fields=['x', 'y'])."
        )
        raise TypeError(msg)

    @classmethod
    def _collect_slots(cls, class_: type[object]) -> set[str]:
        """Collect all ``__slots__`` from *class_* and its MRO.

        Handles the rare case where ``__slots__`` is defined as a single
        string (``__slots__ = "x"``) rather than an iterable of strings.
        """
        all_slots: set[str] = set()
        for c in class_.__mro__:
            slots = getattr(c, "__slots__", ())
            if isinstance(slots, str):
                slots = (slots,)
            for slot in slots:
                if not slot.startswith("__"):
                    all_slots.add(slot)
        return all_slots

    @classmethod
    def _collect_annotations(cls, class_: type[object]) -> set[str]:
        """Collect all ``__annotations__`` keys from *class_* and its MRO.

        Excludes dunder names (``__module__``, ``__qualname__``, etc.).
        """
        all_annotations: set[str] = set()
        for c in class_.__mro__:
            ann: dict[str, object] | None = getattr(c, "__annotations__", None)
            if ann is not None:
                for key in ann:
                    if not key.startswith("__"):
                        all_annotations.add(key)
        return all_annotations


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

    Can be used as ``@auto_hash``, ``@auto_hash()``, or
    ``@auto_hash(fields=[...])``. Generates ``__hash__`` only — does NOT
    generate ``__eq__``. Use `auto_eq` for structural equality
    comparisons.

    Args:
        class_: The target class (when used directly as ``@auto_hash``).
            ``None`` when used with parentheses (``@auto_hash()`` or
            ``@auto_hash(fields=...)``).
        fields: Optional sequence of field names to include in the hash.
            When ``None``, all fields declared in ``__slots__`` or
            ``__annotations__`` are used.

    Returns:
        The decorated class if *class_* is provided; otherwise a callable
        that can be used as a decorator.

    Raises:
        TypeError: If no field names can be determined automatically and
            *fields* is ``None``.

    """
    decorator = _AutoHashDecorator(fields=fields)

    if class_ is not None:
        return decorator(class_)
    return decorator
