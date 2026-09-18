"""Decorators for message classes.

Provides ``@message_dataclass`` (and its aliases ``@event_dataclass``,
``@command_dataclass``, ``@query_dataclass``) to reduce boilerplate when
defining message types.  The decorated class is a frozen dataclass whose
fields are automatically exposed via ``get_payload_fields()`` and are used
by ``from_payload_fields()`` for reconstruction.

Example:
    ```python
    class OrderPayload:
        def __init__(self, order_id: str, customer_id: str, total: float) -> None:
            self.order_id = order_id
            self.customer_id = customer_id
            self.total = total


    class Event[T]:
        # Inline stub for the example.
        pass


    @event_dataclass
    class OrderCreated(Event[OrderPayload]):
        order_id: str
        customer_id: str
        total: float


    event = OrderCreated(order_id="ORD-001", customer_id="CUST-42", total=99.95)
    ```
"""

import dataclasses
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol, Self, TypeVar, cast, overload, runtime_checkable

from forging_blocks.domain.messages.message import Message, MessageMetadata

_M = TypeVar("_M", bound="Message[Any]")


@runtime_checkable
class _PatchedMessage(Protocol):
    """Structural type describing a message class after decorator patching.

    This protocol allows pyright to verify that the patched attributes exist
    and have the correct signatures, replacing attribute assignment suppressions
    with a proper type-safe cast boundary.

    Example:
        ```python
        @message_dataclass
        class OrderCreated(Event[dict[str, object]]):
            order_id: str


        decorated = OrderCreated
        assert isinstance(decorated, _PatchedMessage)

        fields = decorated.get_payload_fields()
        assert fields == {"order_id": "order_id"}

        from_payload = decorated.from_payload_fields(
            {"order_id": "ORD-001"},
            metadata=MessageMetadata(),
        )
        assert isinstance(from_payload, OrderCreated)
        assert from_payload.order_id == "ORD-001"
        ```
    """

    def get_payload_fields(self) -> dict[str, object]: ...

    @classmethod
    def from_payload_fields(
        cls,
        data: dict[str, object],
        metadata: MessageMetadata,
    ) -> Self: ...


def _frozen_setattr(self: object, name: str, value: object) -> None:
    """Raise FrozenInstanceError for attribute assignment after init."""
    if getattr(self, "__init_finished__", False):
        raise dataclasses.FrozenInstanceError(f"cannot assign to field {name!r}")
    object.__setattr__(self, name, value)


def _resolve_abstract_methods_to_remove(
    dc_cls: type[Any], abstract_methods: frozenset[str]
) -> set[str]:
    """Resolve which abstract methods to remove from the dataclass."""
    to_remove: set[str] = set()
    patched = cast(Any, dc_cls)
    if "_payload" in abstract_methods:
        patched._payload = property(lambda self: self.get_payload_fields())
        to_remove.add("_payload")
    if "value" in abstract_methods:
        patched.value = property(lambda self: self.get_payload_fields())
        to_remove.add("value")
    if "from_payload_fields" in abstract_methods:
        to_remove.add("from_payload_fields")
    return to_remove


def _patch_abstract_methods(dc_cls: type[Any]) -> None:
    """Patch abstract methods on the decorated message dataclass."""
    abstract_methods: frozenset[str] = getattr(dc_cls, "__abstractmethods__", frozenset())
    to_remove = _resolve_abstract_methods_to_remove(dc_cls, abstract_methods)
    if to_remove:
        dc_cls.__abstractmethods__ = frozenset(abstract_methods - to_remove)


def _validate_patched_message(dc_cls: type[Any]) -> None:
    """Validate that the decorated class satisfies the _PatchedMessage protocol."""
    if not isinstance(dc_cls, _PatchedMessage):
        raise TypeError(
            f"{dc_cls.__name__!r} does not satisfy _PatchedMessage after decoration. "
            "This is a bug in message_dataclass."
        )


def _create_message_init(
    original_init: Callable[..., None],
) -> Callable[..., None]:
    """Create the custom __init__ for message dataclasses."""

    def new_init(
        self: Any,
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

    return new_init


def _create_from_payload_fields(
    dc_cls: type[Any],
) -> classmethod[Any, Any, Any]:
    """Create the from_payload_fields classmethod for message dataclasses."""

    def from_payload_fields(
        cls: type[Any],
        data: dict[str, object],
        metadata: MessageMetadata,
    ) -> Any:
        fields = cast(Any, dc_cls).__dataclass_fields__
        unknown = data.keys() - fields.keys()
        if unknown:
            raise TypeError(f"Unknown field(s) in payload for {cls.__name__}: {sorted(unknown)}")
        return cls(metadata=metadata, **data)

    return classmethod(from_payload_fields)


def _wrap_message_dataclass(cls: type[_M]) -> type[_M]:
    """Decorate and patch a concrete message class."""
    dc_cls: type[_M] = dataclass(frozen=False, eq=False)(cls)
    dc_cls.__setattr__ = _frozen_setattr

    def get_payload_fields(self: _M) -> dict[str, object]:
        return {
            name: getattr(self, name)
            for name in cast(Any, dc_cls).__dataclass_fields__
            if not name.startswith("_") and name not in ("metadata",)
        }

    patched = cast(Any, dc_cls)
    patched.__init__ = _create_message_init(dc_cls.__init__)
    patched.get_payload_fields = get_payload_fields
    patched.from_payload_fields = _create_from_payload_fields(dc_cls)

    _patch_abstract_methods(dc_cls)
    _validate_patched_message(dc_cls)
    return dc_cls


@overload
def message_dataclass(cls: type[_M]) -> type[_M]: ...


@overload
def message_dataclass(
    cls: None = None,
) -> Callable[[type[_M]], type[_M]]: ...


def message_dataclass(
    cls: type[_M] | None = None,
) -> type[_M] | Callable[[type[_M]], type[_M]]:
    """Decorate a class as a message dataclass.

    The decorator applies ``@dataclass(frozen=False)`` and then replaces
    ``__setattr__`` with a custom implementation that raises
    ``FrozenInstanceError`` after ``__init__`` completes.  It also
    patches ``get_payload_fields`` and ``from_payload_fields`` onto the
    class so that payload data is automatically derived from its fields.

    When the decorated class inherits from an abstract base (e.g.
    `Event`, `Command`, `Query`), the decorator
    automatically patches ``_payload``, ``value``, and
    ``from_payload_fields`` — and removes them from ``__abstractmethods__``
    — so the concrete subclass is instantiable without manual stubs.

    Args:
        cls: The class to decorate (when used without arguments).

    Returns:
        The decorated class (or a wrapper when called with keyword arguments).
    """
    return _wrap_message_dataclass if cls is None else _wrap_message_dataclass(cls)


event_dataclass = message_dataclass
"""Alias for ``@message_dataclass`` intended for domain events."""

command_dataclass = message_dataclass
"""Alias for ``@message_dataclass`` intended for commands."""

query_dataclass = message_dataclass
"""Alias for ``@message_dataclass`` intended for queries."""
