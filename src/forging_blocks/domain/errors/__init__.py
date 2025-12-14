"""ForgingBlocks for domain errors."""

from .draft_entity_is_not_hashable_error import DraftEntityIsNotHashableError
from .entity_id_none_error import EntityIdNoneError

__all__ = [
    "DraftEntityIsNotHashableError",
    "EntityIdNoneError",
]
