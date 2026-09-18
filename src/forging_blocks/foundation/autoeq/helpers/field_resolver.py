"""Field resolution logic shared by the auto_eq decorator."""

import dataclasses
from collections.abc import Sequence


class FieldResolver:
    """Resolves which field names contribute to ``__eq__`` for a class.

    Example:
        ```python
        from forging_blocks.foundation.autoeq.helpers.field_resolver import FieldResolver


        class Point:
            x: int
            y: int


        fields = FieldResolver.resolve(Point)
        assert fields == ["x", "y"]
        ```
    """

    @classmethod
    def _dataclass_fields(cls, class_: type[object]) -> list[str] | None:
        if dataclasses.is_dataclass(class_):
            return [f.name for f in dataclasses.fields(class_)]
        return None

    @classmethod
    def _resolve_from_class(cls, class_: type[object]) -> list[str] | None:
        dc_fields = cls._dataclass_fields(class_)
        if dc_fields is not None:
            return dc_fields

        slots = cls._collect_slots(class_)
        if slots:
            return sorted(slots)

        annotations = cls._collect_annotations(class_)
        if annotations:
            return sorted(annotations)

        return None

    @classmethod
    def resolve(
        cls,
        class_: type[object],
        fields: Sequence[str] | None = None,
    ) -> list[str]:
        """Resolve field names contributing to equality for a class."""
        if fields is not None:
            return list(fields)

        resolved = cls._resolve_from_class(class_)
        if resolved is not None:
            return resolved

        msg = (
            f"Cannot determine eq fields for non-dataclass {class_.__name__}. "
            f"Pass fields= explicitly, e.g. @auto_eq(fields=['x', 'y'])."
        )
        raise TypeError(msg)

    @classmethod
    def _collect_slots(cls, class_: type[object]) -> set[str]:
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
