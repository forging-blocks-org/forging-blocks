"""Callable implementation for the auto_freeze decorator."""

from collections.abc import Sequence

from forging_blocks.foundation.autofreeze.helpers.frozen_init_wrapper import (
    FrozenInitWrapper,
)
from forging_blocks.foundation.autofreeze.helpers.frozen_setattr_handler import (
    FrozenSetattrHandler,
)
from forging_blocks.foundation.autofreeze.helpers.frozen_state_manager import (
    FrozenStateManager,
)


class AutoFreezeDecorator:
    """Callable class that applies auto-freeze behaviour to a target class.

    Injects a ``__setattr__`` that prevents modifications to frozen attributes.
    No protocol implementation is required on the target class.

    Example:
        ```python
        class Config:
            def __init__(self, value: str) -> None:
                self.value = value


        decorator = _AutoFreezeDecorator()
        Config = decorator(Config)
        c = Config("read-only")
        # c.value = "new" would raise CantModifyImmutableAttributeError
        ```
    """

    def __init__(
        self,
        *,
        attrs: Sequence[str] | None = None,
    ) -> None:
        """Initialise the decorator with optional selective-freeze attributes.

        Args:
            attrs: Attribute names to selectively freeze. When ``None``
                (the default), the entire instance is frozen. When provided,
                only those attributes are frozen.

        """
        self._attrs = attrs

    def __call__[T](self, class_: type[T]) -> type[T]:
        """Apply the auto-freeze behaviour to *class_*.

        Injects a frozen state marker and wraps ``__setattr__`` to enforce
        immutability. If *class_* has already been decorated (detected via
        an internal marker), returns the class unchanged to avoid double-wrapping.

        Args:
            class_: The target class to decorate.

        Returns:
            The decorated class (may be the original if already decorated).

        """
        if FrozenStateManager.is_decorated(class_.__init__):
            return class_

        init_wrapper = FrozenInitWrapper(class_.__init__, class_, self._attrs)
        class_.__init__ = init_wrapper.wrap()

        setattr_handler = FrozenSetattrHandler(class_)
        if setattr_handler.should_override_setattr():
            class_.__setattr__ = setattr_handler.create_frozen_setattr()

        return class_


__all__ = ["AutoFreezeDecorator"]
