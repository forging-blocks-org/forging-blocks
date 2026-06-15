# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
"""Tests for the auto_freeze decorator."""

from __future__ import annotations

from typing import Any

import pytest

from forging_blocks.foundation.autofreeze.auto_freeze import auto_freeze
from forging_blocks.foundation.errors.cant_modify_immutable_attribute_error import (
    CantModifyImmutableAttributeError,
)

# ---------------------------------------------------------------------------
# Tests for the auto_freeze decorator
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAutoFreezeDecorator:
    """Tests for the auto_freeze decorator public API."""

    # -- Usage modes --------------------------------------------------------

    def test_when_used_without_parentheses_then_decorates_class(self) -> None:
        class MyClass:
            def __init__(self) -> None:
                pass

        decorated = auto_freeze(MyClass)
        assert decorated is MyClass

    def test_when_used_with_empty_parentheses_then_returns_decorator(self) -> None:
        class MyClass:
            def __init__(self) -> None:
                pass

        decorator = auto_freeze()
        decorated = decorator(MyClass)
        assert decorated is MyClass

    def test_when_used_with_attrs_then_returns_decorator(self) -> None:
        class MyClass:
            def __init__(self) -> None:
                pass

        decorator = auto_freeze(attrs=["_id"])
        decorated = decorator(MyClass)
        assert decorated is MyClass

    def test_when_class_already_decorated_then_returns_same_class(self) -> None:
        class MyClass:
            def __init__(self) -> None:
                pass

        first = auto_freeze(MyClass)
        second = auto_freeze(first)
        assert first is second

    # -- Freeze behavior ----------------------------------------------------

    def test_when_attrs_is_none_then_freezes_entire_instance(self) -> None:
        class MyClass:
            def __init__(self, value: int) -> None:
                self.value = value

        decorated = auto_freeze(MyClass)
        instance = decorated(42)

        assert instance.value == 42

        with pytest.raises(CantModifyImmutableAttributeError):
            instance.value = 99

    def test_when_attrs_provided_then_only_freezes_specified_attributes(self) -> None:
        class MyClass:
            def __init__(self, id_: int, name: str) -> None:
                self.id = id_
                self.name = name

        decorated = auto_freeze(attrs=["id"])(MyClass)
        instance = decorated(1, "test")

        with pytest.raises(CantModifyImmutableAttributeError):
            instance.id = 99

        instance.name = "new name"
        assert instance.name == "new name"

    def test_when_init_raises_then_instance_not_frozen(self) -> None:
        class MyClass:
            def __init__(self, value: int) -> None:
                if value < 0:
                    raise ValueError("fail")
                self.value = value

        decorated = auto_freeze(MyClass)

        with pytest.raises(ValueError, match="fail"):
            decorated(-1)

    # -- Selective freezing -------------------------------------------------

    def test_when_attrs_is_list_then_only_those_attributes_frozen(self) -> None:
        class MyClass:
            def __init__(self, a: int, b: int, c: int) -> None:
                self.a = a
                self.b = b
                self.c = c

        decorated = auto_freeze(attrs=["a", "b"])(MyClass)
        instance = decorated(1, 2, 3)

        with pytest.raises(CantModifyImmutableAttributeError):
            instance.a = 99
        with pytest.raises(CantModifyImmutableAttributeError):
            instance.b = 99

        instance.c = 99
        assert instance.c == 99

    def test_when_attrs_is_empty_list_then_no_attributes_frozen(self) -> None:
        class MyClass:
            def __init__(self, a: int) -> None:
                self.a = a

        decorated = auto_freeze(attrs=[])(MyClass)
        instance = decorated(1)

        instance.a = 99
        assert instance.a == 99

    # -- Abstract classes ---------------------------------------------------

    def test_when_class_is_abstract_then_not_frozen(self) -> None:
        from abc import ABC, abstractmethod

        class AbstractBase(ABC):
            @abstractmethod
            def do_something(self) -> None:
                pass

        auto_freeze(AbstractBase)

        @auto_freeze
        class Concrete(AbstractBase):
            def __init__(self, value: int) -> None:
                self.value = value

            def do_something(self) -> None:
                pass

        instance = Concrete(42)
        assert instance.value == 42

        with pytest.raises(CantModifyImmutableAttributeError):
            instance.value = 99

    # -- Existing __setattr__ preservation ----------------------------------

    def test_when_class_has_custom_setattr_then_class_handles_freezing(self) -> None:
        """When a class has custom __setattr__, it must handle frozen checks itself."""

        class MyClass:
            def __init__(self, value: int) -> None:
                self._value = value

            def __setattr__(self, name: str, value: Any) -> None:
                # Frozen check must come FIRST for frozen objects
                if getattr(self, "_autofreeze__frozen", False):
                    raise CantModifyImmutableAttributeError(
                        class_name=self.__class__.__name__,
                        attribute_name=name,
                    )
                # Custom validation
                if name == "_value" and value < 0:
                    raise ValueError("value must be non-negative")
                object.__setattr__(self, name, value)

        decorated = auto_freeze(MyClass)
        instance = decorated(10)

        # Custom validation works during __init__ (before freeze)
        # After freeze, class's own frozen check blocks modifications
        with pytest.raises(CantModifyImmutableAttributeError):
            instance._value = -5

        with pytest.raises(CantModifyImmutableAttributeError):
            instance._value = 20

        with pytest.raises(CantModifyImmutableAttributeError):
            instance._value = 30

    def test_when_class_has_slots_then_works_correctly(self) -> None:
        class Slotted:
            __slots__ = (
                "_value",
                "_autofreeze__frozen",
                "_autofreeze__frozen_attrs",
                "_autofreeze__init_depth",
            )

            def __init__(self, value: int) -> None:
                self._value = value

        decorated = auto_freeze(Slotted)
        instance = decorated(42)

        with pytest.raises(CantModifyImmutableAttributeError):
            instance._value = 99

    # -- Inheritance (requires manual decorator on each class) -------------

    def test_when_subclass_also_decorated_then_frozen_independently(self) -> None:
        @auto_freeze
        class Base:
            def __init__(self, value: int) -> None:
                self.value = value

        @auto_freeze
        class Child(Base):
            def __init__(self, value: int, extra: str) -> None:
                super().__init__(value)
                self.extra = extra

        instance = Child(1, "test")

        with pytest.raises(CantModifyImmutableAttributeError):
            instance.value = 99
        with pytest.raises(CantModifyImmutableAttributeError):
            instance.extra = "hacked"

    def test_when_freeze_instance_is_async_then_still_works(self) -> None:
        class AsyncFreeze:
            def __init__(self) -> None:
                pass

            async def some_async_method(self) -> None:
                pass

        decorated = auto_freeze(AsyncFreeze)
        instance = decorated()
        assert instance is not None

    # -- super().__init__ chaining -----------------------------------------

    def test_when_super_init_chaining_then_freezes_at_end(self) -> None:
        from abc import ABC, abstractmethod

        @auto_freeze
        class Base(ABC):
            @abstractmethod
            def base_method(self) -> None:
                pass

            def __init__(self, value: int) -> None:
                self.base_value = value

        @auto_freeze
        class Child(Base):
            def __init__(self, value: int, extra: str) -> None:
                super().__init__(value)
                self.extra = extra

            def base_method(self) -> None:
                pass

        instance = Child(42, "test")
        assert instance.base_value == 42
        assert instance.extra == "test"

        with pytest.raises(CantModifyImmutableAttributeError):
            instance.base_value = 99
        with pytest.raises(CantModifyImmutableAttributeError):
            instance.extra = "hacked"
