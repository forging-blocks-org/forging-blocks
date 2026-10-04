"""``__setattr__`` override handler for auto-frozen classes.

Wraps a class's ``__setattr__`` to enforce frozen-attribute checks
at write time and protect auto-freeze state attributes.
"""

from collections.abc import Callable
from typing import Any

from forging_blocks.foundation.autofreeze.helpers.frozen_state_manager import FrozenStateManager
from forging_blocks.foundation.errors.cant_modify_immutable_attribute_error import (
    CantModifyImmutableAttributeError,
)


class FrozenSetattrHandler:
    """Produces a frozen-aware ``__setattr__`` for a target class.

    The decorator always performs frozen-state checks before delegating to a
    class's original assignment behavior.
    """

    def __init__(
        self,
        target_class: type[object],
        *,
        custom_mutator_attrs: frozenset[str] = frozenset(),
    ) -> None:
        """Initialize with the class whose setattr may be overridden.

        Args:
            target_class: The class being decorated by ``@auto_freeze``.
            custom_mutator_attrs: Frozen attributes whose domain-owned
                mutator should receive the assignment before generic checks.

        """
        self.original_setattr: Callable[..., None] = target_class.__setattr__
        self.has_custom_setattr: bool = self.original_setattr is not object.__setattr__
        self.custom_mutator_attrs = custom_mutator_attrs

    def create_frozen_setattr(self) -> Callable[..., None]:
        """Build a ``__setattr__`` that enforces freeze rules.

        Returns:
            A callable suitable for assignment to ``cls.__setattr__``.

        """

        def frozen_setattr(instance: Any, name: str, value: Any) -> None:
            if self.has_custom_setattr and name in self.custom_mutator_attrs:
                self.original_setattr(instance, name, value)
                return

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

            if self.has_custom_setattr:
                self.original_setattr(instance, name, value)
                return

            object.__setattr__(instance, name, value)

        return frozen_setattr
