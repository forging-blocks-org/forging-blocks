"""Internal constants for frozen-state tracking."""

AUTO_FREEZE_MARKER = "__auto_freeze_applied"
FROZEN_FLAG = "_autofreeze__frozen"
FROZEN_ATTRS_FLAG = "_autofreeze__frozen_attrs"
INIT_DEPTH_FLAG = "_autofreeze__init_depth"
INTERNAL_STATE_ATTRIBUTES: frozenset[str] = frozenset(
    {FROZEN_FLAG, FROZEN_ATTRS_FLAG, INIT_DEPTH_FLAG}
)
