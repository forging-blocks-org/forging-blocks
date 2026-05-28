import inspect

import pytest

from forging_blocks.domain import (
    DraftEntityIsNotHashableError,
)
from forging_blocks.foundation.errors.base import Error


@pytest.mark.unit
class TestDraftEntityIsNotHashableError:
    def test_from_class_name_message_starts_with_unhashable(self) -> None:
        instance = DraftEntityIsNotHashableError.from_class_name("MyEntity")

        assert str(instance.message.value).startswith("Unhashable MyEntity:")

    def test_from_class_name_includes_class_name_in_message(self) -> None:
        instance = DraftEntityIsNotHashableError.from_class_name("OrderAggregate")

        assert "OrderAggregate" in str(instance.message.value)

    def test_from_class_name_includes_draft_entities_explanation(self) -> None:
        instance = DraftEntityIsNotHashableError.from_class_name("SomeEntity")

        assert "draft entities (id=None) are not hashable" in str(instance.message.value)

    def test_from_class_name_returns_error_instance(self) -> None:
        instance = DraftEntityIsNotHashableError.from_class_name("MyEntity")

        assert isinstance(instance, Error)

    def test_from_class_name_with_empty_string(self) -> None:
        instance = DraftEntityIsNotHashableError.from_class_name("")

        assert "Unhashable" in str(instance.message.value)
        assert "draft entities (id=None) are not hashable" in str(instance.message.value)

    def test_from_class_name_with_single_char(self) -> None:
        instance = DraftEntityIsNotHashableError.from_class_name("X")

        assert str(instance.message.value) == "Unhashable X: draft entities (id=None) are not hashable"

    def test_from_class_name_with_special_characters(self) -> None:
        instance = DraftEntityIsNotHashableError.from_class_name("My.Entity_123")

        assert "My.Entity_123" in str(instance.message.value)

    def test_from_class_name_source_has_no_dead_code(self) -> None:
        """Ensure there is exactly one assignment to error_text in from_class_name.

        This catches dead code where a variable is assigned and immediately
        overwritten on the next line.
        """
        source = inspect.getsource(DraftEntityIsNotHashableError.from_class_name)
        assignments = [line for line in source.splitlines() if "error_text =" in line]

        assert len(assignments) == 1, (
            f"Expected exactly 1 assignment to 'error_text' in from_class_name, "
            f"found {len(assignments)}. Dead code detected: a variable is assigned "
            f"and immediately overwritten."
        )

