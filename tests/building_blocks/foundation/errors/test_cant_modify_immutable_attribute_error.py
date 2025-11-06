from building_blocks.foundation.errors.cant_modify_immutable_attribute_error import (
    CantModifyImmutableAttributeError,
)
from building_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata


class TestCantModifyImmutableAttributeError:
    def test_initialization(self):
        # Arrange
        attribute_name = "test_attribute"
        class_name = "TestClass"

        # Act
        error = CantModifyImmutableAttributeError(
            class_name=class_name,
            attribute_name=attribute_name,
        )

        # Assert
        expected_message = ErrorMessage(
            f"Cannot modify immutable attribute '{attribute_name}' of class '{class_name}'."
        )
        expected_metadata = ErrorMetadata(
            {
                "class_name": class_name,
                "attribute_name": attribute_name,
            }
        )
        assert expected_message == error.message
        assert expected_metadata == error.metadata
