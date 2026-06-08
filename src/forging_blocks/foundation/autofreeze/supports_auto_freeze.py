from typing import Protocol # pragma: no cover


class SupportsAutoFreeze(Protocol):
    """Contract required by the internal auto-freeze mechanism."""

    @classmethod
    def should_use_internal_freezing(cls) -> bool:
        """Determine whether toolkit-managed freezing should be used."""
        ...

    def freeze_instance(self) -> None:
        """Transition the instance into an immutable state."""
        ...

    def unfreeze_instance(self) -> None:
        """Transition the instance into a mutable state."""
        ...
