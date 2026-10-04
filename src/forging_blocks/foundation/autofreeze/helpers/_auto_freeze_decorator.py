"""Callable implementation for the auto_freeze decorator."""

import inspect
from collections.abc import Sequence

from forging_blocks.foundation.autofreeze.helpers.frozen_delattr_handler import (
    FrozenDelattrHandler,
)
from forging_blocks.foundation.autofreeze.helpers.frozen_init_wrapper import FrozenInitWrapper
from forging_blocks.foundation.autofreeze.helpers.frozen_setattr_handler import (
    FrozenSetattrHandler,
)
from forging_blocks.foundation.autofreeze.helpers.frozen_state_manager import FrozenStateManager


class AutoFreezeDecorator:
    """Callable class that applies auto-freeze behaviour to a target class.

    Injects ``__setattr__`` and ``__delattr__`` overrides that prevent
    modifications to frozen attributes. No protocol implementation is required
    on the target class.
    """

    def __init__(self, *, attrs: Sequence[str] | None = None) -> None:
        """Initialize the decorator with selective-freeze attributes."""
        self._attrs = attrs

    def __call__[T](self, class_: type[T]) -> type[T]:
        if inspect.isabstract(class_):
            return class_
        if FrozenStateManager.is_decorated(class_.__init__):
            return class_

        init_wrapper = FrozenInitWrapper(class_.__init__, class_, self._attrs)
        class_.__init__ = init_wrapper.wrap()

        setattr_handler = FrozenSetattrHandler(class_)
        class_.__setattr__ = setattr_handler.create_frozen_setattr()

        delattr_handler = FrozenDelattrHandler(class_)
        class_.__delattr__ = delattr_handler.create_frozen_delattr()

        return class_


__all__ = ["AutoFreezeDecorator"]
