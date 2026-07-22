"""Configuration error for misconfigured adapters.

Defines ``ConfigurationError``, raised when an infrastructure adapter is
used with invalid configuration (e.g., disallowed URL schemes, invalid
paths, or misconfigured parameters).
"""

from collections.abc import Mapping

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error


class ConfigurationError(Error[Mapping[str, object]]):
    """Raised when an infrastructure adapter receives invalid configuration.

    This error signals operational misconfiguration at runtime — for example,
    a URL with a disallowed scheme being passed to an HTTP client, or an
    invalid filesystem path being used by a file adapter.
    """

    def __init__(self, message: str) -> None:
        """Initialise with a descriptive configuration-violation message.

        Args:
            message: Human-readable description of the misconfiguration,
                including the offending value and the acceptable range.

        """
        super().__init__(ErrorMessage(message))
