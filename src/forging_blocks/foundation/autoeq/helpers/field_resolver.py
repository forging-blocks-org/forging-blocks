"""Field resolution logic shared by the auto_eq decorator."""

import dataclasses
from collections.abc import Sequence


class FieldResolver:
    """Resolves which field names contribute to ``__eq__`` for a class."""

    @staticmethod
    def resolve(
        class_: type[object],
        fields: Sequence[str] | None = None,
    ) -> list[str]:
        if fields is not None:
            return list(fields)

        if dataclasses.is_dataclass(class_):
            return [f.name for f in dataclasses.fields(class_)]

        slots = FieldResolver._collect_slots(class_)
        if slots:
            return sorted(slots)

        annotations: dict[str, object] | None = getattr(class_, "__annotations__", None)
        if annotations:
            return [k for k in annotations if not k.startswith("__")]

        msg = (
            f"Cannot determine eq fields for non-dataclass {class_.__name__}. "
            f"Pass fields= explicitly, e.g. @auto_eq(fields=['x', 'y'])."
        )
        raise TypeError(msg)

    @staticmethod
    def _collect_slots(class_: type[object]) -> set[str]:
        all_slots: set[str] = set()
        for cls in class_.__mro__:
            slots = getattr(cls, "__slots__", ())
            if isinstance(slots, str):
                slots = (slots,)
            for slot in slots:
                if not slot.startswith("__"):
                    all_slots.add(slot)
        return all_slots
