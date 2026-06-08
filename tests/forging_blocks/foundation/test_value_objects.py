# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest

from forging_blocks.foundation import CantModifyImmutableAttributeError
from forging_blocks.foundation.value_object import ValueObject


class Email(ValueObject[str]):
    __slots__ = ("_value",)

    def __init__(self, value: str):
        super().__init__()
        if "@" not in value:
            raise ValueError("Invalid email format")
        self._value = value
        self._freeze()

    @property
    def value(self) -> str:
        return self._value

    @property
    def _equality_components(self) -> tuple[str]:
        return (self._value,)


class AnotherEmailType(ValueObject[str]):
    __slots__ = ("_value",)

    def __init__(self, value: str):
        super().__init__()
        if "@" not in value:
            raise ValueError("Invalid email format")
        self._value = value
        self._freeze()

    @property
    def value(self) -> str:
        return self._value

    @property
    def _equality_components(self) -> tuple[str]:
        return (self._value,)


class MultiComponentVO(ValueObject[str]):
    """Value object with multiple equality components for testing __str__ branch."""

    __slots__ = ("_first", "_second")

    def __init__(self, first: str, second: str) -> None:
        super().__init__()
        self._first = first
        self._second = second
        self._freeze()

    @property
    def value(self) -> str:
        return f"{self._first}:{self._second}"

    @property
    def _equality_components(self) -> tuple[str, str]:
        return (self._first, self._second)


@pytest.mark.unit
class TestValueObject:
    def test___init___when_invalid_email_then_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            Email("invalid")

    def test___setattr___when_object_is_frozen_then_raises_cant_modify_immutable_error(
        self,
    ) -> None:
        email = Email("a@example.com")
        with pytest.raises(CantModifyImmutableAttributeError):
            email._value = "b@example.com"  # type: ignore

    def test___eq___when_values_are_equal_then_returns_true(self) -> None:
        e1 = Email("a@example.com")
        e2 = Email("a@example.com")
        assert e1 == e2

    def test___eq___when_values_differ_then_returns_false(self) -> None:
        e1 = Email("a@example.com")
        e2 = Email("b@example.com")
        assert e1 != e2

    def test___eq___when_values_equal_but_different_type_then_returns_false(
        self,
    ) -> None:
        e1 = Email("a@example.com")
        e2 = AnotherEmailType("b@example.com")
        assert e1 != e2

    def test___hash___when_values_are_equal_then_hashes_match(self) -> None:
        e1 = Email("a@example.com")
        e2 = Email("a@example.com")
        assert hash(e1) == hash(e2)

    def test___str___when_called_then_returns_readable_string(self) -> None:
        e = Email("a@example.com")
        assert "a@example.com" in str(e)

    def test___repr___when_called_then_returns_same_as_str(self) -> None:
        e = Email("a@example.com")
        assert repr(e) == str(e)

    def test_value_property_when_called_then_returns_underlying_value(self) -> None:
        e = Email("a@example.com")
        assert e.value == "a@example.com"

    def test___str___when_multiple_components_then_returns_tuple_representation(
        self,
    ) -> None:
        vo = MultiComponentVO("hello", "world")

        result = str(vo)

        assert "MultiComponentVO" in result
        assert "hello" in result
        assert "world" in result

    def test___eq___when_multi_component_values_equal_then_returns_true(self) -> None:
        vo1 = MultiComponentVO("hello", "world")
        vo2 = MultiComponentVO("hello", "world")

        assert vo1 == vo2

    def test___eq___when_multi_component_values_differ_then_returns_false(self) -> None:
        vo1 = MultiComponentVO("hello", "world")
        vo2 = MultiComponentVO("hello", "mars")

        assert vo1 != vo2

    def test___hash___when_multi_component_values_equal_then_hashes_match(self) -> None:
        vo1 = MultiComponentVO("hello", "world")
        vo2 = MultiComponentVO("hello", "world")

        assert hash(vo1) == hash(vo2)

    def test___setattr___when_multi_component_is_frozen_then_raises_cant_modify_immutable(
        self,
    ) -> None:
        vo = MultiComponentVO("hello", "world")

        with pytest.raises(CantModifyImmutableAttributeError):
            vo._first = "changed"  # type: ignore
