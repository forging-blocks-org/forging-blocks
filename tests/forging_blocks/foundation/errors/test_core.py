import pytest

from forging_blocks.foundation import (
    ErrorMetadata,
)


class TestErrorMetadata:
    def test_context_when_context_defined_then_context_equals_to_argument(self) -> None:
        context = {"key": "value"}

        metadata = ErrorMetadata(context=context)

        expected_context = {"key": "value"}
        assert metadata.context == expected_context

    def test_context_when_reassigning_then_raises_attribute_error(self) -> None:
        metadata = ErrorMetadata(context={"key": "value"})

        with pytest.raises(AttributeError):
            metadata.context = {"new_key": "new_value"}  # type: ignore[assignment]

    def test_context_when_mutating_dictionary_then_succeeds(self) -> None:
        metadata = ErrorMetadata(context={"key": "value"})
        new_value = "new_value"

        metadata.context["key"] = new_value

        assert metadata.context["key"] == new_value
