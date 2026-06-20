"""Decorators for message classes.

Provides ``@message_dataclass`` (and its aliases ``@event_dataclass``,
``@command_dataclass``, ``@query_dataclass``) to reduce boilerplate when
defining message types.  The decorated class is a frozen dataclass whose
fields are automatically exposed via ``get_payload_fields()`` and are used
by ``_from_payload_fields()`` for deserialisation.

Example::

    from forging_blocks.foundation.messages.decorators import event_dataclass
    from forging_blocks.foundation.messages.event import Event


    @event_dataclass
    class OrderCreated(Event[dict[str, object]]):
        order_id: str
        customer_id: str
        total: float


    event = OrderCreated(order_id="ORD-001", customer_id="CUST-42", total=99.95)
    event.to_dict()  # includes both "payload" and "data" keys
"""

import dataclasses
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol, Self, TypeVar, cast, overload, runtime_checkable

from forging_blocks.foundation.messages.message import Message, MessageMetadata

_M = TypeVar("_M", bound="Message[dict[str, object]]")


@runtime_checkable
class _PatchedMessage(Protocol):
    """Structural type describing a message class after decorator patching.

    This protocol allows pyright to verify that the patched attributes exist
    and have the correct signatures, replacing attribute assignment suppressions
    with a proper type-safe cast boundary.
    """

    def get_payload_fields(self) -> dict[str, object]: ...

    @classmethod
    def _from_payload_fields(
        cls,
        data: dict[str, object],
        metadata: MessageMetadata,
    ) -> type[Self]: ...


@overload
def message_dataclass(cls: type[_M]) -> type[_M]: ...


@overload
def message_dataclass(
    cls: None = None,
    *,
    frozen: bool = True,
) -> Callable[[type[_M]], type[_M]]: ...


def message_dataclass(
    cls: type[_M] | None = None,
    *,
    frozen: bool = True,
) -> type[_M] | Callable[[type[_M]], type[_M]]:
    """Decorate a class as a message dataclass.

    The decorator applies ``@dataclass(frozen=frozen)`` and then patches
    ``get_payload_fields`` and ``_from_payload_fields`` onto the class so
    that payload data is automatically derived from its fields.

    Args:
        cls: The class to decorate (when used without arguments).
        frozen: Whether the dataclass should be frozen (default ``True``).

    Returns:
        The decorated class (or a wrapper when called with keyword arguments).
    """

    def wrap(cls: type[_M]) -> type[_M]:
        dc_cls: type[_M] = dataclass(frozen=False)(cls)

        original_init = dc_cls.__init__

        def frozen_setattr(self: object, name: str, value: object) -> None:
            """Raise FrozenInstanceError for attribute assignment after init."""
            if getattr(self, "__init_finished__", False):
                raise dataclasses.FrozenInstanceError(f"cannot assign to field {name!r}")
            object.__setattr__(self, name, value)

        def new_init(
            self: _M,
            *args: Any,
            metadata: MessageMetadata | None = None,
            **kwargs: Any,
        ) -> None:
            object.__setattr__(self, "__init_finished__", False)
            original_init(self, *args, **kwargs)
            effective_type = type(self).__name__
            object.__setattr__(
                self, "_metadata", metadata or MessageMetadata(message_type=effective_type)
            )
            object.__setattr__(self, "__init_finished__", True)

        dc_cls.__setattr__ = frozen_setattr

        def get_payload_fields(self: _M) -> dict[str, object]:
            return {
                name: getattr(self, name)
                for name in cast(Any, dc_cls).__dataclass_fields__
                if not name.startswith("_") and name not in ("metadata",)
            }

        @classmethod
        def _from_payload_fields(
            cls: type[_M],
            data: dict[str, object],
            metadata: MessageMetadata,
        ) -> _M:
            return cls(metadata=metadata, **data)

        # Pyright cannot verify attribute assignment on a closed generic class.
        # We use setattr with explicit string keys and validate the result against
        # _PatchedMessage to preserve type safety without suppression comments.
        dc_cls.__init__ = new_init
        dc_cls.get_payload_fields = get_payload_fields
        dc_cls._from_payload_fields = _from_payload_fields

        # Patch abstract members so decorated subclasses of Event/Command/Query
        # can be instantiated without manually implementing _payload / value.
        # ``_from_payload_fields`` is intentionally not patched here: it is never
        # declared abstract by the Message hierarchy, so it cannot appear in
        # ``__abstractmethods__``. It is added explicitly above via setattr.
        abstract_methods: frozenset[str] = getattr(dc_cls, "__abstractmethods__", frozenset())
        if "_payload" in abstract_methods:
            dc_cls._payload = property(lambda self: self.get_payload_fields())
            dc_cls.__abstractmethods__ = frozenset(
                m for m in dc_cls.__abstractmethods__ if m != "_payload"
            )
        if "value" in abstract_methods:
            dc_cls.value = property(lambda self: self.get_payload_fields())
            dc_cls.__abstractmethods__ = frozenset(
                m for m in dc_cls.__abstractmethods__ if m != "value"
            )

        assert isinstance(dc_cls, _PatchedMessage), (
            f"{dc_cls.__name__!r} does not satisfy _PatchedMessage after decoration. "
            "This is a bug in message_dataclass."
        )

        return cast(type[_M], dc_cls)

    return wrap if cls is None else wrap(cls)


event_dataclass = message_dataclass
"""Alias for ``@message_dataclass`` intended for domain events."""

command_dataclass = message_dataclass
"""Alias for ``@message_dataclass`` intended for commands."""

query_dataclass = message_dataclass
"""Alias for ``@message_dataclass`` intended for queries."""
