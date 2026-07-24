# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportAttributeAccessIssue=false, reportUnusedVariable=false
"""Tests for the auto_eq decorator."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from forging_blocks.foundation.autoeq.auto_eq import auto_eq


@pytest.mark.unit
class TestAutoEqDecorator:
    """Tests for the auto_eq decorator public API."""

    def test_when_used_without_parentheses_then_decorates_class(self) -> None:
        @auto_eq
        @dataclass
        class MyClass:
            x: int

        decorated = auto_eq(MyClass)
        assert decorated is MyClass

    def test_when_used_with_empty_parentheses_then_returns_decorator(self) -> None:
        @dataclass
        class MyClass:
            x: int

        decorator = auto_eq()
        decorated = decorator(MyClass)
        assert decorated is MyClass

    def test_when_used_with_fields_then_returns_decorator(self) -> None:
        @dataclass
        class MyClass:
            x: int
            y: int

        decorator = auto_eq(fields=["x"])
        decorated = decorator(MyClass)
        assert decorated is MyClass

    def test_when_class_already_decorated_then_replaces_eq(self) -> None:
        @auto_eq
        @dataclass
        class MyClass:
            x: int

        original_eq = MyClass.__eq__

        redecorated = auto_eq(MyClass)
        assert redecorated is MyClass
        assert redecorated.__eq__ is not original_eq

    def test_when_equal_values_then_objects_are_equal(self) -> None:
        @auto_eq
        @dataclass
        class Point:
            x: int
            y: int

        p1 = Point(1, 2)
        p2 = Point(1, 2)

        assert p1 == p2

    def test_when_different_values_then_objects_are_not_equal(self) -> None:
        @auto_eq
        @dataclass
        class Point:
            x: int
            y: int

        p1 = Point(1, 2)
        p2 = Point(3, 4)

        assert p1 != p2

    def test_when_fields_subset_then_only_selected_fields_compared(self) -> None:
        @auto_eq(fields=["x"])
        @dataclass
        class Point:
            x: int
            y: int

        p1 = Point(1, 2)
        p2 = Point(1, 999)

        assert p1 == p2

    def test_when_fields_subset_different_then_not_equal(self) -> None:
        @auto_eq(fields=["x"])
        @dataclass
        class Point:
            x: int
            y: int

        p1 = Point(1, 2)
        p2 = Point(2, 999)

        assert p1 != p2

    def test_when_none_field_value_then_eq_does_not_raise(self) -> None:
        @auto_eq
        @dataclass
        class OptionalThing:
            name: str | None

        t1 = OptionalThing(None)
        t2 = OptionalThing(None)
        assert t1 == t2

        t3 = OptionalThing("hello")
        assert t1 != t3

    def test_when_different_type_then_not_equal(self) -> None:
        @auto_eq
        @dataclass
        class A:
            x: int

        @auto_eq
        @dataclass
        class B:
            x: int

        assert A(1) != B(1)

    def test_when_subclass_same_fields_then_not_equal(self) -> None:
        @auto_eq
        @dataclass
        class Parent:
            x: int

        @auto_eq
        @dataclass
        class Child(Parent):
            pass

        assert Parent(1) != Child(1)

    def test_when_different_type_unrelated_then_not_equal(self) -> None:
        @auto_eq
        @dataclass
        class Point:
            x: int

        p = Point(1)
        assert p != "not a point"
        assert p != 1
        assert p != None  # noqa: E711

    def test_when_single_field_then_eq_compares_fields_individually(self) -> None:
        @auto_eq
        @dataclass
        class Single:
            value: str

        s1 = Single("hello")
        s2 = Single("hello")
        s3 = Single("world")

        assert s1 == s2
        assert s1 != s3

    def test_when_dataclass_with_default_then_default_included_in_eq(self) -> None:
        @auto_eq
        @dataclass
        class WithDefault:
            x: int
            y: int = 42

        w1 = WithDefault(1)
        w2 = WithDefault(1)

        assert w1 == w2

    def test_when_auto_hash_also_applied_then_eq_still_works(self) -> None:
        from forging_blocks.foundation.autohash.auto_hash import auto_hash

        @auto_hash
        @auto_eq
        @dataclass
        class Money:
            amount: int
            currency: str

        m1 = Money(100, "USD")
        m2 = Money(100, "USD")
        m3 = Money(200, "USD")

        assert m1 == m2
        assert m1 != m3

    def test_when_auto_eq_alone_then_no_hash_generated(self) -> None:
        @auto_eq
        @dataclass
        class Point:
            x: int

        assert Point.__auto_eq_fields__ == ("x",)
        assert Point.__dict__["__eq__"].__name__ == "__eq__"

    def test_marker_fields_set_on_class(self) -> None:
        @auto_eq
        @dataclass
        class Point:
            x: int
            y: int

        assert Point.__auto_eq_fields__ == ("x", "y")

    def test_marker_fields_when_subset_selected(self) -> None:
        @auto_eq(fields=["x"])
        @dataclass
        class Point:
            x: int
            y: int

        assert Point.__auto_eq_fields__ == ("x",)

    def test_when_slots_class_then_uses_slots(self) -> None:
        @auto_eq
        class Slotted:
            __slots__ = ("x", "y")

            def __init__(self, x: int, y: int) -> None:
                self.x = x
                self.y = y

        assert Slotted(1, 2) == Slotted(1, 2)
        assert Slotted(1, 2) != Slotted(3, 4)

    def test_when_slots_inherited_then_collects_all(self) -> None:
        @auto_eq
        class Base:
            __slots__ = ("x",)

            def __init__(self, x: int) -> None:
                self.x = x

        class Child(Base):
            __slots__ = ("y",)

            def __init__(self, x: int, y: int) -> None:
                super().__init__(x)
                self.y = y

        assert Child(1, 2) == Child(1, 2)
        assert Child(1, 2) != Child(3, 4)

    def test_when_annotations_only_then_uses_annotations(self) -> None:
        @auto_eq
        class Annotated:
            x: int
            y: int

            def __init__(self, x: int, y: int) -> None:
                self.x = x
                self.y = y

        assert Annotated(1, 2) == Annotated(1, 2)
        assert Annotated(1, 2) != Annotated(3, 4)

    def test_when_no_fields_detectable_then_raises_type_error(self) -> None:
        with pytest.raises(TypeError, match="Cannot determine eq fields"):

            @auto_eq
            class Empty:
                pass

    def test_when_explicit_fields_on_empty_class_then_succeeds(self) -> None:
        @auto_eq(fields=["x", "y"])
        class Explicit:
            def __init__(self, x: int, y: int) -> None:
                self.x = x
                self.y = y

        assert Explicit(1, 2) == Explicit(1, 2)
        assert Explicit(1, 2) != Explicit(3, 4)

    def test_when_eq_comparison_uses_getattr_not_dict(self) -> None:
        """Explicit fields path uses getattr, supporting properties and descriptors."""

        @auto_eq(fields=["_value"])
        @dataclass
        class Point:
            _value: int

            @property
            def value(self) -> int:
                return self._value

        assert Point(1) == Point(1)
        assert Point(1) != Point(2)
