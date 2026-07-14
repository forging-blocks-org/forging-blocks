"""``__setattr__`` override handler for auto-frozen classes.

Wraps a class's ``__setattr__`` to enforce frozen-attribute checks
at write time.
"""

from collections.abc import Callable
from typing import Any

from forging_blocks.foundation.autofreeze.helpers.frozen_state import (
    FrozenStateManager,
)
from forging_blocks.foundation.errors.cant_modify_immutable_attribute_error import (
    CantModifyImmutableAttributeError,
)


class FrozenSetattrHandler:
    """Produces a frozen-aware ``__setattr__`` for a target class.

    If the class already defines a custom ``__setattr__``, it is left
    untouched — we assume the author knows what they are doing.
    """

    def __init__(self, target_class: type[object]) -> None:
        """Initialise with the class whose setattr may be overridden.

        Args:
            target_class: The class being decorated by ``@auto_freeze``.
        """
        self.target_class = target_class
        self.original_setattr = target_class.__setattr__
        self.has_custom_setattr = self.original_setattr is not object.__setattr__

    def should_override_setattr(self) -> bool:
        """Return ``True`` when it is safe to replace ``__setattr__``."""
        return not self.has_custom_setattr

    def create_frozen_setattr(self) -> Callable[..., None]:
        """Build a ``__setattr__`` that enforces freeze rules.

        Returns:
            A callable suitable for assignment to ``cls.__setattr__``.
            When the class already has a custom setattr, the original is
            returned unchanged.
        """
        if self.has_custom_setattr:
            return self.original_setattr

        def frozen_setattr(instance: Any, name: str, value: Any) -> None:
            state = FrozenStateManager.get_state(instance)

            if state.is_full_freeze:
                raise CantModifyImmutableAttributeError(
                    class_name=instance.__class__.__name__,
                    attribute_name=name,
                )

            if state.frozen_attrs is not None and name in state.frozen_attrs:
                raise CantModifyImmutableAttributeError(
                    class_name=instance.__class__.__name__,
                    attribute_name=name,
                )

            object.__setattr__(instance, name, value)

        return frozen_setattr
