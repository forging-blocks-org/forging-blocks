"""ForgingBlocks for domain-specific modules."""

from .aggregate_root import AggregateRoot, AggregateVersion
from .entity import Entity
from .errors import DraftEntityIsNotHashableError, EntityIdNoneError
from .messages import Command, Event, Message, MessageMetadata, Query
from .value_object import ValueObject

__all__ = [
    "DraftEntityIsNotHashableError",
    "Command",
    "EntityIdNoneError",
    "Entity",
    "Event",
    "Message",
    "MessageMetadata",
    "Query",
    "AggregateRoot",
    "AggregateVersion",
    "ValueObject",
]
