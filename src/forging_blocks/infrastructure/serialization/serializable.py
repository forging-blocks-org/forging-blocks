"""Serializable protocol for messages and domain events.

Provides a ``Serializable`` protocol that allows types to declare they can be
converted to and from plain dictionaries. This enables generic serialization
infrastructure (JSON, database adapters, event stores) to work with any type
that satisfies the protocol structurally — no base class required.
"""

from typing import Protocol, Self


class Serializable[T](Protocol):
    """Protocol for serializable objects.

    Types satisfying this protocol can be:
      - serialised to a dictionary via ``to_dict()``.
      - deserialised from a dictionary via ``from_dict()``.

    The protocol is structural — any class that defines ``to_dict`` and
    ``from_dict`` with matching signatures satisfies it automatically,
    without explicit registration or inheritance.
    """

    def to_dict(self) -> dict[str, T]:
        """Return a dictionary representation of this instance."""
        ...

    @classmethod
    def from_dict(cls, data: dict[str, T]) -> Self:
        """Create an instance from a dictionary representation.

        Args:
            data: Dictionary containing the serialised representation.

        Returns:
            A new instance reconstituted from *data*.

        """
        ...
