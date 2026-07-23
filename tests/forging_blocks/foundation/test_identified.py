"""Tests for the Identified protocol."""

import pytest

from forging_blocks.domain.aggregate_root import AggregateRoot
from forging_blocks.domain.entity import Entity
from forging_blocks.foundation.identified import Identified


class WithId:
    """Class that structurally satisfies Identified."""

    def __init__(self, entity_id: str) -> None:
        self._id = entity_id

    @property
    def id(self) -> str | None:
        return self._id


class WithoutId:
    """Class that does not have an id property."""

    def __init__(self, name: str) -> None:
        self.name = name


class WithIdAsPlainAttribute:
    """Class with id as a plain attribute, not a property."""

    def __init__(self, entity_id: str) -> None:
        object.__setattr__(self, "id", entity_id)


@pytest.mark.unit
class TestIdentifiedProtocol:
    def test_with_id_class_satisfies_identified(self) -> None:
        """A class with an id property should be usable where Identified is expected."""
        obj: Identified[str] = WithId("abc")
        assert obj.id == "abc"

    def test_entity_satisfies_identified(self) -> None:
        """Entity class should structurally satisfy Identified protocol."""

        class MyEntity(Entity[int]):
            pass

        entity: Identified[int] = MyEntity(42)
        assert entity.id == 42

    def test_aggregate_root_satisfies_identified(self) -> None:
        """AggregateRoot should structurally satisfy Identified protocol."""

        class MyAggregate(AggregateRoot[str, object]):
            def _handle(self, event: object) -> None:
                pass

        aggregate: Identified[str] = MyAggregate("agg-1")
        assert aggregate.id == "agg-1"

    def test_identified_allows_none_id(self) -> None:
        """Identified should allow None id for draft/unpersisted objects."""

        class DraftEntity(Entity[str]):
            pass

        entity: Identified[str] = DraftEntity(None)
        assert entity.id is None

    def test_with_id_plain_attribute_satisfies_identified(self) -> None:
        """A plain attribute 'id' should structurally satisfy Identified."""
        obj: Identified[str] = WithIdAsPlainAttribute("xyz")
        assert obj.id == "xyz"

    def test_identified_is_protocol(self) -> None:
        """Identified should be usable for type annotations without inheritance."""

        def get_id(obj: Identified[str]) -> str | None:
            return obj.id

        result = get_id(WithId("test"))
        assert result == "test"
