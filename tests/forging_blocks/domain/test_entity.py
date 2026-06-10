# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import copy

import pytest

from forging_blocks.domain import (
    DraftEntityIsNotHashableError,
    Entity,
)


class User(Entity[int]):
    def __init__(self, entity_id: int | None = None, name: str = "") -> None:
        super().__init__(entity_id)
        self.name = name


class Admin(User):
    pass


@pytest.mark.unit
class TestUser:
    @pytest.fixture
    def draft_user(self) -> User:
        return User(None, "Alice")

    @pytest.fixture
    def persisted_user(self) -> User:
        return User(1, "Alice")

    def test___init___when_id_is_none_then_creates_draft_entity(self, draft_user: User) -> None:
        result = draft_user.id
        assert result is None

    def test___init___when_id_is_defined_then_assigns_id_correctly(
        self, persisted_user: User
    ) -> None:
        result = persisted_user.id
        assert result == 1

    def test___setattr___when_trying_to_modify_id_then_raises_attribute_error(
        self, persisted_user: User
    ) -> None:
        new_id = 99
        with pytest.raises(AttributeError) as exc_info:
            persisted_user.__setattr__("_id", new_id)
        assert "cannot modify" in str(exc_info.value)

    def test___setattr___when_setting_same_id_value_then_allows_copy_safe_reassign(
        self, persisted_user: User
    ) -> None:
        same_id = persisted_user.id
        persisted_user.__setattr__("_id", same_id)
        assert persisted_user.id == same_id

    def test___setattr___when_setting_non_id_attribute_then_allows_assignment(
        self, persisted_user: User
    ) -> None:
        new_name = "Bob"
        persisted_user.__setattr__("name", new_name)
        assert persisted_user.name == new_name

    def test___delattr___when_deleting_id_then_raises_attribute_error(
        self, persisted_user: User
    ) -> None:
        with pytest.raises(AttributeError) as exc_info:
            persisted_user.__delattr__("_id")
        assert "cannot delete" in str(exc_info.value)

    def test___delattr___when_deleting_non_id_attribute_then_deletes_successfully(
        self, persisted_user: User
    ) -> None:
        persisted_user.extra = "data"
        persisted_user.__delattr__("extra")
        assert not hasattr(persisted_user, "extra")

    def test_is_persisted_when_id_is_none_then_returns_false(self, draft_user: User) -> None:
        result = draft_user.is_persisted()
        assert result is False

    def test_is_persisted_when_id_defined_then_returns_true(self, persisted_user: User) -> None:
        result = persisted_user.is_persisted()
        assert result is True

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
        self, draft_user: User
    ) -> None:
        other_draft = User(None, "Alice")
        result_same = draft_user == draft_user
        result_different = draft_user == other_draft
        assert result_same is True
        assert result_different is False

    def test___eq___when_comparing_with_different_class_then_returns_false(
        self, persisted_user: User
    ) -> None:
        other_object = object()
        result = persisted_user.__eq__(other_object)
        assert result is False

    def test___eq___when_comparing_with_subclass_then_returns_false(self) -> None:
        user = User(1, "A")
        admin = Admin(1, "A")

        result = user.__eq__(admin)

        assert result is False

    def test_eq_using_equals_syntatic_sugar_when_comparing_with_subclass_then_returns_false(
        self,
    ) -> None:
        user = User(1, "A")
        admin = Admin(1, "A")

        result = user == admin

        assert result is False

    def test___hash___when_persisted_then_returns_hash_of_class_and_id(
        self, persisted_user: User
    ) -> None:
        actual_hash = hash(persisted_user)

        expected_hash = hash((User, 1))
        assert actual_hash == expected_hash

    def test___hash___when_draft_then_raises_draft_entity_is_not_hashable_error(
        self, draft_user: User
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

    def test_copy_when_entity_is_persisted_then_copy_preserves_state(
        self, persisted_user: User
    ) -> None:
        clone = copy.copy(persisted_user)
        assert clone.id == persisted_user.id
        assert clone.name == persisted_user.name

    def test___str___when_called_then_returns_class_and_id_string(
        self, persisted_user: User
    ) -> None:
        result = str(persisted_user)
        assert result == "User(id=1)"

    def test___repr___when_called_then_returns_same_as_str(self, persisted_user: User) -> None:
        result = repr(persisted_user)
        assert result == str(persisted_user)

    def test___str___when_draft_then_returns_class_with_none_id(self, draft_user: User) -> None:
        result = str(draft_user)
        assert result == "User(id=None)"

    def test___repr___when_draft_then_returns_same_as_str(self, draft_user: User) -> None:
        result = repr(draft_user)
        assert result == str(draft_user)

    def test_copy_when_entity_is_draft_then_copy_preserves_draft_state(
        self, draft_user: User
    ) -> None:
        clone = copy.copy(draft_user)
        assert clone.id is None
        assert clone.name == draft_user.name
        assert clone.is_persisted() is False

    def test___delattr___when_draft_entity_then_raises_attribute_error(
        self, draft_user: User
    ) -> None:
        with pytest.raises(AttributeError) as exc_info:
            draft_user.__delattr__("_id")
        assert "cannot delete" in str(exc_info.value)

    def test___setattr___when_draft_entity_then_allows_id_assignment(
        self, draft_user: User
    ) -> None:
        draft_user._id = 42
        assert draft_user.id == 42
        assert draft_user.is_persisted() is True

    def test___setattr___when_draft_entity_then_blocks_same_id_reassignment(
        self, draft_user: User
    ) -> None:
        draft_user._id = 42
        draft_user._id = 42
        assert draft_user.id == 42

    def test___setattr___when_draft_entity_then_blocks_different_id_after_persist(
        self, draft_user: User
    ) -> None:
        draft_user._id = 42
        with pytest.raises(AttributeError):
            draft_user._id = 99
