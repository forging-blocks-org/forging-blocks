import pytest

from forging_blocks.domain import Entity, EntityIdDeletionError, EntityIdModificationError


class User(Entity[int]):
    def __init__(self, entity_id: int | None = None, name: str = "") -> None:
        super().__init__(entity_id)
        self.name = name


class Order(Entity[int]):
    def __init__(self, order_id: int) -> None:
        self._id = order_id


@pytest.fixture
def draft_user() -> User:
    return User(None, "Alice")


@pytest.mark.unit
class TestDraftUserLifecycle:
    def test___delattr___when_draft_entity_then_raises_entity_id_deletion_error(
        self,
        draft_user: User,
    ) -> None:
        with pytest.raises(EntityIdDeletionError) as exc_info:
            draft_user.__delattr__("_id")

        assert "Cannot delete" in str(exc_info.value)
        assert exc_info.value.context["class_name"] == "User"
        assert exc_info.value.context["attribute_name"] == "id"

    def test___setattr___when_draft_entity_then_allows_id_assignment(
        self,
        draft_user: User,
    ) -> None:
        draft_user._id = 42

        assert draft_user.id == 42
        assert draft_user.is_persisted() is True

    def test___setattr___when_draft_entity_then_allows_same_id_reassignment(
        self,
        draft_user: User,
    ) -> None:
        draft_user.__setattr__("_id", 42)
        draft_user.__setattr__("_id", 42)

        assert draft_user.id == 42

    def test___setattr___when_draft_entity_then_blocks_different_id_after_persist(
        self,
        draft_user: User,
    ) -> None:
        draft_user.__setattr__("_id", 42)

        with pytest.raises(EntityIdModificationError):
            draft_user.__setattr__("_id", 99)

    def test___setattr___when_id_assigned_before_freeze_then_allows_assignment(
        self,
    ) -> None:
        order = Order(42)

        assert order.id == 42
        assert order.is_persisted() is True

        with pytest.raises(EntityIdModificationError):
            order.__setattr__("_id", 99)
