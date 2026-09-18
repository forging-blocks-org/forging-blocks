"""Convert arbitrary field values into hashable equivalents.

Ensures that field values such as ``list`` and ``dict`` can
participate in ``__hash__`` computations by converting them to
immutable types.
"""

from collections.abc import Hashable
from typing import cast

from forging_blocks.foundation.errors.non_hashable_value_error import (
    NonHashableValueError,
)


class HashableConverter:
    """Recursively converts non-hashable values to hashable equivalents.

    - ``list`` → ``tuple`` (recursively)
    - ``set`` → ``frozenset``
    - ``dict``  → ``frozenset`` of ``(key, hashable_value)`` pairs (recursively)
    - Already-hashable values (``str``, ``int``, ``None``, ``tuple``,
      ``frozenset``, etc.) are returned unchanged.
    - Everything else raises `NonHashableValueError`.

    Example:
        ```python
        from forging_blocks.foundation.autohash.helpers.hashable_converter import HashableConverter

        result = HashableConverter.convert([1, 2, 3])
        assert result == (1, 2, 3)
        assert hash(result) is not None
        ```
    """

    @classmethod
    def _convert_sequence(
        cls,
        value: tuple[object, ...] | list[object],
        field_name: str | None,
    ) -> tuple[Hashable, ...]:
        return tuple(cls.convert(v, field_name=field_name) for v in value)

    @classmethod
    def _convert_set(
        cls,
        value: frozenset[object] | set[object],
        field_name: str | None,
    ) -> frozenset[Hashable]:
        return frozenset(cls.convert(v, field_name=field_name) for v in value)

    @classmethod
    def _convert_dict(
        cls,
        value: dict[object, object],
        field_name: str | None,
    ) -> frozenset[tuple[object, Hashable]]:
        return frozenset((k, cls.convert(v, field_name=field_name)) for k, v in value.items())

    @classmethod
    def convert(cls, value: object, field_name: str | None = None) -> Hashable:
        """Convert *value* to a hashable equivalent.

        Args:
            value: Any value that may appear as a field on a decorated class.
            field_name: Optional field name where the value was encountered.

        Returns:
            A hashable representation of *value*.

        Raises:
            NonHashableValueError: When *value* cannot be made hashable (e.g. a
                custom non-hashable object).

        """
        if isinstance(value, (tuple, list)):
            return cls._convert_sequence(
                cast("tuple[object, ...] | list[object]", value), field_name
            )
        if isinstance(value, (frozenset, set)):
            return cls._convert_set(cast("frozenset[object] | set[object]", value), field_name)
        if isinstance(value, dict):
            return cls._convert_dict(cast("dict[object, object]", value), field_name)
        if isinstance(value, Hashable):
            return value
        raise NonHashableValueError(type(value).__name__, field_name=field_name)
