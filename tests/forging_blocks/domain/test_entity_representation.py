import copy

import pytest

from tests.forging_blocks.domain.fixtures.user import User


@pytest.mark.unit
class TestUserRepresentationAndCopy:
    @pytest.fixture
    def draft_user(self) -> User:
        return User(None, "Alice")

    @pytest.fixture
    def persisted_user(self) -> User:
        return User(1, "Alice")

    def test_copy_when_entity_is_persisted_then_copy_preserves_state(
        self,
        persisted_user: User,
    ) -> None:
        clone = copy.copy(persisted_user)

        assert clone.id == persisted_user.id
        assert clone.name == persisted_user.name

    def test___str___when_called_then_returns_class_and_id_string(
        self,
        persisted_user: User,
    ) -> None:
        result = str(persisted_user)

        assert result == "User(id=1)"

    def test___repr___when_called_then_returns_same_as_str(
        self,
        persisted_user: User,
    ) -> None:
        result = repr(persisted_user)

        assert result == str(persisted_user)

    def test___str___when_draft_then_returns_class_with_none_id(
        self,
        draft_user: User,
    ) -> None:
        result = str(draft_user)

        assert result == "User(id=None)"

    def test___repr___when_draft_then_returns_same_as_str(
        self,
        draft_user: User,
    ) -> None:
        result = repr(draft_user)

        assert result == str(draft_user)

    def test_copy_when_entity_is_draft_then_copy_preserves_draft_state(
        self,
        draft_user: User,
    ) -> None:
        clone = copy.copy(draft_user)

        assert clone.id is None
        assert clone.name == draft_user.name
        assert clone.is_persisted() is False
