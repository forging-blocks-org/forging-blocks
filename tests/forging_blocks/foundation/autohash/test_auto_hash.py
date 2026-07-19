# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportUnhashable=false
"""Tests for the auto_hash decorator."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from forging_blocks.foundation.autofreeze.auto_freeze import auto_freeze
from forging_blocks.foundation.autohash.auto_hash import auto_hash
from forging_blocks.foundation.errors import CantModifyImmutableAttributeError
from forging_blocks.foundation.errors.non_hashable_value_error import (
    NonHashableValueError,
)


@pytest.mark.unit
class TestAutoHashDecorator:
    """Tests for the auto_hash decorator public API."""

    def test_when_used_without_parentheses_then_decorates_class(self) -> None:
        @auto_hash
        @dataclass
        class MyClass:
            x: int

        decorated = auto_hash(MyClass)
        assert decorated is MyClass

    def test_when_used_with_empty_parentheses_then_returns_decorator(self) -> None:
        @dataclass
        class MyClass:
            x: int

        decorator = auto_hash()
        decorated = decorator(MyClass)
        assert decorated is MyClass

    def test_when_used_with_fields_then_returns_decorator(self) -> None:
        @dataclass
        class MyClass:
            x: int
            y: int

        decorator = auto_hash(fields=["x"])
        decorated = decorator(MyClass)
        assert decorated is MyClass

    def test_when_class_already_decorated_then_replaces_hash(self) -> None:
        @auto_hash
        @dataclass
        class MyClass:
            x: int

        original_hash = MyClass.__hash__

        redecorated = auto_hash(MyClass)
        assert redecorated is MyClass
        assert redecorated.__hash__ is not original_hash

    def test_when_dataclass_all_fields_then_equal_objects_have_equal_hash(self) -> None:
        @auto_hash
        @dataclass
        class Point:
            x: int
            y: int

        p1 = Point(1, 2)
        p2 = Point(1, 2)
        p3 = Point(3, 4)

        assert p1 == p2
        assert hash(p1) == hash(p2)
        assert hash(p1) != hash(p3)

    def test_when_dataclass_different_values_then_different_hash(self) -> None:
        @auto_hash
        @dataclass
        class Point:
            x: int
            y: int

        p1 = Point(1, 2)
        p2 = Point(2, 1)

        assert hash(p1) != hash(p2)

    def test_when_fields_subset_then_only_selected_fields_in_hash(self) -> None:
        @auto_hash(fields=["x"])
        @dataclass
        class Point:
            x: int
            y: int

        p1 = Point(1, 2)
        p2 = Point(1, 999)

        assert hash(p1) == hash(p2)

    def test_when_none_field_value_then_hash_does_not_raise(self) -> None:
        @auto_hash
        @dataclass
        class OptionalThing:
            name: str | None

        t = OptionalThing(None)
        _ = hash(t)

    def test_when_single_field_then_hash_matches_tuple_of_one(self) -> None:
        @auto_hash
        @dataclass
        class Single:
            value: str

        s = Single("hello")
        assert hash(s) == hash(("hello",))

    def test_when_dataclass_with_default_then_default_not_in_fields(self) -> None:
        @auto_hash
        @dataclass
        class WithDefault:
            x: int
            y: int = 42

        w1 = WithDefault(1)
        w2 = WithDefault(1)

        assert hash(w1) == hash(w2)

    def test_when_dataclass_frozen_by_auto_freeze_then_hash_still_works(self) -> None:
        @auto_freeze
        @auto_hash
        @dataclass
        class Money:
            amount: int
            currency: str

        m1 = Money(100, "USD")
        m2 = Money(100, "USD")
        m3 = Money(200, "USD")

        assert m1 == m2
        assert hash(m1) == hash(m2)
        assert hash(m1) != hash(m3)

    def test_when_hash_follows_auto_freeze_then_still_hashable(self) -> None:
        """auto_hash inside auto_freeze (= applied second) still works."""

        @auto_freeze
        @auto_hash
        @dataclass
        class Item:
            sku: str

        i1 = Item("A")
        i2 = Item("A")

        assert hash(i1) == hash(i2)
        assert i1 in {i1, i2}  # hashable → can be in set

    def test_when_auto_hash_then_instance_is_frozen(self) -> None:
        """auto_hash composes auto_freeze — instances are immutable."""

        @auto_hash
        @dataclass
        class Point:
            x: int
            y: int

        p = Point(1, 2)
        _ = hash(p)

        with pytest.raises(CantModifyImmutableAttributeError):
            p.x = 999

    def test_when_plain_class_with_slots_then_hash_works(self) -> None:
        @auto_hash
        class Slotted:
            __slots__ = ("x", "y")

            def __init__(self, x: int, y: int) -> None:
                self.x = x
                self.y = y

        s1 = Slotted(1, 2)
        s2 = Slotted(1, 2)
        s3 = Slotted(3, 4)

        assert hash(s1) == hash(s2)
        assert hash(s1) != hash(s3)

    def test_when_plain_class_with_slots_and_dunder_skipped(self) -> None:
        @auto_hash
        class SlottedWithDunder:
            __slots__ = ("x", "__cached__")

            def __init__(self, x: int) -> None:
                self.x = x
                self.__cached__ = hash(x)

        s1 = SlottedWithDunder(5)
        s2 = SlottedWithDunder(5)

        assert hash(s1) == hash(s2)

    def test_when_slotted_inheritance_chain_with_auto_hash_then_hash_correct(self) -> None:
        @auto_hash
        class Base:
            __slots__ = ("_x",)

            def __init__(self, x: int) -> None:
                self._x = x

        @auto_hash
        class Child(Base):
            __slots__ = ("_y",)

            def __init__(self, x: int, y: str) -> None:
                super().__init__(x)
                self._y = y

        c1 = Child(1, "a")
        c2 = Child(1, "a")
        c3 = Child(2, "a")
        c4 = Child(1, "b")

        assert hash(c1) == hash(c2)
        assert hash(c1) != hash(c3)
        assert hash(c1) != hash(c4)

    def test_when_slotted_with_mixin_then_slots_collected_across_mro(self) -> None:
        """Verify _collect_slots walks MRO correctly even with mixins."""

        class Mixin:
            __slots__ = ()

        @auto_hash
        class Base:
            __slots__ = ("_base_field",)

            def __init__(self, base_field: int) -> None:
                self._base_field = base_field

        @auto_hash
        class Child(Mixin, Base):
            __slots__ = ("_child_field",)

            def __init__(self, base_field: int, child_field: str) -> None:
                super().__init__(base_field)
                self._child_field = child_field

        c1 = Child(1, "x")
        c2 = Child(1, "x")
        c3 = Child(2, "x")

        assert hash(c1) == hash(c2)
        assert hash(c1) != hash(c3)

    def test_when_single_string_slots_then_hash_works(self) -> None:
        @auto_hash
        class SingleSlot:
            __slots__ = "_value"

            def __init__(self, value: int) -> None:
                self._value = value

        s1 = SingleSlot(1)
        s2 = SingleSlot(1)
        s3 = SingleSlot(2)

        assert hash(s1) == hash(s2)
        assert hash(s1) != hash(s3)

    def test_when_non_dataclass_without_fields_then_type_error(self) -> None:
        with pytest.raises(TypeError, match="Cannot determine hash fields"):

            class Plain:
                def __init__(self, x: int) -> None:
                    self.x = x

            auto_hash(Plain)

    def test_when_plain_class_with_annotations_then_hash_uses_annotations(self) -> None:
        class Plain:
            x: int
            y: int

            def __init__(self, x: int, y: int) -> None:
                self.x = x
                self.y = y

        auto_hash(Plain)

        p1 = Plain(1, 2)
        p2 = Plain(1, 2)
        p3 = Plain(3, 2)

        assert hash(p1) == hash(p2)
        assert hash(p1) != hash(p3)

    def test_when_non_dataclass_with_explicit_fields_then_succeeds(self) -> None:
        class Plain:
            def __init__(self, x: int, y: int) -> None:
                self.x = x
                self.y = y

        auto_hash(fields=["x", "y"])(Plain)

        p1 = Plain(1, 2)
        p2 = Plain(1, 2)
        p3 = Plain(3, 2)

        assert hash(p1) == hash(p2)
        assert hash(p1) != hash(p3)

    def test_when_auto_hash_and_auto_freeze_stacked_then_idempotent(self) -> None:
        """@auto_hash auto-applies @auto_freeze — stacking both is harmless."""

        @auto_freeze
        @auto_hash
        @dataclass
        class Point:
            x: int
            y: int

        p = Point(1, 2)
        assert hash(p) == hash(Point(1, 2))
        with pytest.raises(CantModifyImmutableAttributeError):
            p.x = 99

    def test_when_auto_freeze_before_auto_hash_then_idempotent(self) -> None:
        @auto_hash
        @auto_freeze
        @dataclass
        class Point:
            x: int
            y: int

        p = Point(1, 2)
        assert hash(p) == hash(Point(1, 2))
        with pytest.raises(CantModifyImmutableAttributeError):
            p.x = 99

    def test_when_hash_consistent_then_set_deduplicates(self) -> None:
        @auto_freeze
        @auto_hash
        @dataclass
        class Currency:
            code: str

        usd1 = Currency("USD")
        usd2 = Currency("USD")
        eur = Currency("EUR")

        unique = {usd1, usd2, eur}

        assert len(unique) == 2

    def test_when_list_field_then_converted_to_tuple_for_hash(self) -> None:
        @auto_freeze
        @auto_hash
        @dataclass
        class WithList:
            name: str
            items: list[str]

        a = WithList("x", ["a", "b"])
        b = WithList("x", ["a", "b"])
        c = WithList("x", ["c"])

        assert hash(a) == hash(b)
        assert hash(a) != hash(c)
        assert len({a, b, c}) == 2

    def test_when_dict_field_then_converted_to_frozenset_for_hash(self) -> None:
        @auto_hash
        @dataclass
        class WithDict:
            key: str
            metadata: dict[str, int]

        a = WithDict("k", {"b": 2, "a": 1})
        b = WithDict("k", {"a": 1, "b": 2})  # different insertion order, same contents

        assert hash(a) == hash(b)

    def test_when_none_list_or_dict_then_hash_fine(self) -> None:
        @auto_hash
        @dataclass
        class WithOptional:
            id: str
            tags: list[str] | None = None

        a = WithOptional("1", None)
        b = WithOptional("1", None)

        assert hash(a) == hash(b)

    def test_when_unhashable_unsupported_type_then_type_error(self) -> None:
        @auto_hash
        @dataclass
        class WithSet:
            id: str
            values: set[int]

        instance = WithSet("x", {1, 2})
        with pytest.raises(NonHashableValueError, match="Cannot convert"):
            hash(instance)


@pytest.mark.unit
class TestHashableConverterDeeplyHashable:
    """Tests for HashableConverter._ensure_deeply_hashable internals."""

    def test_ensure_deeply_hashable_when_frozenset_then_recursively_converts_elements(
        self,
    ) -> None:
        from forging_blocks.foundation.autohash.helpers.hashable_converter import (
            HashableConverter,
        )

        result = HashableConverter._ensure_deeply_hashable(frozenset([1, 2, 3]))
        assert isinstance(result, frozenset)
        assert result == frozenset([1, 2, 3])
