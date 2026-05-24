# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest

from forging_blocks.infrastructure.errors.repository_errors import (
    RepositoryError,
    RepositoryNotFoundError,
)
from forging_blocks.infrastructure.repositories.in_memory_write_repository import (
    InMemoryWriteRepository,
)


class FakeAggregate:
    """A simple aggregate for testing write operations."""

    def __init__(self, id: str | None, name: str) -> None:
        self.id = id
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FakeAggregate):
            return False
        return self.id == other.id and self.name == other.name


@pytest.mark.unit
class TestInMemoryWriteRepository:
    async def test_save_when_aggregate_has_id_then_persists_aggregate(self) -> None:
        repo = InMemoryWriteRepository[FakeAggregate, str]()
        aggregate = FakeAggregate("1", "Alice")

        await repo.save(aggregate)

        assert repo._storage["1"] == aggregate

    async def test_save_when_aggregate_has_no_id_then_raises_repository_error(self) -> None:
        repo = InMemoryWriteRepository[FakeAggregate, str]()
        aggregate = FakeAggregate(None, "Draft")

        with pytest.raises(RepositoryError):
            await repo.save(aggregate)

    async def test_save_when_aggregate_overwrites_existing_then_updates_storage(self) -> None:
        repo = InMemoryWriteRepository[FakeAggregate, str]()
        old = FakeAggregate("1", "OldName")
        new = FakeAggregate("1", "NewName")

        await repo.save(old)
        await repo.save(new)

        assert repo._storage["1"].name == "NewName"

    async def test_delete_by_id_when_id_exists_then_removes_aggregate(self) -> None:
        repo = InMemoryWriteRepository[FakeAggregate, str]()
        repo._storage["1"] = FakeAggregate("1", "Alice")

        await repo.delete_by_id("1")

        assert "1" not in repo._storage

    async def test_delete_by_id_when_id_does_not_exist_then_raises_not_found_error(self) -> None:
        repo = InMemoryWriteRepository[FakeAggregate, str]()

        with pytest.raises(RepositoryNotFoundError) as exc_info:
            await repo.delete_by_id("nonexistent")

        assert "nonexistent" in str(exc_info.value)
        assert "not found" in str(exc_info.value).lower()

    async def test_delete_by_id_when_id_exists_then_does_not_raise(self) -> None:
        repo = InMemoryWriteRepository[FakeAggregate, str]()
        repo._storage["1"] = FakeAggregate("1", "Alice")

        await repo.delete_by_id("1")

        assert "1" not in repo._storage

    async def test_init_when_no_storage_given_then_creates_empty_storage(self) -> None:
        repo = InMemoryWriteRepository[FakeAggregate, str]()

        assert len(repo._storage) == 0

    async def test_init_when_storage_given_then_uses_provided_data(self) -> None:
        storage = {"a": FakeAggregate("a", "X")}
        repo = InMemoryWriteRepository[FakeAggregate, str](storage)

        assert repo._storage["a"].name == "X"

    async def test_storage_is_independent_copy_when_storage_given(self) -> None:
        storage: dict[str, FakeAggregate] = {"1": FakeAggregate("1", "Alice")}
        repo = InMemoryWriteRepository[FakeAggregate, str](storage)

        storage["1"] = FakeAggregate("1", "Changed")

        assert repo._storage["1"].name == "Alice"
