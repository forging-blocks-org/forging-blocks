from building_blocks.domain.errors.draft_entity_is_not_hashable_error import (
    DraftEntityIsNotHashableError,
)
from building_blocks.foundation.errors.core import ErrorMessage


class TestDraftEntityIsNotHashableError:
    def test_from_class_name(self) -> None:
        fake_class_name = "FakeDraftEntity"

        instance = DraftEntityIsNotHashableError.from_class_name(fake_class_name)

        assert instance.message == ErrorMessage(
            "Unhashable FakeDraftEntity: draft entities (id=None) are not hashable"
        )
