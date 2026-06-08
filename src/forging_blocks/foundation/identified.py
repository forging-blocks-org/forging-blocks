"""Protocol for domain objects that carry an identifier."""

from typing import Protocol


class Identified[IdentityType](Protocol):
    """Protocol for objects that expose an ``id`` property.

    Satisfied by any object whose ``id`` returns the object's identity,
    which may be ``None`` for draft/unpersisted instances.
    """

    @property
    def id(self) -> IdentityType | None: ...
