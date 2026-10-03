import pytest

from forging_blocks.foundation.autofreeze.helpers.frozen_state_config import FrozenStateConfig


@pytest.mark.unit
class TestFrozenStateConfig:
    def test_when_created_with_full_freeze_then_exposes_snapshot(self) -> None:
        config = FrozenStateConfig(is_full_freeze=True, frozen_attrs=None)

        assert config.is_full_freeze is True
        assert config.frozen_attrs is None

    def test_when_created_with_selected_attributes_then_exposes_snapshot(self) -> None:
        config = FrozenStateConfig(is_full_freeze=False, frozen_attrs=frozenset({"name"}))

        assert config.is_full_freeze is False
        assert config.frozen_attrs == frozenset({"name"})
