import pytest

from forging_blocks.domain import (
    DraftEntityIsNotHashableError,
)
from forging_blocks.foundation import ErrorMessage


@pytest.mark.unit
class TestDraftEntityIsNotHashableError:
    def test_from_class_name(self) -> None:
        fake_class_name = "FakeDraftEntity"

        instance = DraftEntityIsNotHashableError.from_class_name(fake_class_name)

        assert instance.message == ErrorMessage(
            "Unhashable FakeDraftEntity: draft entities (id=None) are not hashable"
        )
