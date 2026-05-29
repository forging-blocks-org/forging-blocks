"""Protocol for domain objects that carry an identifier."""

from typing import Protocol, TypeVar

TId_co = TypeVar("TId_co", covariant=True)


class Identified(Protocol[TId_co]):
    """Protocol for objects that expose an ``id`` property.

    Satisfied by any object whose ``id`` returns the object's identity,
    which may be ``None`` for draft/unpersisted instances.
    """

    @property
    def id(self) -> TId_co | None:
        ...
