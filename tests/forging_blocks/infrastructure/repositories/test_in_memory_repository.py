"""
Tests for the in-memory repository classes.
"""

import pytest

from forging_blocks.foundation.identified import Identified
from forging_blocks.foundation.specification import Specification
from forging_blocks.infrastructure.errors.repository_errors import (
    RepositoryError,
    RepositoryNotFoundError,
)
from forging_blocks.infrastructure.repositories.in_memory_read_repository import (
    InMemoryReadRepository,
)
from forging_blocks.infrastructure.repositories.in_memory_repository import (
    InMemoryRepository,
)
from forging_blocks.infrastructure.repositories.in_memory_write_repository import (
    InMemoryWriteRepository,
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

    def __init__(self, name_filter: str) -> None:
        self._name_filter = name_filter

    def is_satisfied_by(self, candidate: FakeEntity) -> bool:
        return self._name_filter in candidate.name


class TestInMemoryReadRepository:
    """Tests for InMemoryReadRepository."""

    @pytest.fixture
    def storage(self) -> dict[str, FakeEntity]:
        """Create a storage fixture with test entities."""
        return {
            "1": FakeEntity(id="1", name="Alice"),
            "2": FakeEntity(id="2", name="Bob"),
            "3": FakeEntity(id="3", name="Charlie"),
        }

    @pytest.fixture
    def repo(self, storage: dict[str, FakeEntity]) -> InMemoryReadRepository[FakeEntity, str]:
        """Create an InMemoryReadRepository with test storage."""
        return InMemoryReadRepository[FakeEntity, str](storage)

    async def test_get_by_id_existing(self, repo: InMemoryReadRepository[FakeEntity, str]) -> None:
        """Test getting an existing entity by ID."""
        entity = await repo.get_by_id("1")
        assert entity is not None
        assert entity.name == "Alice"

    async def test_get_by_id_not_found(self, repo: InMemoryReadRepository[FakeEntity, str]) -> None:
        """Test getting a non-existent entity by ID."""
        entity = await repo.get_by_id("999")
        assert entity is None

    async def test_list_all(self, repo: InMemoryReadRepository[FakeEntity, str]) -> None:
        """Test listing all entities."""
        entities = await repo.list_all()
        assert len(entities) == 3
        names = {e.name for e in entities}
        assert names == {"Alice", "Bob", "Charlie"}

    async def test_find_matching(self, repo: InMemoryReadRepository[FakeEntity, str]) -> None:
        """Test finding entities matching a specification."""
        spec = FakeSpecification("Ali")
        entities = await repo.find_matching(spec)
        assert len(entities) == 1
        assert entities[0].name == "Alice"

    async def test_count_matching(self, repo: InMemoryReadRepository[FakeEntity, str]) -> None:
        """Test counting entities matching a specification."""
        spec = FakeSpecification("li")  # Alice, Charlie
        count = await repo.count_matching(spec)
        assert count == 2

    async def test_exists_matching(self, repo: InMemoryReadRepository[FakeEntity, str]) -> None:
        """Test checking if any entity matches a specification."""
        spec = FakeSpecification("Bob")
        exists = await repo.exists_matching(spec)
        assert exists is True

    async def test_empty_storage(self) -> None:
        """Test repository with empty storage."""
        repo: InMemoryReadRepository[FakeEntity, str] = InMemoryReadRepository[FakeEntity, str]({})
        entities = await repo.list_all()
        assert entities == []


class TestInMemoryWriteRepository:
    """Tests for InMemoryWriteRepository."""

    @pytest.fixture
    def repo(self) -> InMemoryWriteRepository[FakeEntity, str]:
        """Create an InMemoryWriteRepository."""
        return InMemoryWriteRepository[FakeEntity, str]()

    async def test_save_new_entity(self, repo: InMemoryWriteRepository[FakeEntity, str]) -> None:
        """Test saving a new entity."""
        entity = FakeEntity(id="1", name="Alice")
        await repo.save(entity)
        # Verify via the storage
        storage = getattr(repo, "_storage")
        assert storage["1"] is entity

    async def test_save_updates_existing(
        self, repo: InMemoryWriteRepository[FakeEntity, str]
    ) -> None:
        """Test saving an entity with an existing ID."""
        entity1 = FakeEntity(id="1", name="Alice")
        await repo.save(entity1)

        entity2 = FakeEntity(id="1", name="AliceUpdated")
        await repo.save(entity2)

        storage = getattr(repo, "_storage")
        assert storage["1"] is entity2

    async def test_delete_by_id(self, repo: InMemoryWriteRepository[FakeEntity, str]) -> None:
        """Test deleting an entity by ID."""
        entity = FakeEntity(id="1", name="Alice")
        await repo.save(entity)
        await repo.delete_by_id("1")

        storage = getattr(repo, "_storage")
        assert "1" not in storage

    async def test_delete_by_id_not_found(
        self, repo: InMemoryWriteRepository[FakeEntity, str]
    ) -> None:
        """Test deleting a non-existent entity raises RepositoryNotFoundError."""
        with pytest.raises(RepositoryNotFoundError):
            await repo.delete_by_id("999")

    async def test_delete_by_id_none_raises_error(
        self, repo: InMemoryWriteRepository[FakeEntity, str]
    ) -> None:
        """Test deleting with None ID raises RepositoryError."""
        with pytest.raises(RepositoryError):
            await repo.delete_by_id(None)  # type: ignore[arg-type]

    async def test_delete_by_id_empty_string_raises_error(
        self, repo: InMemoryWriteRepository[FakeEntity, str]
    ) -> None:
        """Test deleting with empty string ID raises RepositoryError."""
        with pytest.raises(RepositoryError):
            await repo.delete_by_id("")

    async def test_delete_by_id_false_raises_error(
        self, repo: InMemoryWriteRepository[FakeEntity, str]
    ) -> None:
        """Test deleting with False ID raises RepositoryError."""
        with pytest.raises(RepositoryError):
            await repo.delete_by_id(False)  # type: ignore[arg-type]

    async def test_save_none_id_raises_error(
        self, repo: InMemoryWriteRepository[FakeEntity, str]
    ) -> None:
        """Test saving entity with None ID raises RepositoryError."""
        entity = FakeEntity(id=None, name="Alice")
        with pytest.raises(RepositoryError):
            await repo.save(entity)


class TestInMemoryRepository:
    """Tests for InMemoryRepository (full CRUD)."""

    @pytest.fixture
    def repo(self) -> InMemoryRepository[FakeEntity, str]:
        """Create an InMemoryRepository."""
        return InMemoryRepository[FakeEntity, str]()

    async def test_save_and_get_by_id(self, repo: InMemoryRepository[FakeEntity, str]) -> None:
        """Test saving and retrieving an entity."""
        entity = FakeEntity(id="1", name="Alice")
        await repo.save(entity)

        retrieved = await repo.get_by_id("1")
        assert retrieved is not None
        assert retrieved.name == "Alice"

    async def test_get_by_id_not_found(self, repo: InMemoryRepository[FakeEntity, str]) -> None:
        """Test getting a non-existent entity."""
        entity = await repo.get_by_id("999")
        assert entity is None

    async def test_list_all(self, repo: InMemoryRepository[FakeEntity, str]) -> None:
        """Test listing all entities."""
        await repo.save(FakeEntity(id="1", name="Alice"))
        await repo.save(FakeEntity(id="2", name="Bob"))

        entities = await repo.list_all()
        assert len(entities) == 2

    async def test_delete_and_verify(self, repo: InMemoryRepository[FakeEntity, str]) -> None:
        """Test deleting an entity and verifying it's gone."""
        entity = FakeEntity(id="1", name="Alice")
        await repo.save(entity)
        await repo.delete_by_id("1")

        assert await repo.get_by_id("1") is None

    async def test_delete_nonexistent_raises(
        self, repo: InMemoryRepository[FakeEntity, str]
    ) -> None:
        """Test deleting a non-existent entity raises error."""
        with pytest.raises(RepositoryNotFoundError):
            await repo.delete_by_id("999")

    async def test_exists_matching(self, repo: InMemoryRepository[FakeEntity, str]) -> None:
        """Test exists_matching with InMemoryRepository."""
        await repo.save(FakeEntity(id="1", name="Alice"))
        spec = FakeSpecification("Ali")
        exists = await repo.exists_matching(spec)
        assert exists is True
