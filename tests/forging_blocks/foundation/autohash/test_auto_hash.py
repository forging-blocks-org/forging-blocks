# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportUnhashable=false
"""Tests for the auto_hash decorator."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from forging_blocks.foundation.autofreeze.auto_freeze import auto_freeze
from forging_blocks.foundation.autohash.auto_hash import auto_hash

# ---------------------------------------------------------------------------
# Tests for the auto_hash decorator
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAutoHashDecorator:
    """Tests for the auto_hash decorator public API."""

    # -- Usage modes --------------------------------------------------------

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

        # Decorating again replaces __hash__
        redecorated = auto_hash(MyClass)
        assert redecorated is MyClass
        assert redecorated.__hash__ is not original_hash

    # -- Hash behavior ------------------------------------------------------

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

        # Same x, different y — should be equal hash since only x used
        assert hash(p1) == hash(p2)

    def test_when_none_field_value_then_hash_does_not_raise(self) -> None:
        @auto_hash
        @dataclass
        class OptionalThing:
            name: str | None

        t = OptionalThing(None)
        # Should not raise
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

    def test_when_only_auto_hash_no_freeze_then_mutable_but_hashable(self) -> None:
        @auto_hash
        @dataclass
        class MutablePoint:
            x: int
            y: int

        mp = MutablePoint(1, 2)
        original_hash = hash(mp)

        mp.x = 999
        new_hash = hash(mp)

        assert new_hash != original_hash

    # -- Plain classes ------------------------------------------------------

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
                self.__cached__ = hash(x)  # dunder slot ignored

        s1 = SlottedWithDunder(5)
        s2 = SlottedWithDunder(5)

        assert hash(s1) == hash(s2)

    def test_when_non_dataclass_without_fields_then_type_error(self) -> None:
        with pytest.raises(TypeError, match="Cannot determine hash fields"):

            class Plain:
                def __init__(self, x: int) -> None:
                    self.x = x

            auto_hash(Plain)

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

    # -- Integration: sets --------------------------------------------------

    def test_whenhash_consistent_then_set_deduplicates(self) -> None:
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

    # -- Unhashable field types -------------------------------------------

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
        # Verify set dedup works
        assert len({a, b, c}) == 2

    def test_when_dict_field_then_converted_to_sorted_tuple_for_hash(self) -> None:
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

        # sets are not converted — should raise
        instance = WithSet("x", {1, 2})
        with pytest.raises(TypeError, match="Cannot convert"):
            hash(instance)
