"""A single error message intended for display to an end user."""

from dataclasses import dataclass

from forging_blocks.foundation.autofreeze import auto_freeze
from forging_blocks.foundation.autohash import auto_hash


@auto_hash
@auto_freeze
@dataclass
class ErrorMessageModel:
    """Carries the information needed to render one error to a user.

    Attributes:
        title: A short, human-readable summary of what went wrong.
        detail: An optional longer explanation with remediation guidance.
        field: An optional field or parameter name associated with the
            error (e.g. ``"username"``).
        code: An optional machine-readable error code for lookups.
        status_code: An optional HTTP-like status code (e.g. 400, 422)
            assigned by an ``ErrorStatusCodeMapper``.

    """

    title: str
    detail: str | None = None
    field: str | None = None
    code: str | None = None
    status_code: int | None = None
