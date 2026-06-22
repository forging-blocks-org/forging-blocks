"""
Tests for the base repository classes.
"""

import pytest

from forging_blocks.foundation.identified import Identified
from forging_blocks.foundation.specification import ExpressionSpecification, Specification
from forging_blocks.infrastructure.errors.repository_errors import (
    RepositoryError,
    RepositoryNotFoundError,
)
from forging_blocks.infrastructure.repositories.base_repository import (
    BaseReadRepository,
    BaseRepository,
    BaseWriteRepository,
)


class FakeEntity(Identified[str]):
    """Fake entity for testing."""

    def __init__(self, id: str | None = None, name: str = "") -> None:
        self._id = id
        self._name = name

    @property
    def id(self) -> str | None:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class FakeSpecification(Specification[FakeEntity]):
    """Fake specification for testing."""

    def __init__(self, name_filter: str):
        self._name_filter = name_filter

    def is_satisfied_by(self, candidate: FakeEntity) -> bool:
        return self._name_filter in candidate.name


class TestBaseReadRepository:
    """Tests for BaseReadRepository."""

    @pytest.fixture
    def storage(self) -> dict[str, FakeEntity]:
        """Create test storage."""
        return {
            "1": FakeEntity("1", "Alice"),
            "2": FakeEntity("2", "Bob"),
            "3": FakeEntity("3", "Charlie"),
        }

    @pytest.fixture
    def repo(self, storage: dict[str, FakeEntity]) -> BaseReadRepository[FakeEntity, str]:
        """Create a BaseReadRepository with test storage."""
        return BaseReadRepository[FakeEntity, str](storage)

    @pytest.mark.asyncio
    async def test_get_by_id_existing(self, repo: BaseReadRepository[FakeEntity, str]) -> None:
        """Test getting an existing entity by ID."""
        entity = await repo.get_by_id("1")
        assert entity is not None
        assert entity.id == "1"
        assert entity.name == "Alice"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo: BaseReadRepository[FakeEntity, str]) -> None:
        """Test getting a non-existent entity by ID."""
        entity = await repo.get_by_id("999")
        assert entity is None

    @pytest.mark.asyncio
    async def test_list_all(self, repo: BaseReadRepository[FakeEntity, str]) -> None:
        """Test listing all entities."""
        entities = await repo.list_all()
        assert len(entities) == 3
        names = {e.name for e in entities}
        assert names == {"Alice", "Bob", "Charlie"}

    @pytest.mark.asyncio
    async def test_find_matching(self, repo: BaseReadRepository[FakeEntity, str]) -> None:
        """Test finding entities matching a specification."""
        spec = FakeSpecification("Ali")
        entities = await repo.find_matching(spec)
        assert len(entities) == 1
        assert entities[0].name == "Alice"

    @pytest.mark.asyncio
    async def test_count_matching(self, repo: BaseReadRepository[FakeEntity, str]) -> None:
        """Test counting entities matching a specification."""
        spec = FakeSpecification("li")  # Alice, Charlie
        count = await repo.count_matching(spec)
        assert count == 2

    @pytest.mark.asyncio
    async def test_exists_matching(self, repo: BaseReadRepository[FakeEntity, str]) -> None:
        """Test checking if any entity matches a specification."""
        spec = FakeSpecification("Bob")
        exists = await repo.exists_matching(spec)
        assert exists is True

        spec = FakeSpecification("David")
        exists = await repo.exists_matching(spec)
        assert exists is False

    @pytest.mark.asyncio
    async def test_empty_storage(self) -> None:
        """Test repository with empty storage."""
        repo: BaseReadRepository[FakeEntity, str] = BaseReadRepository[FakeEntity, str]({})
        entities = await repo.list_all()
        assert entities == []


