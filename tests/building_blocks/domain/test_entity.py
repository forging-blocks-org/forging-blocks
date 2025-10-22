import pytest

from building_blocks.domain.entity import DraftEntity, Entity, _BaseEntity
from building_blocks.domain.errors.entity_id_errors import (
    DraftEntityIsNotHashableError,
    EntityIdCannotBeNoneError,
)


class FakeEntity(_BaseEntity[str]):
    def __init__(self, id: str | None):
        super().__init__(id)


class DefinedIdEntity(Entity[str]):
    def __init__(self, id: str):
        super().__init__(id)


class IdToDefineEntity(DraftEntity[int]):
    def __init__(self, id: int | None = None):
        super().__init__(id)


class TestBaseEntity:
    def test_init_when_id_then_set_id(self):
        id_ = "123"

        entity = FakeEntity(id_)

        assert entity.id == id_, "Entity ID should be set correctly"

    def test_id_property_when_id_exists_then_return_id(self):
        id_ = "123"
        entity = FakeEntity(id_)

        result = entity.id

        expected_result = id_
        assert result == expected_result, "ID property should return the correct ID"

    def test__eq_when_another_entity_with_the_same_id_then_true(self):
        entity1 = FakeEntity("123")
        entity2 = FakeEntity("123")

        result = entity1 == entity2

        expected_result = True
        assert result is expected_result, "Entities with the same ID should be equal"

    def test__eq_when_another_entity_with_different_id_then_false(self):
        entity1 = FakeEntity("123")
        entity2 = FakeEntity("456")

        result = entity1 == entity2

        expected_result = False
        result_assertion = result is expected_result
        assert result_assertion, "Entities with different IDs should not be equal"

    def test__eq_when_another_object_then_false(self):
        entity = FakeEntity("123")
        other_object = object()

        result = entity == other_object

        expected_result = False
        result_assertion = result is expected_result
        assert result_assertion, "Entity should not be equal to a non-entity object"

    def test_hash_when_id_then_hash_id(self):
        id_ = "123"
        entity = FakeEntity(id_)

        hash1 = hash(entity)

        expected_hash = hash(id_)
        assert (
            hash1 == expected_hash
        ), "Hash values should be equal for entities with the same ID"

    def test_hash_when_id_is_not_set_then_raises_type_error(self):
        entity = FakeEntity(None)

        with pytest.raises(TypeError, match="Unhashable FakeEntity: id is None"):
            hash(entity)

    def test_str_representation(self):
        entity = FakeEntity("123")

        result = str(entity)

        expected_result = "FakeEntity(id=123)"
        assert (
            result == expected_result
        ), f"String representation should be '{expected_result}'"

    def test_repr_representation(self):
        entity = FakeEntity("123")

        result = repr(entity)

        expected_result = "FakeEntity(id=123)"
        assert (
            result == expected_result
        ), f"Repr representation should be '{expected_result}'"


class TestEntity:
    def test_init_when_id_then_set_id(self):
        id_ = "123"

        entity = DefinedIdEntity(id_)

        assert entity.id == id_, "Entity ID should be set correctly"

    def test_init_when_id_is_none_then_raises_type_error(self):
        with pytest.raises(EntityIdCannotBeNoneError):
            DefinedIdEntity(None)  # type: ignore


class TestDraftEntity:
    def test_init_when_id_is_none_then_set_id_to_none(self):
        entity = IdToDefineEntity()

        assert entity.id is None, "ID should be None for DraftEntity without ID"

    def test_init_when_id_is_provided_then_set_id(self):
        id_ = 123
        entity = IdToDefineEntity(id_)

        assert entity.id == id_, "ID should be set correctly for DraftEntity with ID"

    def test_eq_when_another_entity_with_the_same_id_then_true(self) -> None:
        entity1 = IdToDefineEntity(123)
        entity2 = IdToDefineEntity(123)

        result = entity1 == entity2

        expected_result = True
        assert (
            result is expected_result
        ), "DraftEntities with the same ID should be equal"

    def test_eq_when_another_entity_with_different_id_then_false(self) -> None:
        entity1 = IdToDefineEntity(123)
        entity2 = IdToDefineEntity(456)

        result = entity1 == entity2

        expected_result = False
        result_assertion = result is expected_result
        assert result_assertion, "DraftEntities with different IDs should not be equal"

    def test_eq_when_another_object_then_false(self) -> None:
        entity = IdToDefineEntity(123)
        other_object = object()

        result = entity == other_object

        expected_result = False
        result_assertion = result is expected_result
        assert (
            result_assertion
        ), "DraftEntity should not be equal to a non-entity object"

    def test_hash_when_draft_entity_then_raises_draft_entity_is_not_hashable(
        self,
    ) -> None:
        entity = IdToDefineEntity()

        with pytest.raises(DraftEntityIsNotHashableError):
            hash(entity)
