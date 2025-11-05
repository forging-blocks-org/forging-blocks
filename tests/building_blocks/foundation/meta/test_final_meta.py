"""Unit tests for FinalMeta and runtime_final decorators."""

from __future__ import annotations

import pytest

from building_blocks.foundation.meta.final_meta import FinalMeta, runtime_final


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


class EmptyBase(metaclass=FinalMeta):
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


class StandaloneBaseWithFinal(metaclass=FinalMeta):
    @runtime_final
    def final_method(self) -> str:
        return "base"


# Helper class for testing method functionality
class SampleClassWithRuntimeFinalMethod:
    @runtime_final
    def test_method(self, value: int) -> int:
        return value * 2


class TestFinalMeta:
    def test___new___when_no_final_methods_overridden_then_creates_class(self) -> None:
        # Arrange
        # (ChildOverridingNormalMethod already defined)

        # Action
        instance = ChildOverridingNormalMethod()

        # Assert
        assert instance.normal_method() == "overridden"
        assert instance.final_method() == "base"

    def test___new___when_final_method_overridden_then_raises_type_error(self) -> None:
        # Arrange
        # (BaseWithFinalMethod already defined)

        # Action & Assert
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
        # Arrange
        # (BaseWithMultipleFinalMethods already defined)

        # Action & Assert
        with pytest.raises(
            TypeError, match="Cannot override runtime-final method 'final_method_one'"
        ):

            class Child(BaseWithMultipleFinalMethods):
                def final_method_one(self) -> str:
                    return "overridden"

    def test___new___when_final_method_inherited_then_raises_type_error(self) -> None:
        # Arrange
        # (DirectChildOfGrandParent already defined)

        # Action & Assert
        with pytest.raises(
            TypeError,
            match="Cannot override runtime-final method 'final_method' in subclass 'GrandChild'",
        ):

            class GrandChild(DirectChildOfGrandParent):
                def final_method(self) -> str:
                    return "overridden"

    def test___new___when_no_base_classes_then_creates_class(self) -> None:
        # Arrange
        # (StandaloneBaseWithFinal already defined)

        # Action
        instance = StandaloneBaseWithFinal()

        # Assert
        assert instance.final_method() == "base"

    def test___new___when_non_final_method_in_base_then_allows_override(self) -> None:
        # Arrange
        # (ChildOverridingNonFinalMethod already defined)

        # Action
        instance = ChildOverridingNonFinalMethod()

        # Assert
        assert instance.non_final_method() == "child"

    def test___new___when_final_method_not_in_namespace_then_creates_class(
        self,
    ) -> None:
        # Arrange
        # (ChildWithAdditionalMethod already defined)

        # Action
        instance = ChildWithAdditionalMethod()

        # Assert
        assert instance.final_method() == "base"
        assert instance.another_method() == "another"


class TestRuntimeFinal:
    def test_runtime_final_when_applied_to_function_then_sets_final_attribute(
        self,
    ) -> None:
        # Arrange
        def sample_function() -> str:
            return "test"

        # Action
        decorated = runtime_final(sample_function)

        # Assert
        assert hasattr(decorated, "__final__")
        assert decorated.__final__ is True

    def test_runtime_final_when_applied_to_function_then_sets_is_runtime_final_attribute(
        self,
    ) -> None:
        # Arrange
        def sample_function() -> str:
            return "test"

        # Action
        decorated = runtime_final(sample_function)

        # Assert
        assert hasattr(decorated, "__is_runtime_final__")
        assert decorated.__is_runtime_final__ is True

    def test_runtime_final_when_applied_to_function_then_returns_same_function(
        self,
    ) -> None:
        # Arrange
        def sample_function() -> str:
            return "test"

        # Action
        decorated = runtime_final(sample_function)

        # Assert
        assert decorated() == "test"
        assert decorated.__name__ == "sample_function"

    def test_runtime_final_when_applied_to_method_then_preserves_functionality(
        self,
    ) -> None:
        # Arrange
        instance = SampleClassWithRuntimeFinalMethod()

        # Action
        result = instance.test_method(5)

        # Assert
        assert result == 10

    def test_runtime_final_when_applied_to_classmethod_then_sets_attributes(
        self,
    ) -> None:
        # Arrange
        @classmethod
        def sample_classmethod(cls) -> str:
            return "test"

        # Action
        decorated = runtime_final(sample_classmethod)

        # Assert
        assert hasattr(decorated, "__is_runtime_final__")
        assert decorated.__is_runtime_final__ is True

    def test_runtime_final_when_applied_to_staticmethod_then_sets_attributes(
        self,
    ) -> None:
        # Arrange
        @staticmethod
        def sample_staticmethod() -> str:
            return "test"

        # Action
        decorated = runtime_final(sample_staticmethod)

        # Assert
        assert hasattr(decorated, "__is_runtime_final__")
        assert decorated.__is_runtime_final__ is True