class TestBaseWriteRepository:
    """Tests for BaseWriteRepository."""

    @pytest.fixture
    def repo(self) -> BaseWriteRepository[FakeEntity, str]:
        """Create a BaseWriteRepository."""
        return BaseWriteRepository[FakeEntity, str]()

    @pytest.mark.asyncio
    async def test_save_entity(self, repo: BaseWriteRepository[FakeEntity, str]) -> None:
        """Test saving an entity."""
        entity = FakeEntity("1", "Alice")
        await repo.save(entity)

        await repo.delete_by_id("1")

    @pytest.mark.asyncio
    async def test_save_overwrites_existing(
        self, repo: BaseWriteRepository[FakeEntity, str]
    ) -> None:
        """Test that saving an entity with existing ID overwrites it."""
        entity1 = FakeEntity("1", "Alice")
        entity2 = FakeEntity("1", "Bob")
        await repo.save(entity1)
        await repo.save(entity2)

        await repo.delete_by_id("1")

    @pytest.mark.asyncio
    async def test_delete_by_id(self, repo: BaseWriteRepository[FakeEntity, str]) -> None:
        """Test deleting an entity by ID."""
        entity = FakeEntity("1", "Alice")
        await repo.save(entity)

        await repo.delete_by_id("1")

        with pytest.raises(RepositoryNotFoundError):
            await repo.delete_by_id("1")

    @pytest.mark.asyncio
    async def test_delete_nonexistent_raises(
        self, repo: BaseWriteRepository[FakeEntity, str]
    ) -> None:
        """Test deleting a non-existent entity raises RepositoryNotFoundError."""
        with pytest.raises(RepositoryNotFoundError):
            await repo.delete_by_id("999")

    @pytest.mark.asyncio
    async def test_save_none_id_raises(self, repo: BaseWriteRepository[FakeEntity, str]) -> None:
        """Test saving an entity with None ID raises RepositoryError."""
        entity = FakeEntity(name="Alice")
        with pytest.raises(RepositoryError):
            await repo.save(entity)

    @pytest.mark.asyncio
    async def test_save_empty_string_id_raises(
        self, repo: BaseWriteRepository[FakeEntity, str]
    ) -> None:
        """Test saving an entity with empty string ID raises RepositoryError."""
        entity = FakeEntity("", "Alice")
        with pytest.raises(RepositoryError):
            await repo.save(entity)

    @pytest.mark.asyncio
    async def test_save_false_id_raises(self, repo: BaseWriteRepository[FakeEntity, str]) -> None:
        """Test saving an entity with False ID raises RepositoryError."""
        entity = FakeEntity("1", "Alice")
        object.__setattr__(entity, "_id", False)
        with pytest.raises(RepositoryError):
            await repo.save(entity)

    @pytest.mark.asyncio
    async def test_delete_none_id_raises(self, repo: BaseWriteRepository[FakeEntity, str]) -> None:
        """Test deleting with None ID raises RepositoryError."""
        with pytest.raises(RepositoryError):
            from typing import cast

            await repo.delete_by_id(cast(str, None))

    @pytest.mark.asyncio
    async def test_delete_empty_string_id_raises(
        self, repo: BaseWriteRepository[FakeEntity, str]
    ) -> None:
        """Test deleting with empty string ID raises RepositoryError."""
        with pytest.raises(RepositoryError):
            await repo.delete_by_id("")

    @pytest.mark.asyncio
    async def test_delete_false_id_raises(self, repo: BaseWriteRepository[FakeEntity, str]) -> None:
        """Test deleting with False ID raises RepositoryError."""
        with pytest.raises(RepositoryError):
            from typing import cast

            await repo.delete_by_id(cast(str, False))


class TestBaseRepository:
    """Tests for BaseRepository (full CRUD)."""

    @pytest.fixture
    def repo(self) -> BaseRepository[FakeEntity, str]:
        """Create a BaseRepository."""
        return BaseRepository[FakeEntity, str]()

    @pytest.mark.asyncio
    async def test_full_crud(self, repo: BaseRepository[FakeEntity, str]) -> None:
        """Test full CRUD operations."""
        # Create
        entity = FakeEntity("1", "Alice")
        await repo.save(entity)

        # Read
        retrieved = await repo.get_by_id("1")
        assert retrieved is not None
        assert retrieved.name == "Alice"

        # Update
        updated = FakeEntity("1", "Bob")
        await repo.save(updated)
        retrieved = await repo.get_by_id("1")
        assert retrieved is not None
        assert retrieved.name == "Bob"

        # Delete
        await repo.delete_by_id("1")
        retrieved = await repo.get_by_id("1")
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_list_all_after_operations(self, repo: BaseRepository[FakeEntity, str]) -> None:
        """Test list_all reflects all operations."""
        await repo.save(FakeEntity("1", "Alice"))
        await repo.save(FakeEntity("2", "Bob"))

        entities = await repo.list_all()
        assert len(entities) == 2

        await repo.delete_by_id("1")
        entities = await repo.list_all()
        assert len(entities) == 1
        assert entities[0].name == "Bob"

    @pytest.mark.asyncio
    async def test_specification_queries(self, repo: BaseRepository[FakeEntity, str]) -> None:
        """Test specification-based queries work with full repository."""
        await repo.save(FakeEntity("1", "Alice"))
        await repo.save(FakeEntity("2", "Bob"))
        await repo.save(FakeEntity("3", "Charlie"))

        spec = ExpressionSpecification[FakeEntity](lambda e: e.name.startswith("A"))
        entities = await repo.find_matching(spec)
        assert len(entities) == 1
        assert entities[0].name == "Alice"

        count = await repo.count_matching(spec)
        assert count == 1

        exists = await repo.exists_matching(spec)
        assert exists is True
