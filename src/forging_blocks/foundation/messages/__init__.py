"""Foundation messages package."""

from .command import Command
from .decorators import (
    command_dataclass,
    event_dataclass,
    message_dataclass,
    query_dataclass,
)
from .event import Event
from .message import Message, MessageMetadata
from .query import Query

__all__ = [
    "Message",
    "MessageMetadata",
    "Event",
    "Command",
    "Query",
    "message_dataclass",
    "event_dataclass",
    "command_dataclass",
    "query_dataclass",
]
