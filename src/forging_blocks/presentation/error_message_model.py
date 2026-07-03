"""A single error message intended for display to an end user."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorMessageModel:
    """Carries the information needed to render one error to a user.

    Attributes:
        title: A short, human-readable summary of what went wrong.
        detail: An optional longer explanation with remediation guidance.
        field: An optional field or parameter name associated with the
            error (e.g. ``"username"``).
        code: An optional machine-readable error code for lookups.
    """

    title: str
    detail: str | None = None
    field: str | None = None
    code: str | None = None
