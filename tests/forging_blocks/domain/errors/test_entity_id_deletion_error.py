import pytest

from forging_blocks.domain import EntityIdDeletionError


@pytest.mark.unit
class TestEntityIdDeletionError:
    def test_entity_id_deletion_error_populates_message_and_metadata(self) -> None:
        error = EntityIdDeletionError("User")

        assert error.message.value == (
            "Cannot delete 'id' of User as it defines the entity's identity."
        )
        assert error.metadata.context == {
            "class_name": "User",
            "attribute_name": "id",
        }
