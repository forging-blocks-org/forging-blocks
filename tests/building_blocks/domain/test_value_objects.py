import pytest

from building_blocks.domain.value_object import ValueObject


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

    def _equality_components(self) -> tuple[str]:
        return (self._value,)


class TestValueObject:
    def test___init___when_invalid_email_then_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            Email("invalid")

    def test___setattr___when_object_is_frozen_then_raises_attribute_error(
        self,
    ) -> None:
        email = Email("a@example.com")
        with pytest.raises(AttributeError):
            email._value = "b@example.com"  # type: ignore

    def test___eq___when_values_are_equal_then_returns_true(self) -> None:
        e1 = Email("a@example.com")
        e2 = Email("a@example.com")
        assert e1 == e2

    def test___eq___when_values_differ_then_returns_false(self) -> None:
        e1 = Email("a@example.com")
        e2 = Email("b@example.com")
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
