"""Convert arbitrary field values into hashable equivalents.

Used by the auto_hash decorator to ensure that field values such as
``list`` and ``dict`` can participate in ``__hash__`` computations.
"""

from collections.abc import Hashable
from typing import cast

from forging_blocks.foundation.errors.non_hashable_value_error import (
    NonHashableValueError,
)


class HashableConverter:
    """Recursively converts non-hashable values to hashable equivalents.

    - ``list`` → ``tuple`` (recursively)
    - ``dict``  → ``tuple(sorted(...))`` (recursively on values)
    - Already-hashable values (``str``, ``int``, ``None``, ``tuple``,
      ``frozenset``, etc.) are returned unchanged.
    - Everything else raises :class:`NonHashableValueError`.
    """

    @classmethod
    def convert(cls, value: object) -> Hashable:
        """Convert *value* to a hashable equivalent.

        Args:
            value: Any value that may appear as a field on a decorated class.

        Returns:
            A hashable representation of *value*.

        Raises:
            NonHashableValueError: When *value* cannot be made hashable (e.g. a mutable
                set or a custom non-hashable object).
        """
        if isinstance(value, Hashable):
            return value
        if isinstance(value, list):
            return cls._convert_list(cast("list[object]", value))
        if isinstance(value, dict):
            return cls._convert_dict(cast("dict[object, object]", value))
        raise NonHashableValueError(type(value).__name__)

    @classmethod
    def _convert_list[T](cls, items: list[T]) -> tuple[Hashable, ...]:
        return tuple(cls.convert(v) for v in items)

    @classmethod
    def _convert_dict[K, V](cls, mapping: dict[K, V]) -> tuple[tuple[K, Hashable], ...]:
        return tuple(sorted((k, cls.convert(v)) for k, v in mapping.items()))
