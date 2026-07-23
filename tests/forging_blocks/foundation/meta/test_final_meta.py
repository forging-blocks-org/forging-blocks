# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportUnknownLambdaType=false
"""Unit tests for FinalMeta and runtime_final decorators."""

from __future__ import annotations

from typing import cast

import pytest

from forging_blocks.foundation import FinalMeta, runtime_final
from forging_blocks.foundation.meta.final_meta import validate_no_runtime_final_override


class BaseWithFinalMethod(metaclass=FinalMeta):
    @runtime_final
    def final_method(self) -> str:
        return "base"

    def normal_method(self) -> str:
        return "normal"


class BaseWithMultipleFinalMethods(metaclass=FinalMeta):
    @runtime_final
    def final_method_one(self) -> str:
        return "one"

    @runtime_final
    def final_method_two(self) -> str:
        return "two"


class GrandParentWithFinalMethod(metaclass=FinalMeta):
    @runtime_final
    def final_method(self) -> str:
        return "grandparent"


class DirectChildOfGrandParent(GrandParentWithFinalMethod):
    pass


class BaseWithOnlyNormalMethod(metaclass=FinalMeta):
    def non_final_method(self) -> str:
        return "base"


class StandaloneBaseWithFinal(metaclass=FinalMeta):
    @runtime_final
    def final_method(self) -> str:
        return "base"


class ChildOverridingNormalMethod(BaseWithFinalMethod):
    def normal_method(self) -> str:
        return "overridden"


class ChildOverridingNonFinalMethod(BaseWithOnlyNormalMethod):
    def non_final_method(self) -> str:
        return "child"


class ChildWithAdditionalMethod(BaseWithFinalMethod):
    def another_method(self) -> str:
        return "another"


class ClassWithRuntimeFinalMethod:
    @runtime_final
    def test_method(self, value: int) -> int:
        return value * 2


class HelperBaseWithFinal:
    @runtime_final
    def final_method(self) -> str:
        return "base"


class HelperBasePlain:
    def normal_method(self) -> str:
        return "normal"


class HelperGrandParentFinal:
    @runtime_final
    def deep_method(self) -> str:
        return "deep"


class HelperBaseWithTwoFinals:
    @runtime_final
    def method_a(self) -> str:
        return "a"

    @runtime_final
    def method_b(self) -> str:
        return "b"


@pytest.mark.unit
class TestFinalMeta:
    def test___new___when_no_final_methods_overridden_then_creates_class(self) -> None:
        instance = ChildOverridingNormalMethod()
        assert instance.normal_method() == "overridden"
        assert instance.final_method() == "base"

    def test___new___when_final_method_overridden_then_raises_type_error(self) -> None:
        with pytest.raises(
            TypeError,
            match="Cannot override runtime-final method 'final_method' in subclass 'Child'",
        ):

            class Child(BaseWithFinalMethod):
                def final_method(self) -> str:
                    return "overridden"

    def test___new___when_multiple_final_methods_one_overridden_then_raises_type_error(
        self,
    ) -> None:
        with pytest.raises(
            TypeError, match="Cannot override runtime-final method 'final_method_one'"
        ):

            class Child(BaseWithMultipleFinalMethods):
                def final_method_one(self) -> str:
                    return "overridden"

    def test___new___when_final_method_inherited_then_raises_type_error(self) -> None:
        with pytest.raises(
            TypeError,
            match="Cannot override runtime-final method 'final_method' in subclass 'GrandChild'",
        ):

            class GrandChild(DirectChildOfGrandParent):
                def final_method(self) -> str:
                    return "overridden"

    def test___new___when_no_base_classes_then_creates_class(self) -> None:
        instance = StandaloneBaseWithFinal()
        assert instance.final_method() == "base"

    def test___new___when_non_final_method_in_base_then_allows_override(self) -> None:
        instance = ChildOverridingNonFinalMethod()
        assert instance.non_final_method() == "child"

    def test___new___when_final_method_not_in_namespace_then_creates_class(
        self,
    ) -> None:
        instance = ChildWithAdditionalMethod()
        assert instance.final_method() == "base"
        assert instance.another_method() == "another"


