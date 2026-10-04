"""Frozen state configuration value object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FrozenStateConfig:
    """Read-only snapshot of an instance's frozen state.

    Example:
        ```python
        config = FrozenStateConfig(is_full_freeze=True, frozen_attrs=None)
        assert config.is_full_freeze
        assert config.frozen_attrs is None

        partial = FrozenStateConfig(is_full_freeze=False, frozen_attrs=frozenset(["name"]))
        assert "name" in partial.frozen_attrs
        ```
    """

    is_full_freeze: bool
    frozen_attrs: frozenset[str] | None
