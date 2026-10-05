"""Shared User entity implementation for domain tests."""

from forging_blocks.domain import Entity


class User(Entity[int]):
    """Entity implementation used by domain behavior tests."""

    def __init__(self, entity_id: int | None = None, name: str = "") -> None:
        """Initialize a user with an optional identity and name."""
        super().__init__(entity_id)
        self.name = name
