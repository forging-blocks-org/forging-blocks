"""``__init__`` wrapper that applies freeze after construction completes.

The wrapper tracks init-depth to handle inheritance chains: freeze is
only applied when the outermost ``__init__`` returns (depth == 0),
and only for concrete (non-abstract) classes.
"""

import inspect
from collections.abc import Callable, Sequence
from functools import wraps
from typing import Any

from forging_blocks.foundation.autofreeze.helpers.frozen_state import (
    FrozenStateManager,
)


class FrozenInitWrapper:
    """Wraps ``__init__`` to apply freeze state after construction.

    The wrapper:
    1. Increments the init-depth counter before calling the original init.
    2. Calls the original ``__init__``.
    3. Decrements the depth in a ``finally`` block.
    4. When depth reaches zero and the class is concrete, applies the
       appropriate freeze (full or selective).
    """

    def __init__(
        self,
        original_init: Callable[..., None],
        target_class: type[object],
        freeze_attrs: Sequence[str] | None,
    ) -> None:
        """Initialise the wrapper.

        Args:
            original_init: The original ``__init__`` method to wrap.
            target_class: The class being decorated.
            freeze_attrs: Attribute names for selective freezing, or
                ``None`` for full freeze.

        """
        self.original_init = original_init
        self.target_class = target_class
        self.freeze_attrs = freeze_attrs

    def wrap(self) -> Callable[..., None]:
        """Return the wrapped ``__init__``, tagged with the auto-freeze marker.

        Returns:
            A callable to assign to ``cls.__init__``.

        """

        @wraps(self.original_init)
        def wrapped_init(instance: Any, *args: Any, **kwargs: Any) -> None:
            FrozenStateManager.increment_init_depth(instance)

            try:
                self.original_init(instance, *args, **kwargs)
            finally:
                new_depth = FrozenStateManager.decrement_init_depth(instance)

                if new_depth == 0 and not inspect.isabstract(self.target_class):
                    if self.freeze_attrs is None:
                        FrozenStateManager.apply_full_freeze(instance)
                    else:
                        FrozenStateManager.apply_selective_freeze(instance, self.freeze_attrs)

        FrozenStateManager.mark_as_decorated(wrapped_init)
        return wrapped_init
