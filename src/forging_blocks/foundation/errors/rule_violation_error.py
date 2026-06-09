"""Module defining errors related to rule violations within the system.

Defines error classes for handling rule violation scenarios.
"""

from forging_blocks.foundation.errors.combined_errors import CombinedErrors
from forging_blocks.foundation.errors.error import Error


class RuleViolationError(Error):
    """Base class for rule violation errors."""

    ...


class CombinedRuleViolationErrors(CombinedErrors[RuleViolationError]):
    """Aggregates multiple rule violation errors for easier handling and reporting."""

    ...
