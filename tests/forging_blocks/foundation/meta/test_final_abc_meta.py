# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
"""Unit tests for FinalABCMeta metaclass."""

from __future__ import annotations

from abc import abstractmethod

import pytest

from forging_blocks.foundation.meta import FinalABCMeta, runtime_final


class AbstractBase(metaclass=FinalABCMeta):
    @runtime_final
    def sealed_method(self) -> str:
        return "base"

    @abstractmethod
    def abstract_method(self) -> str: ...

    def normal_method(self) -> str:
        return "normal"


class ConcreteChild(AbstractBase):
    def abstract_method(self) -> str:
        return "concrete"


class ChildAddingNewMethod(AbstractBase):
    def abstract_method(self) -> str:
        return "child"

    def extra_method(self) -> str:
        return "extra"


class Middle(AbstractBase):
    def abstract_method(self) -> str:
        return "middle"


class Deep(Middle):
    pass


class BaseWithMultipleSealedAndAbstract(metaclass=FinalABCMeta):
    @runtime_final
    def sealed_one(self) -> str:
        return "s1"

    @runtime_final
    def sealed_two(self) -> str:
        return "s2"

    @abstractmethod
    def abstract_one(self) -> str: ...

    @abstractmethod
    def abstract_two(self) -> str: ...


class ConcreteMulti(BaseWithMultipleSealedAndAbstract):
    def abstract_one(self) -> str:
        return "a1"

    def abstract_two(self) -> str:
        return "a2"


class BaseWithOnlyAbstract(metaclass=FinalABCMeta):
    @abstractmethod
    def do_work(self) -> str: ...


class ConcreteOnly(BaseWithOnlyAbstract):
    def do_work(self) -> str:
        return "done"


class IncompleteOnly(BaseWithOnlyAbstract):
    pass


class BaseWithOnlySealed(metaclass=FinalABCMeta):
    @runtime_final
    def do_work(self) -> str:
        return "sealed"


class PlainBase(metaclass=FinalABCMeta):
    def ordinary(self) -> str:
        return "plain"


class CustomPlain(PlainBase):
    def ordinary(self) -> str:
        return "custom"


class CustomChild(AbstractBase):
    def abstract_method(self) -> str:
        return "custom"

    def normal_method(self) -> str:
        return "overridden"


class Incomplete(AbstractBase):
    pass


@pytest.mark.unit
class TestFinalABCMetaAbstractEnforcement:
    def test_instantiating_base_with_abstract_method_raises_type_error(self) -> None:
        with pytest.raises(TypeError):
            AbstractBase()  # type: ignore[abstract]

    def test_concrete_child_instantiates(self) -> None:
        instance = ConcreteChild()
        assert instance.abstract_method() == "concrete"

    def test_child_providing_abstract_method_instantiates(self) -> None:
        instance = ChildAddingNewMethod()
        assert instance.abstract_method() == "child"
        assert instance.extra_method() == "extra"

    def test_inheriting_abstract_without_implementation_raises_type_error(self) -> None:
        with pytest.raises(TypeError):
            Incomplete()  # type: ignore[abstract]


@pytest.mark.unit
class TestFinalABCMetaRuntimeFinalEnforcement:
    def test_overriding_sealed_method_raises_type_error(self) -> None:
        with pytest.raises(TypeError, match="runtime-final"):

            class _(AbstractBase):
                def sealed_method(self) -> str:
                    return "bad"

                def abstract_method(self) -> str:
                    return "impl"

    def test_overriding_multiple_sealed_methods_raises_type_error(self) -> None:
        with pytest.raises(TypeError, match="runtime-final"):

            class _(BaseWithMultipleSealedAndAbstract):
                def sealed_one(self) -> str:
                    return "bad"

                def sealed_two(self) -> str:
                    return "bad"

                def abstract_one(self) -> str:
                    return "a1"

                def abstract_two(self) -> str:
                    return "a2"

    def test_overriding_second_sealed_method_raises_type_error(self) -> None:
        with pytest.raises(TypeError, match="runtime-final"):

            class _(BaseWithMultipleSealedAndAbstract):
                def sealed_one(self) -> str:
                    return "ok"

                def sealed_two(self) -> str:
                    return "bad"

                def abstract_one(self) -> str:
                    return "a1"

                def abstract_two(self) -> str:
                    return "a2"

    def test_override_blocked_at_deep_inheritance_level(self) -> None:
        with pytest.raises(TypeError, match="runtime-final"):

            class _(Deep):
                def sealed_method(self) -> str:
                    return "bad"

    def test_child_without_override_succeeds(self) -> None:
        instance = ConcreteChild()
        assert instance.sealed_method() == "base"

    def test_deep_child_without_override_succeeds(self) -> None:
        instance = Deep()
        assert instance.sealed_method() == "base"


@pytest.mark.unit
class TestFinalABCMetaCombinedBehavior:
    def test_sealed_method_returns_correct_value(self) -> None:
        instance = ConcreteChild()
        assert instance.sealed_method() == "base"

    def test_abstract_method_returns_child_implementation(self) -> None:
        instance = ConcreteChild()
        assert instance.abstract_method() == "concrete"

    def test_normal_method_is_overridable(self) -> None:
        instance = CustomChild()
        assert instance.normal_method() == "overridden"

    def test_instantiating_class_with_only_abstract_succeeds_when_implemented(self) -> None:
        assert ConcreteOnly().do_work() == "done"

    def test_instantiating_class_with_only_sealed_succeeds(self) -> None:
        instance = BaseWithOnlySealed()
        assert instance.do_work() == "sealed"

    def test_instantiating_class_with_only_abstract_fails_without_implementation(self) -> None:
        with pytest.raises(TypeError):
            IncompleteOnly()  # type: ignore[abstract]

    def test_plain_base_with_no_abstract_or_sealed_instantiates(self) -> None:
        instance = PlainBase()
        assert instance.ordinary() == "plain"

    def test_overriding_normal_method_on_plain_base_succeeds(self) -> None:
        instance = CustomPlain()
        assert instance.ordinary() == "custom"
