"""Frozen state management for the auto_freeze decorator.

Provides state flags, configuration objects, and a central manager that
tracks init depth and freeze state on decorated instances.

Fallback storage uses weak references when the instance supports them,
so entries are automatically cleaned up when the instance is garbage
collected.  For slotted classes that exclude ``__weakref__``, the
manager falls back to ``id()``-keyed dicts with a type-qualifier guard
to prevent stale reads from ``id`` reuse.
"""

import weakref
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

    Stores per-instance init-depth, frozen-flag, and frozen-attrs state.
    For classes whose instances support weak references the entries are
    automatically cleaned up on garbage collection.  For slotted classes
    that exclude ``__weakref__`` the ``id()`` entries persist until the
    end of the process — their count is bounded by the number of
    concurrently-live instances, which is acceptable for typical
    workloads.

    All internal dicts are keyed by ``id(instance)`` (an :class:`int`)
    so that lookups never trigger ``__hash__`` on the instance — the
    instance may still be inside ``__init__`` and its fields may not be
    populated yet.
    """

    _RefKey = int
    """Key type for all internal tracking dicts — always ``id(instance)``."""

    _refs_by_id: dict[_RefKey, weakref.ReferenceType[object]] = {}
    """``id(instance)`` → ``weakref.ref``.

    Maintained only for instances that support weak references so that
    the callback can clean up stale entries from the fallback dicts when
    the instance is garbage-collected.  Slotted classes without
    ``__weakref__`` are absent from this map.
    """

    _init_depth_fallback: dict[_RefKey, tuple[str, int]] = {}
    _frozen_fallback: dict[_RefKey, tuple[str, bool]] = {}
    _frozen_attrs_fallback: dict[_RefKey, tuple[str, set[str]]] = {}
    # ------------------------------------------------------------------
    # key management
    # ------------------------------------------------------------------

    @classmethod
    def _fallback_key(cls, instance: object) -> _RefKey:
        """Return the stable ``id(instance)`` key used in all tracking dicts.

        As a side effect, registers a :class:`weakref.ref` for instances
        that support weak references so that entries are cleaned up on
        garbage collection.
        """
        iid = id(instance)
        if iid in cls._refs_by_id:
            return iid
        try:
            ref: weakref.ReferenceType[object] = weakref.ref(instance, cls._cleanup_fallback)
        except TypeError:
            # Instance does not support weak references (slotted without
            # ``__weakref__``).  No cleanup; entries persist until exit.
            pass
        else:
            cls._refs_by_id[iid] = ref
        return iid

    @classmethod
    def _cleanup_fallback(cls, ref: weakref.ReferenceType[object]) -> None:
        """Remove all per-instance entries from every tracking dict.

        Installed as the callback on every :class:`weakref.ref` stored in
        :attr:`_refs_by_id`.  Called automatically by the runtime when the
        referent is garbage-collected.
        """
        # Find the id that maps to this ref.
        for iid, cached in list(cls._refs_by_id.items()):
            if cached is ref:
                del cls._refs_by_id[iid]
                cls._init_depth_fallback.pop(iid, None)
                cls._frozen_fallback.pop(iid, None)
                cls._frozen_attrs_fallback.pop(iid, None)
                return

    # ------------------------------------------------------------------
    # init depth
    # ------------------------------------------------------------------

    @classmethod
    def _qualname_of(cls, instance: object) -> str:
        return type(instance).__qualname__

    @classmethod
    def _read_init_depth(cls, instance: object) -> int:
        try:
            return cast(int, getattr(instance, _INIT_DEPTH_FLAG))
        except AttributeError:
            key = cls._fallback_key(instance)
            entry = cls._init_depth_fallback.get(key)
            if entry is not None and entry[0] == cls._qualname_of(instance):
                return entry[1]
            return 0

    @classmethod
    def _write_init_depth(cls, instance: object, depth: int) -> None:
        try:
            object.__setattr__(instance, _INIT_DEPTH_FLAG, depth)
        except AttributeError:
            cls._init_depth_fallback[cls._fallback_key(instance)] = (
                cls._qualname_of(instance),
                depth,
            )

    @classmethod
    def _erase_init_depth(cls, instance: object) -> None:
        try:
            object.__delattr__(instance, _INIT_DEPTH_FLAG)
        except (AttributeError, TypeError):
            # Instance cannot have the tracking attribute removed
            # (e.g., it was never set, or the class is slotted).
            # Fallback map cleanup happens unconditionally below.
            pass
        cls._init_depth_fallback.pop(cls._fallback_key(instance), None)

    # ------------------------------------------------------------------
    # frozen flag
    # ------------------------------------------------------------------
    @classmethod
    def _read_is_frozen(cls, instance: object) -> bool:
        if cls._read_init_depth(instance) > 0:
            return False
        try:
            return cast("bool", getattr(instance, _FROZEN_FLAG))
        except AttributeError:
            key = cls._fallback_key(instance)
            entry = cls._frozen_fallback.get(key)
            if entry is None:
                return False
            qualifier, value = entry
            if qualifier == cls._qualname_of(instance):
                return value
            del cls._frozen_fallback[key]
            return False

    @classmethod
    def _write_is_frozen(cls, instance: object, value: bool) -> None:
        try:
            object.__setattr__(instance, _FROZEN_FLAG, value)
        except AttributeError:
            cls._frozen_fallback[cls._fallback_key(instance)] = (
                cls._qualname_of(instance),
                value,
            )

    # ------------------------------------------------------------------
    # frozen attrs
    # ------------------------------------------------------------------

    @classmethod
    def _read_frozen_attrs(cls, instance: object) -> set[str] | None:
        if cls._read_init_depth(instance) > 0:
            return None
        try:
            return cast("set[str] | None", getattr(instance, _FROZEN_ATTRS_FLAG))
        except AttributeError:
            key = cls._fallback_key(instance)
            entry = cls._frozen_attrs_fallback.get(key)
            if entry is None:
                return None
            qualifier, value = entry
            if qualifier == cls._qualname_of(instance):
                return value
            del cls._frozen_attrs_fallback[key]
            return None

    @classmethod
    def _write_frozen_attrs(cls, instance: object, attrs: set[str]) -> None:
        try:
            object.__setattr__(instance, _FROZEN_ATTRS_FLAG, attrs)
        except AttributeError:
            cls._frozen_attrs_fallback[cls._fallback_key(instance)] = (
                cls._qualname_of(instance),
                attrs,
            )

    # ------------------------------------------------------------------
    # public api
    # ------------------------------------------------------------------

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
