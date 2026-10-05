import pytest

from forging_blocks.domain import DraftEntityIsNotHashableError, Entity


class User(Entity[int]):
    def __init__(self, entity_id: int | None = None, name: str = "") -> None:
        super().__init__(entity_id)
        self.name = name


@pytest.mark.unit
class TestUserEqualityAndHashing:
    @pytest.fixture
    def draft_user(self) -> User:
        return User(None, "Alice")

    @pytest.fixture
    def persisted_user(self) -> User:
        return User(1, "Alice")

    def test___eq___when_same_class_and_same_id_then_returns_true(self) -> None:
        user_a = User(1, "A")
        user_b = User(1, "B")

        result = user_a == user_b

        assert result is True

    def test___eq___when_same_class_and_different_ids_then_returns_false(self) -> None:
        user_a = User(1, "A")
        user_b = User(2, "B")

        result = user_a == user_b

        assert result is False

    def test___eq___when_one_persisted_and_one_draft_then_returns_false(self) -> None:
        persisted = User(1, "A")
        draft = User(None, "A")

        result = persisted == draft

        assert result is False

    def test___eq___when_both_drafts_then_only_equal_if_same_instance(
        self,
        draft_user: User,
    ) -> None:
        other_draft = User(None, "Alice")
        result_same = draft_user == draft_user
        result_different = draft_user == other_draft

        assert result_same is True
        assert result_different is False

    def test___eq___when_comparing_with_different_class_then_returns_false(
        self,
        persisted_user: User,
    ) -> None:
        other_object = object()

        result = persisted_user.__eq__(other_object)

        assert result is False

    def test___eq___when_comparing_with_subclass_then_returns_false(self) -> None:
        class Admin(User):
            pass

        user = User(1, "A")
        admin = Admin(1, "A")

        result = user.__eq__(admin)

        assert result is False

    def test_eq_using_equals_syntatic_sugar_when_comparing_with_subclass_then_returns_false(
        self,
    ) -> None:
        class Admin(User):
            pass

        user = User(1, "A")
        admin = Admin(1, "A")

        result = user == admin

        assert result is False

    def test___hash___when_persisted_then_returns_hash_of_class_and_id(
        self,
        persisted_user: User,
    ) -> None:
        actual_hash = hash(persisted_user)
        expected_hash = hash((User, 1))

        assert actual_hash == expected_hash

    def test___hash___when_draft_then_raises_draft_entity_is_not_hashable_error(
        self,
        draft_user: User,
    ) -> None:
        with pytest.raises(DraftEntityIsNotHashableError):
            hash(draft_user)

    def test___hash___when_two_entities_have_same_id_then_hashes_are_equal(
        self,
    ) -> None:
        user_a = User(1, "A")
        user_b = User(1, "B")
        hash_a = hash(user_a)
        hash_b = hash(user_b)

        assert hash_a == hash_b
