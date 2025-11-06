import pytest

from building_blocks.domain.entity import Entity
from building_blocks.domain.errors.draft_entity_is_not_hashable_error import (
    DraftEntityIsNotHashableError,
)


class User(Entity[int]):
    def __init__(self, entity_id: int | None = None, name: str = "") -> None:
        super().__init__(entity_id)
        self.name = name


class TestEntity:
    @pytest.fixture
    def draft_user(self) -> User:
        return User(None, "Alice")

    @pytest.fixture
    def persisted_user(self) -> User:
        return User(1, "Alice")

    def test___init___when_id_is_none_then_creates_draft_entity(self, draft_user: User) -> None:
        # Arrange done by fixture

        # Act done by constructor

        # Assert
        assert draft_user._id is None

    def test___init___when_id_is_defined_then_assigns_id_correctly(
        self, persisted_user: User
    ) -> None:
        # Arrange done by fixture

        # Act done by constructor

        # Assert
        assert persisted_user._id == 1

    def test___setattr___when_setting_id_after_init_then_raises_attribute_error(
        self, persisted_user: User
    ) -> None:
        # Arrange

        # Act / Assert
        with pytest.raises(AttributeError) as exc_info:
            persisted_user.__setattr__("_id", 99)
        # Assert
        assert "Cannot modify" in str(exc_info.value)

    def test___setattr___when_setting_non_id_attribute_then_allows_assignment(
        self, persisted_user: User
    ) -> None:
        # Arrange

        # Act
        persisted_user.__setattr__("name", "Bob")
        # Assert
        assert persisted_user.name == "Bob"

    def test___delattr___when_deleting_id_then_raises_attribute_error(
        self, persisted_user: User
    ) -> None:
        # Arrange

        # Act / Assert
        with pytest.raises(AttributeError) as exc_info:
            persisted_user.__delattr__("_id")
        # Assert
        assert "Cannot delete" in str(exc_info.value)

    def test___delattr___when_deleting_non_id_attribute_then_deletes_successfully(
        self, persisted_user: User
    ) -> None:
        # Arrange
        persisted_user.extra = "data"

        # Act
        persisted_user.__delattr__("extra")

        # Assert
        assert not hasattr(persisted_user, "extra")

    def test_id_when_called_then_returns_current_identifier(self, persisted_user: User) -> None:
        # Arrange

        # Act
        result = persisted_user.id

        # Assert
        assert result == 1

    def test_is_persisted_when_id_is_none_then_returns_false(self, draft_user: User) -> None:
        # Arrange

        # Act
        result = draft_user.is_persisted()

        # Assert
        assert result is False

    def test_is_persisted_when_id_is_defined_then_returns_true(self, persisted_user: User) -> None:
        # Arrange

        # Act
        result = persisted_user.is_persisted()

        # Assert
        assert result is True

    def test___eq___when_same_class_and_same_id_then_returns_true(self) -> None:
        # Arrange
        user1 = User(1, "A")
        user2 = User(1, "B")

        # Act
        result = user1.__eq__(user2)

        # Assert
        assert result is True

    def test___eq___when_same_class_and_different_ids_then_returns_false(self) -> None:
        # Arrange
        user1 = User(1, "A")
        user2 = User(2, "B")

        # Act
        result = user1.__eq__(user2)

        # Assert
        assert result is False

    def test___eq___when_draft_entities_then_only_equal_if_same_instance(
        self, draft_user: User
    ) -> None:
        # Arrange
        other_draft = User(None, "Alice")

        # Act
        result_same = draft_user.__eq__(draft_user)
        result_different = draft_user.__eq__(other_draft)

        # Assert
        assert result_same is True
        assert result_different is False

    def test___eq___when_comparing_with_different_class_then_returns_not_implemented(
        self, persisted_user: User
    ) -> None:
        # Arrange
        other = object()

        # Act
        result = persisted_user.__eq__(other)

        # Assert
        assert result is NotImplemented

    def test___hash___when_persisted_then_returns_hash_of_id(self, persisted_user: User) -> None:
        # Arrange

        # Act
        result = persisted_user.__hash__()

        # Assert
        assert result == hash(1)

    def test___hash___when_draft_then_raises_draft_entity_is_not_hashable_error(
        self, draft_user: User
    ) -> None:
        # Arrange

        # Act / Assert
        with pytest.raises(DraftEntityIsNotHashableError):
            _ = draft_user.__hash__()

    def test___str___when_called_then_returns_class_and_id_string(
        self, persisted_user: User
    ) -> None:
        # Arrange

        # Act
        result = persisted_user.__str__()

        # Assert
        assert result == "User(id=1)"

    def test___repr___when_called_then_returns_same_as_str(self, persisted_user: User) -> None:
        # Arrange

        # Act
        result = persisted_user.__repr__()

        # Assert
        assert result == str(persisted_user)
