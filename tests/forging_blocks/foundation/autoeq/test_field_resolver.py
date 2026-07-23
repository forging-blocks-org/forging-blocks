from __future__ import annotations

import dataclasses

import pytest

from forging_blocks.foundation.autoeq.helpers.field_resolver import FieldResolver


@pytest.mark.unit
class TestFieldResolver:
    def test_when_fields_explicit_then_returns_list(self) -> None:
        class A:
            def __init__(self) -> None:
                self.x = 1

        result = FieldResolver.resolve(A, fields=["x", "y"])
        assert result == ["x", "y"]

    def test_when_dataclass_then_returns_field_names(self) -> None:
        @dataclasses.dataclass
        class A:
            x: int
            y: str

        result = FieldResolver.resolve(A)
        assert result == ["x", "y"]

    def test_when_slots_present_then_returns_sorted_slot_names(self) -> None:
        class A:
            __slots__ = ("z", "a", "m")

            def __init__(self, z: int, a: str, m: float) -> None:
                self.z = z
                self.a = a
                self.m = m

        result = FieldResolver.resolve(A)
        assert result == ["a", "m", "z"]

    def test_when_slots_single_element_then_returns_slot(self) -> None:
        class A:
            __slots__ = ("only_slot",)

            def __init__(self, only_slot: int) -> None:
                self.only_slot = only_slot

        result = FieldResolver.resolve(A)
        assert result == ["only_slot"]

    def test_when_slots_from_inheritance_chain_then_returns_all(self) -> None:
        class Base:
            __slots__ = ("x",)

        class Child(Base):
            __slots__ = ("y",)

        result = FieldResolver.resolve(Child)
        assert result == ["x", "y"]

    def test_when_slots_exclude_dunder_names(self) -> None:
        class A:
            __slots__ = ("__private", "public", "__another_private")

            def __init__(self) -> None:
                self.public = 1

        result = FieldResolver.resolve(A)
        assert result == ["public"]

    def test_when_no_slots_but_annotations_present_then_returns_annotation_keys(self) -> None:
        class A:
            x: int
            y: str

            def __init__(self, x: int, y: str) -> None:
                self.x = x
                self.y = y

        result = FieldResolver.resolve(A)
        assert sorted(result) == ["x", "y"]

    def test_when_no_explicit_fields_slots_or_annotations_then_raises_typeerror(self) -> None:
        class A:
            pass

        with pytest.raises(TypeError, match="Cannot determine eq fields"):
            FieldResolver.resolve(A)
