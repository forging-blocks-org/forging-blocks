"""Shared Order entity implementation for domain tests."""

from forging_blocks.domain import Entity


class Order(Entity[int]):
    """Entity implementation used by lifecycle tests."""

    def __init__(self, order_id: int) -> None:
        """Initialize an order with its identity assigned during construction."""
        self._id = order_id
