import pytest

from forging_blocks.domain import (
    Entity,
    EntityIdDeletionError,
    EntityIdModificationError,
)
from forging_blocks.foundation import CantModifyImmutableAttributeError


class User(Entity[int]):
    def __init__(self, entity_id: int | None = None, name: str = "") -> None:
        super().__init__(entity_id)
        self.name = name


@pytest.mark.unit
class TestEntity:
    @pytest.fixture
    def draft_user(self) -> User:
        return User(None, "Alice")

    @pytest.fixture
    def persisted_user(self) -> User:
        return User(1, "Alice")

    def test___init___when_id_is_none_then_creates_draft_entity(
        self,
        draft_user: User,
    ) -> None:
        result = draft_user.id

        assert result is None

    def test___init___when_id_is_defined_then_assigns_id_correctly(
        self,
        persisted_user: User,
    ) -> None:
        result = persisted_user.id

        assert result == 1

    def test___setattr___when_trying_to_modify_id_then_raises_entity_id_modification_error(
        self,
        persisted_user: User,
    ) -> None:
        new_id = 99

        with pytest.raises(EntityIdModificationError) as exc_info:
            persisted_user.__setattr__("_id", new_id)

        assert "Cannot modify" in str(exc_info.value)
        assert exc_info.value.context["class_name"] == "User"
        assert exc_info.value.context["attribute_name"] == "_id"
        assert exc_info.value.context["current_value"] == 1

    def test___setattr___when_setting_same_id_value_then_allows_copy_safe_reassign(
        self,
        persisted_user: User,
    ) -> None:
        same_id = persisted_user.id

        persisted_user.__setattr__("_id", same_id)

        assert persisted_user.id == same_id

    def test___setattr___when_setting_non_id_attribute_then_allows_assignment(
        self,
        persisted_user: User,
    ) -> None:
        new_name = "Bob"

        persisted_user.__setattr__("name", new_name)

        assert persisted_user.name == new_name

    def test___delattr___when_deleting_id_then_raises_entity_id_deletion_error(
        self,
        persisted_user: User,
    ) -> None:
        with pytest.raises(EntityIdDeletionError) as exc_info:
            persisted_user.__delattr__("_id")

        assert "Cannot delete" in str(exc_info.value)
        assert exc_info.value.context["class_name"] == "User"
        assert exc_info.value.context["attribute_name"] == "id"

    def test___delattr___when_deleting_non_id_attribute_then_deletes_successfully(
        self,
        persisted_user: User,
    ) -> None:
        persisted_user.extra = "data"

        persisted_user.__delattr__("extra")

        assert not hasattr(persisted_user, "extra")

    def test_is_persisted_when_id_is_none_then_returns_false(
        self,
        draft_user: User,
    ) -> None:
        result = draft_user.is_persisted()

        assert result is False

    def test_is_persisted_when_id_defined_then_returns_true(
        self,
        persisted_user: User,
    ) -> None:
        result = persisted_user.is_persisted()

        assert result is True

    def test___delattr___when_deleting_frozen_attrs_marker_then_raises_and_keeps_id_protected(
        self,
    ) -> None:
        persisted_user = User(1, "Alice")

        with pytest.raises(CantModifyImmutableAttributeError):
            delattr(persisted_user, "_autofreeze__frozen_attrs")

        with pytest.raises(EntityIdModificationError):
            persisted_user.__setattr__("_id", 99)

    def test___setattr___when_modifying_frozen_attrs_marker_then_raises_and_keeps_id_protected(
        self,
    ) -> None:
        persisted_user = User(1, "Alice")

        with pytest.raises(CantModifyImmutableAttributeError):
            persisted_user.__setattr__("_autofreeze__frozen_attrs", set[str]())

        with pytest.raises(EntityIdModificationError):
            persisted_user.__setattr__("_id", 99)
