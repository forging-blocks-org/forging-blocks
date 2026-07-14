"""Error raised when a field value cannot be converted to a hashable equivalent.

Used by :class:`HashableConverter` when a value is neither natively hashable
nor one of the supported convertible types (``list``, ``dict``).
"""

from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata
from forging_blocks.foundation.errors.error import Error


class NonHashableValueError(Error[dict[str, object]]):
    """Raised when a value cannot be made hashable during ``__hash__`` computation.

    ``@auto_hash`` converts ``list`` → ``tuple`` and ``dict`` →
    ``frozenset`` of ``(key, value)`` pairs automatically. Values of
    other mutable types (e.g. ``set``, custom objects without ``__hash__``)
    trigger this error.
    """

    def __init__(self, type_name: str) -> None:
        """Initialise the error with the name of the type that failed conversion.

        Args:
            type_name: The ``type(value).__name__`` of the offending value.
        """
        message = ErrorMessage(
            f"Cannot convert {type_name!r} to hashable. "
            f"Use tuple, frozenset, or immutable types "
            f"in fields hashed by @auto_hash."
        )
        metadata = ErrorMetadata[dict[str, object]]({"type_name": type_name})
        super().__init__(message, metadata)
