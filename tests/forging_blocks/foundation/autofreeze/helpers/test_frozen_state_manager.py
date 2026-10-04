"""Tests for FrozenStateManager."""

import pytest


@pytest.mark.unit
class TestFrozenStateManagerStaleFallback:
    """Tests for FrozenStateManager stale fallback entry cleanup."""

    def test_read_is_frozen_when_stale_qualifier_then_deletes_entry_and_returns_false(
        self,
    ) -> None:
        from forging_blocks.foundation.autofreeze.helpers.frozen_state_manager import (
            FrozenStateManager,
        )

        class SomeClass:
            pass

        instance = SomeClass()
        key = FrozenStateManager._fallback_key(instance)
        FrozenStateManager._frozen_fallback[key] = ("WrongQualifier", True)

        try:
            result = FrozenStateManager._read_is_frozen(instance)
            assert result is False
            assert key not in FrozenStateManager._frozen_fallback
        finally:
            FrozenStateManager._frozen_fallback.pop(key, None)
            FrozenStateManager._refs_by_id.pop(key, None)

    def test_read_frozen_attrs_when_stale_qualifier_then_deletes_entry_and_returns_none(
        self,
    ) -> None:
        from forging_blocks.foundation.autofreeze.helpers.frozen_state_manager import (
            FrozenStateManager,
        )

        class SomeClass:
            pass

        instance = SomeClass()
        key = FrozenStateManager._fallback_key(instance)
        FrozenStateManager._frozen_attrs_fallback[key] = ("WrongQualifier", {"x", "y"})

        try:
            result = FrozenStateManager._read_frozen_attrs(instance)
            assert result is None
            assert key not in FrozenStateManager._frozen_attrs_fallback
        finally:
            FrozenStateManager._frozen_attrs_fallback.pop(key, None)
            FrozenStateManager._refs_by_id.pop(key, None)
