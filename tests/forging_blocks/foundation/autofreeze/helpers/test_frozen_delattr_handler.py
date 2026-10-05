import pytest

from forging_blocks.foundation.autofreeze.helpers.frozen_delattr_handler import (
    FrozenDelattrHandler,
)
from forging_blocks.foundation.autofreeze.helpers.frozen_state_manager import (
    FrozenStateManager,
)


@pytest.mark.unit
class TestFrozenDelattrHandler:
    def test_when_target_has_custom_delattr_then_delegates_unfrozen_deletion(self) -> None:
        class CustomDelattr:
            value: int
            deleted: str | None

            def __init__(self) -> None:
                object.__setattr__(self, "value", 1)
                object.__setattr__(self, "deleted", None)

            def __delattr__(self, name: str) -> None:
                object.__setattr__(self, "deleted", name)

        instance = CustomDelattr()
        handler = FrozenDelattrHandler(CustomDelattr)

        handler.create_frozen_delattr()(instance, "value")

        assert instance.deleted == "value"
        assert instance.value == 1

    def test_when_target_has_custom_mutator_attr_then_delegates_deletion_to_custom_delattr(
        self,
    ) -> None:
        class CustomDelattr:
            value: int
            deleted: str | None

            def __init__(self) -> None:
                object.__setattr__(self, "value", 1)
                object.__setattr__(self, "deleted", None)

            def __delattr__(self, name: str) -> None:
                object.__setattr__(self, "deleted", name)

        instance = CustomDelattr()
        FrozenStateManager.apply_selective_freeze(instance, ["value"])
        handler = FrozenDelattrHandler(
            CustomDelattr,
            custom_mutator_attrs=frozenset({"value"}),
        )

        handler.create_frozen_delattr()(instance, "value")

        assert instance.deleted == "value"
