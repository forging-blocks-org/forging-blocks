from building_blocks.domain.errors.entity_id_none_error import EntityIdNoneError


class TestEntityIdNoneError:
    def test_entity_id_none_error_message(self):
        # Arrange
        actual_fake_class_name = "FakeClassName"

        # Action
        error = EntityIdNoneError(actual_fake_class_name)

        # Assert
        assert error.message.value == (
            f"Entity ID have to be defined for '{actual_fake_class_name}'."
        )
        assert error.metadata.context["entity_class_name"] == actual_fake_class_name
