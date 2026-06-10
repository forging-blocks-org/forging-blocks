# pyright: reportPrivateUsage=false

from typing import Callable

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
    @pytest.fixture
    def create_alice_aggregate(self) -> Callable[[str], FakeAggregate]:
        return lambda id: FakeAggregate(id, "Alice")

    async def test_save_when_aggregate_has_id_then_persists_aggregate(
        self, create_alice_aggregate: Callable[[str], FakeAggregate]
    ) -> None:
        repo = InMemoryWriteRepository[FakeAggregate, str]()
        alice_id = "1"
        aggregate = create_alice_aggregate(alice_id)

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

    async def test_delete_by_id_when_id_exists_then_removes_aggregate(
        self, create_alice_aggregate: Callable[[str], FakeAggregate]
    ) -> None:
        repo = InMemoryWriteRepository[FakeAggregate, str]()
        alice_id = "1"
        repo._storage[alice_id] = create_alice_aggregate(alice_id)

        await repo.delete_by_id(alice_id)

        assert alice_id not in repo._storage

    async def test_delete_by_id_when_id_does_not_exist_then_raises_not_found_error(self) -> None:
        repo = InMemoryWriteRepository[FakeAggregate, str]()

        with pytest.raises(RepositoryNotFoundError) as exc_info:
            await repo.delete_by_id("nonexistent")

        assert "nonexistent" in str(exc_info.value)
        assert "not found" in str(exc_info.value).lower()

    async def test_delete_by_id_when_id_exists_then_removes_only_target_aggregate(
        self, create_alice_aggregate: Callable[[str], FakeAggregate]
    ) -> None:
        repo = InMemoryWriteRepository[FakeAggregate, str]()
        alice_id = "1"
        john_id = "2"
        john_aggregate = FakeAggregate(john_id, "John")
        alice = create_alice_aggregate(alice_id)
        repo._storage[alice_id] = alice
        repo._storage[john_id] = john_aggregate

        await repo.delete_by_id(john_id)

        assert john_id not in repo._storage
        assert repo._storage[alice_id] == alice

    async def test_init_when_no_storage_given_then_creates_empty_storage(self) -> None:
        repo = InMemoryWriteRepository[FakeAggregate, str]()

        assert len(repo._storage) == 0

    async def test_init_when_storage_given_then_uses_provided_data(self) -> None:
        fake_id = "a"
        fake_name = "X"
        storage = {fake_id: FakeAggregate(fake_id, fake_name)}
        repo = InMemoryWriteRepository[FakeAggregate, str](storage)

        assert repo._storage[fake_id].name == fake_name

    async def test_storage_is_independent_copy_when_storage_given(
        self, create_alice_aggregate: Callable[[str], FakeAggregate]
    ) -> None:
        alice_id = "1"
        storage: dict[str, FakeAggregate] = {alice_id: create_alice_aggregate(alice_id)}
        repo = InMemoryWriteRepository[FakeAggregate, str](storage)

        storage[alice_id] = FakeAggregate(alice_id, "Changed")

        expected_name = "Alice"
        assert repo._storage[alice_id].name == expected_name

    async def test_save_when_aggregate_id_is_empty_string_then_raises_repository_error(
        self,
    ) -> None:
        """Empty-string IDs must be rejected — matching AggregateRoot validation."""
        repo = InMemoryWriteRepository[FakeAggregate, str]()
        aggregate = FakeAggregate("", "EmptyId")

        with pytest.raises(RepositoryError):
            await repo.save(aggregate)

    async def test_save_when_aggregate_id_is_false_then_raises_repository_error(
        self,
    ) -> None:
        """Boolean-False IDs must be rejected — matching AggregateRoot validation."""
        repo: InMemoryWriteRepository[FakeAggregate, str] = InMemoryWriteRepository()
        aggregate = FakeAggregate(False, "FalseId")  # type: ignore[arg-type]

        with pytest.raises(RepositoryError):
            await repo.save(aggregate)

    async def test_delete_by_id_when_id_is_none_then_raises_repository_error(
        self,
    ) -> None:
        """delete_by_id must reject None before probing storage.

        A None ID should never reach the storage lookup.  We populate
        storage with a None key so that a *missing* validation would
        succeed silently — proving the bug when the test fails.
        """
        repo: InMemoryWriteRepository[FakeAggregate, str] = InMemoryWriteRepository()
        repo._storage[None] = FakeAggregate("dummy", "dummy")  # type: ignore[index]

        with pytest.raises(RepositoryError):
            await repo.delete_by_id(None)  # type: ignore[arg-type]

    async def test_delete_by_id_when_id_is_empty_string_then_raises_repository_error(
        self,
    ) -> None:
        """delete_by_id must reject empty-string IDs before probing storage."""
        repo = InMemoryWriteRepository[FakeAggregate, str]()
        repo._storage[""] = FakeAggregate("dummy", "dummy")

        with pytest.raises(RepositoryError):
            await repo.delete_by_id("")

    async def test_delete_by_id_when_id_is_false_then_raises_repository_error(
        self,
    ) -> None:
        """delete_by_id must reject boolean-False IDs before probing storage.

        False is especially dangerous because ``False == 0`` and
        ``hash(False) == hash(0)``, causing dict-key collisions with
        legitimate integer IDs.
        """
        repo: InMemoryWriteRepository[FakeAggregate, str] = InMemoryWriteRepository()
        repo._storage[False] = FakeAggregate("dummy", "dummy")  # type: ignore[index]

        with pytest.raises(RepositoryError):
            await repo.delete_by_id(False)  # type: ignore[arg-type]
