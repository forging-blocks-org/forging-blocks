# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest

from forging_blocks.infrastructure.repositories.in_memory_read_repository import (
    InMemoryReadRepository,
)


class FakeReadModel:
    """A simple read model for testing."""

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FakeReadModel):
            return False
        return self.id == other.id and self.name == other.name


@pytest.mark.unit
class TestInMemoryReadRepository:
    async def test_get_by_id_when_id_exists_then_returns_aggregate(self) -> None:
        storage = {"1": FakeReadModel("1", "Alice")}
        repo = InMemoryReadRepository[FakeReadModel, str](storage)

        result = await repo.get_by_id("1")

        assert result is not None
        assert result.id == "1"
        assert result.name == "Alice"

    async def test_get_by_id_when_id_does_not_exist_then_returns_none(self) -> None:
        repo = InMemoryReadRepository[FakeReadModel, str]()

        result = await repo.get_by_id("nonexistent")

        assert result is None

    async def test_list_all_when_storage_has_items_then_returns_all_items(self) -> None:
        storage = {
            "1": FakeReadModel("1", "Alice"),
            "2": FakeReadModel("2", "Bob"),
        }
        repo = InMemoryReadRepository[FakeReadModel, str](storage)

        results = await repo.list_all()

        assert len(results) == 2
        assert FakeReadModel("1", "Alice") in results
        assert FakeReadModel("2", "Bob") in results

    async def test_list_all_when_storage_is_empty_then_returns_empty_sequence(self) -> None:
        repo = InMemoryReadRepository[FakeReadModel, str]()

        results = await repo.list_all()

        assert len(results) == 0
        assert results == []

    async def test_init_when_no_storage_given_then_creates_empty_storage(self) -> None:
        repo = InMemoryReadRepository[FakeReadModel, str]()

        results = await repo.list_all()

        assert results == []

    async def test_init_when_storage_given_then_uses_provided_data(self) -> None:
        storage = {"a": FakeReadModel("a", "X")}
        repo = InMemoryReadRepository[FakeReadModel, str](storage)

        result = await repo.get_by_id("a")

        assert result is not None
        assert result.name == "X"

    async def test_storage_is_independent_copy_when_storage_given(self) -> None:
        storage = {"1": FakeReadModel("1", "Alice")}
        repo = InMemoryReadRepository[FakeReadModel, str](storage)

        storage["1"] = FakeReadModel("1", "Changed")

        result = await repo.get_by_id("1")
        assert result is not None
        assert result.name == "Alice"
