"""Protocol for classes that support the auto-freeze mechanism."""

from typing import Protocol, Sequence


class SupportsAutoFreeze(Protocol):  # pragma: no cover
    """Contract for classes compatible with the @auto_freeze decorator.

    Implementers must provide methods to transition between mutable and
    immutable states. The @auto_freeze decorator calls these methods
    based on class configuration.

    Example:
        ```python
        @auto_freeze
        class Email(ValueObject[str]):
            def freeze_instance(self) -> None:
                object.__setattr__(self, "_Email__is_frozen", True)

            def unfreeze_instance(self) -> None:
                object.__setattr__(self, "_Email__is_frozen", False)

            @classmethod
            def should_use_internal_freezing(cls) -> bool:
                return True
        ```
    """

    @classmethod
    def should_use_internal_freezing(cls) -> bool:
        """Determine whether the decorator should auto-freeze on init.

        Returns:
            True if instances should be automatically frozen after __init__
            completes, False to opt out of automatic freezing.

        Notes:
            - Override to return False to disable auto-freeze for a class tree.
            - Decorator checks this at runtime before calling freeze_instance().
        """
        ...

    def freeze_instance(self) -> None:
        """Transition the instance into an immutable state.

        Called automatically by @auto_freeze after __init__ completes
        (if should_use_internal_freezing() returns True).

        Responsibilities:
            - Mark the instance as frozen.
            - Prevent future attribute modifications.
            - Raise CantModifyImmutableAttributeError on __setattr__.

        Notes:
            - Implementation details are class-specific.
            - May use internal flags or other mechanisms.
        """
        ...

    def unfreeze_instance(self) -> None:
        """Transition the instance into a mutable state.

        Typically used only in testing or rollback scenarios.
        Normal application code should not call this directly.

        Responsibilities:
            - Remove the frozen marker.
            - Allow subsequent attribute modifications.

        Notes:
            - Use sparingly; violates immutability contract.
            - Intended for test setup/teardown and transaction rollback.
        """
        ...

    def freeze_attributes(self, attrs: Sequence[str]) -> None:
        """Selectively freeze specific attributes.

        Optional method for classes that support partial freezing.
        If not implemented, freeze_instance() is called instead.

        Args:
            attrs: Attribute names to freeze (e.g., ["_id"]).

        Notes:
            - Useful for Entities where only identity should be immutable.
            - Default behavior (if not overridden): freeze_instance().
        """
        ...
