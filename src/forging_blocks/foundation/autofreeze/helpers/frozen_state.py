"""Frozen state management for the auto_freeze decorator.

Provides state flags, configuration objects, and a central manager that
tracks init depth and freeze state on decorated instances.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import cast

_AUTO_FREEZE_MARKER = "__auto_freeze_applied"
_FROZEN_FLAG = "_autofreeze__frozen"
_FROZEN_ATTRS_FLAG = "_autofreeze__frozen_attrs"
_INIT_DEPTH_FLAG = "_autofreeze__init_depth"


@dataclass(frozen=True)
class FrozenStateConfig:
    """Read-only snapshot of an instance's frozen state."""

    is_full_freeze: bool
    frozen_attrs: frozenset[str] | None


class FrozenStateManager:
    """Central state tracker for auto-frozen instances.

    State is stored on instances via ``object.__setattr__`` when possible,
    falling back to per-type dicts for instances using ``__slots__`` without
    the tracking attributes. Fallback entries are guarded by a type qualifier
    so that ``id`` reuse across different classes does not leak state.
    """

    _init_depth_fallback: dict[int, tuple[str, int]] = {}
    _frozen_fallback: dict[int, tuple[str, bool]] = {}
    _frozen_attrs_fallback: dict[int, tuple[str, set[str]]] = {}

    @classmethod
    def _qualname_of(cls, instance: object) -> str:
        return type(instance).__qualname__

    @classmethod
    def _read_init_depth(cls, instance: object) -> int:
        try:
            return cast(int, getattr(instance, _INIT_DEPTH_FLAG))
        except AttributeError:
            entry = cls._init_depth_fallback.get(id(instance))
            if entry is not None and entry[0] == cls._qualname_of(instance):
                return entry[1]
            return 0

    @classmethod
    def _write_init_depth(cls, instance: object, depth: int) -> None:
        try:
            object.__setattr__(instance, _INIT_DEPTH_FLAG, depth)
        except AttributeError:
            cls._init_depth_fallback[id(instance)] = (cls._qualname_of(instance), depth)

    @classmethod
    def _erase_init_depth(cls, instance: object) -> None:
        try:
            object.__delattr__(instance, _INIT_DEPTH_FLAG)
        except (AttributeError, TypeError):
            pass
        cls._init_depth_fallback.pop(id(instance), None)

    @classmethod
    def _read_is_frozen(cls, instance: object) -> bool:
        if cls._read_init_depth(instance) > 0:
            return False
        try:
            return cast("bool", getattr(instance, _FROZEN_FLAG))
        except AttributeError:
            entry = cls._frozen_fallback.get(id(instance))
            if entry is None:
                return False
            qualifier, value = entry
            if qualifier == cls._qualname_of(instance):
                return value
            del cls._frozen_fallback[id(instance)]
            return False

    @classmethod
    def _write_is_frozen(cls, instance: object, value: bool) -> None:
        try:
            object.__setattr__(instance, _FROZEN_FLAG, value)
        except AttributeError:
            cls._frozen_fallback[id(instance)] = (cls._qualname_of(instance), value)

    @classmethod
    def _read_frozen_attrs(cls, instance: object) -> set[str] | None:
        if cls._read_init_depth(instance) > 0:
            return None
        try:
            return cast("set[str] | None", getattr(instance, _FROZEN_ATTRS_FLAG))
        except AttributeError:
            entry = cls._frozen_attrs_fallback.get(id(instance))
            if entry is None:
                return None
            qualifier, value = entry
            if qualifier == cls._qualname_of(instance):
                return value
            del cls._frozen_attrs_fallback[id(instance)]
            return None

    @classmethod
    def _write_frozen_attrs(cls, instance: object, attrs: set[str]) -> None:
        try:
            object.__setattr__(instance, _FROZEN_ATTRS_FLAG, attrs)
        except AttributeError:
            cls._frozen_attrs_fallback[id(instance)] = (cls._qualname_of(instance), attrs)

    @classmethod
    def get_state(cls, instance: object) -> FrozenStateConfig:
        """Return the current frozen-state snapshot for *instance*."""
        is_frozen = cls._read_is_frozen(instance)
        frozen_attrs = cls._read_frozen_attrs(instance)
        frozen = frozenset(frozen_attrs) if frozen_attrs is not None else None
        return FrozenStateConfig(is_full_freeze=is_frozen, frozen_attrs=frozen)

    @classmethod
    def mark_as_decorated(cls, init_method: object) -> None:
        """Tag *init_method* so that ``is_decorated`` returns ``True``."""
        object.__setattr__(init_method, _AUTO_FREEZE_MARKER, True)

    @classmethod
    def is_decorated(cls, init_method: object) -> bool:
        """Return ``True`` when *init_method* was already wrapped by auto_freeze."""
        return hasattr(init_method, _AUTO_FREEZE_MARKER)

    @classmethod
    def increment_init_depth(cls, instance: object) -> None:
        """Increment the init-depth counter for *instance*."""
        cls._write_init_depth(instance, cls._read_init_depth(instance) + 1)

    @classmethod
    def decrement_init_depth(cls, instance: object) -> int:
        """Decrement the init-depth counter and return the new depth.

        When depth reaches zero the entry is erased from state.
        """
        new_depth = cls._read_init_depth(instance) - 1
        if new_depth <= 0:
            cls._erase_init_depth(instance)
        else:
            cls._write_init_depth(instance, new_depth)
        return new_depth

    @classmethod
    def apply_full_freeze(cls, instance: object) -> None:
        """Mark *instance* as fully frozen (all attributes immutable)."""
        cls._write_is_frozen(instance, True)

    @classmethod
    def apply_selective_freeze(cls, instance: object, attrs: Sequence[str]) -> None:
        """Mark only the given *attrs* as frozen on *instance*."""
        cls._write_frozen_attrs(instance, set(attrs))
