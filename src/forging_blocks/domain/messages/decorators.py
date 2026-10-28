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
from typing import Any, cast, overload

from forging_blocks.domain.messages.command import Command
from forging_blocks.domain.messages.event import Event
from forging_blocks.domain.messages.helpers._patched_message import (
    PatchedMessage as _PatchedMessage,
)
from forging_blocks.domain.messages.message import Message, MessageMetadata
from forging_blocks.domain.messages.query import Query


def _frozen_setattr(self: object, name: str, value: object) -> None:
    """Raise FrozenInstanceError for attribute assignment after init."""
    if name == "__init_finished__" or getattr(self, "__init_finished__", False):
        raise dataclasses.FrozenInstanceError(f"cannot assign to field {name!r}")
    object.__setattr__(self, name, value)


def _frozen_delattr(self: object, name: str) -> None:
    """Raise FrozenInstanceError for attribute deletion after init."""
    if name == "__init_finished__" or getattr(self, "__init_finished__", False):
        raise dataclasses.FrozenInstanceError(f"cannot delete field {name!r}")
    object.__delattr__(self, name)


def _payload_property(self: Any) -> dict[str, object]:
    """Return payload fields for a dynamically patched message property."""
    return self.get_payload_fields()


def _resolve_abstract_methods_to_remove(
    dc_cls: type[Any], abstract_methods: frozenset[str]
) -> set[str]:
    """Resolve which abstract methods to remove from the dataclass."""
    to_remove: set[str] = set()
    patched = cast(Any, dc_cls)
    if "_payload" in abstract_methods:
        patched._payload = property(_payload_property)
        to_remove.add("_payload")
    if "value" in abstract_methods:
        patched.value = property(_payload_property)
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

    return cast(classmethod[Any, Any, Any], classmethod(from_payload_fields))


def _ensure_message_base(cls: type[Any], base: type[Any]) -> type[Any]:
    """Create a message subclass when the decorated class has no message base."""
    if issubclass(cls, Message):
        return cls

    wrapped = type(cls.__name__, (cls, base), {})
    wrapped.__module__ = cls.__module__
    wrapped.__qualname__ = cls.__qualname__
    wrapped.__doc__ = cls.__doc__
    wrapped.__annotations__ = getattr(cls, "__annotations__", {})
    return wrapped


def _wrap_message_dataclass(cls: type[Any]) -> type[Any]:
    """Decorate and patch a concrete message class."""
    dc_cls: type[Any] = dataclass(frozen=False, eq=False)(cls)
    mutable_cls = cast(Any, dc_cls)
    mutable_cls.__setattr__ = _frozen_setattr
    mutable_cls.__delattr__ = _frozen_delattr

    def get_payload_fields(self: Any) -> dict[str, object]:
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
def message_dataclass(cls: type[Any]) -> type[Any]: ...


@overload
def message_dataclass(
    cls: None = None,
) -> Callable[[type[Any]], type[Any]]: ...


def _message_dataclass_for_base(base: type[Any], cls: type[Any]) -> type[Any]:
    """Decorate a class with a selected message role."""
    message_cls = _ensure_message_base(cls, base)
    return _wrap_message_dataclass(message_cls)


def message_dataclass(
    cls: type[Any] | None = None,
) -> type[Any] | Callable[[type[Any]], type[Any]]:
    """Decorate a class as a message dataclass.

    The decorator applies ``@dataclass(frozen=False)`` and then replaces
    ``__setattr__`` and ``__delattr__`` with custom implementations that raise
    ``FrozenInstanceError`` after ``__init__`` completes. It also patches
    ``get_payload_fields`` and ``from_payload_fields`` onto the class so that
    payload data is automatically derived from its fields.

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
    if cls is None:
        return lambda target: _message_dataclass_for_base(Message, target)
    return _message_dataclass_for_base(Message, cls)


def event_dataclass(cls: type[Any]) -> type[Any]:
    """Decorate a class as an event, adding the Event base when needed."""
    return _message_dataclass_for_base(Event, cls)


def command_dataclass(cls: type[Any]) -> type[Any]:
    """Decorate a class as a command, adding the Command base when needed."""
    return _message_dataclass_for_base(Command, cls)


def query_dataclass(cls: type[Any]) -> type[Any]:
    """Decorate a class as a query, adding the Query base when needed."""
    return _message_dataclass_for_base(Query, cls)