@pytest.mark.unit
class TestValidateNoRuntimeFinalOverride:
    def test_when_no_bases_then_returns_none(self) -> None:
        assert cast(object, validate_no_runtime_final_override("MyClass", (), {"x": 1})) is None

    def test_when_base_has_final_method_not_overridden_then_returns_none(
        self,
    ) -> None:
        assert (
            cast(
                object,
                validate_no_runtime_final_override(
                    "Child", (HelperBaseWithFinal,), {"other_method": lambda: None}
                ),
            )
            is None
        )

    def test_when_base_has_final_method_overridden_then_raises_type_error(
        self,
    ) -> None:
        with pytest.raises(TypeError, match="runtime-final method 'final_method'"):
            validate_no_runtime_final_override(
                "Child",
                (HelperBaseWithFinal,),
                {"final_method": lambda self: "overridden"},
            )

    def test_when_base_has_no_final_methods_then_returns_none(self) -> None:
        assert (
            cast(
                object,
                validate_no_runtime_final_override(
                    "Child",
                    (HelperBasePlain,),
                    {"normal_method": lambda self: "overridden"},
                ),
            )
            is None
        )

    def test_error_message_contains_subclass_name(self) -> None:
        with pytest.raises(TypeError, match="in subclass 'BadChild'"):
            validate_no_runtime_final_override(
                "BadChild",
                (HelperBaseWithFinal,),
                {"final_method": lambda self: "bad"},
            )

    def test_when_final_method_from_grandparent_overridden_then_raises_type_error(
        self,
    ) -> None:
        with pytest.raises(TypeError, match="runtime-final method 'deep_method'"):
            validate_no_runtime_final_override(
                "BadDeep",
                (HelperGrandParentFinal,),
                {"deep_method": lambda self: "bad"},
            )

    def test_when_multiple_bases_and_one_final_overridden_then_raises_type_error(
        self,
    ) -> None:
        with pytest.raises(TypeError, match="runtime-final method 'method_a'"):
            validate_no_runtime_final_override(
                "MultiChild",
                (HelperBaseWithTwoFinals, HelperBasePlain),
                {"method_a": lambda self: "overridden"},
            )

    def test_when_namespace_has_new_method_not_in_bases_then_returns_none(
        self,
    ) -> None:
        assert (
            cast(
                object,
                validate_no_runtime_final_override(
                    "Child",
                    (HelperBaseWithFinal,),
                    {"brand_new_method": lambda self: 42},
                ),
            )
            is None
        )


@pytest.mark.unit
class TestRuntimeFinal:
    def test_runtime_final_when_applied_to_function_then_sets_final_attribute(
        self,
    ) -> None:
        def sample_function() -> str:
            return "test"

        decorated = runtime_final(sample_function)
        assert hasattr(decorated, "__final__")
        assert decorated.__final__ is True

    def test_runtime_final_when_applied_to_function_then_sets_is_runtime_final_attribute(
        self,
    ) -> None:
        def sample_function() -> str:
            return "test"

        decorated = runtime_final(sample_function)

        assert hasattr(decorated, "__is_runtime_final__")
        assert decorated.__is_runtime_final__ is True

    def test_runtime_final_when_applied_to_function_then_returns_same_function(
        self,
    ) -> None:
        def sample_function() -> str:
            return "test"

        decorated = runtime_final(sample_function)

        assert decorated() == "test"
        assert decorated.__name__ == "sample_function"

    def test_runtime_final_when_applied_to_method_then_preserves_functionality(
        self,
    ) -> None:
        instance = ClassWithRuntimeFinalMethod()

        result = instance.test_method(5)

        assert result == 10

    def test_runtime_final_when_applied_to_classmethod_then_sets_attributes(
        self,
    ) -> None:
        class _:
            @classmethod
            def sample_classmethod(cls) -> str:
                return "test"

        decorated = runtime_final(_.__dict__["sample_classmethod"])

        assert hasattr(decorated, "__is_runtime_final__")
        assert decorated.__is_runtime_final__ is True

    def test_runtime_final_when_applied_to_staticmethod_then_sets_attributes(
        self,
    ) -> None:
        class _:
            @staticmethod
            def sample_staticmethod() -> str:
                return "test"

        decorated = runtime_final(_.__dict__["sample_staticmethod"])

        assert hasattr(decorated, "__is_runtime_final__")
        assert decorated.__is_runtime_final__ is True
