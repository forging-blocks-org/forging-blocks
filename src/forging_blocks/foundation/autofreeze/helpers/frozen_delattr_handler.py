"""``__delattr__`` override handler for auto-frozen classes.

Wraps a class's ``__delattr__`` to enforce frozen-attribute checks
at deletion time and protect auto-freeze state attributes.
"""

from collections.abc import Callable

from forging_blocks.foundation.autofreeze.helpers.frozen_state_manager import FrozenStateManager
from forging_blocks.foundation.errors.cant_modify_immutable_attribute_error import (
    CantModifyImmutableAttributeError,
)


class FrozenDelattrHandler:
    """Produces a frozen-aware ``__delattr__`` for a target class.

    The decorator always performs frozen-state checks before delegating to a
    class's original deletion behavior.
    """

    def __init__(self, target_class: type[object]) -> None:
        """Initialize with the class whose delattr may be overridden.

        Args:
            target_class: The class being decorated by ``@auto_freeze``.

        """
        self.original_delattr: Callable[[object, str], None] = target_class.__delattr__
        self.has_custom_delattr: bool = self.original_delattr is not object.__delattr__

    def create_frozen_delattr(self) -> Callable[[object, str], None]:
        """Build a ``__delattr__`` that enforces freeze rules.

        Returns:
            A callable suitable for assignment to ``cls.__delattr__``.

        """

        def frozen_delattr(instance: object, name: str) -> None:
            if FrozenStateManager.is_internal_attribute(name):
                raise CantModifyImmutableAttributeError(
                    class_name=type(instance).__name__,
                    attribute_name=name,
                )

            state = FrozenStateManager.get_state(instance)
            if state.is_full_freeze or (
                state.frozen_attrs is not None and name in state.frozen_attrs
            ):
                raise CantModifyImmutableAttributeError(
                    class_name=type(instance).__name__,
                    attribute_name=name,
                )

            if self.has_custom_delattr:
                self.original_delattr(instance, name)
                return

            object.__delattr__(instance, name)

        return frozen_delattr
