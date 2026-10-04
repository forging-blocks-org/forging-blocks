import pytest

from forging_blocks.foundation.autofreeze.helpers.frozen_setattr_handler import (
    FrozenSetattrHandler,
)


@pytest.mark.unit
class TestFrozenSetattrHandler:
    def test_when_target_has_custom_setattr_then_delegates_unfrozen_assignment(self) -> None:
        class CustomSetattr:
            value: int
            assigned: tuple[str, int] | None

            def __init__(self) -> None:
                object.__setattr__(self, "value", 1)
                object.__setattr__(self, "assigned", None)

            def __setattr__(self, name: str, value: object) -> None:
                if name == "value":
                    object.__setattr__(self, "assigned", (name, value))
                object.__setattr__(self, name, value)

        instance = CustomSetattr()
        handler = FrozenSetattrHandler(CustomSetattr)

        handler.create_frozen_setattr()(instance, "value", 2)

        assert instance.assigned == ("value", 2)
        assert instance.value == 2
