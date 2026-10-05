import pytest

from forging_blocks.domain import EntityIdModificationError


@pytest.mark.unit
class TestEntityIdModificationError:
    def test_entity_id_modification_error_populates_message_and_metadata(self) -> None:
        error = EntityIdModificationError("User", "_id", 42)

        assert error.message.value == ("Cannot modify '_id' of User once set (current value=42).")
        assert error.metadata.context == {
            "class_name": "User",
            "attribute_name": "_id",
            "current_value": 42,
        }
