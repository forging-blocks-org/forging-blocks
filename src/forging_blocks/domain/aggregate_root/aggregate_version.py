"""AggregateVersion value object for optimistic concurrency control."""

from collections.abc import Hashable

from forging_blocks.foundation.value_object import ValueObject


class AggregateVersion(ValueObject[int]):
    """Immutable value object representing the version of an aggregate root.

    Used for optimistic concurrency control to detect conflicting updates.
    """

    __slots__ = ("_value",)

    def __init__(self, value: int) -> None:
        super().__init__()
        if value < 0:
            raise ValueError("Version cannot be negative")
        self._value = value

    @property
    def value(self) -> int:
        """Return the integer version value."""
        return self._value

    def increment(self) -> AggregateVersion:
        """Return a new AggregateVersion incremented by one."""
        return AggregateVersion(self._value + 1)

    @property
    def _equality_components(self) -> tuple[Hashable, ...]:
        """Components used for equality comparison."""
        return (self._value,)
