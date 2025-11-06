"""Module defining errors related to rule violations within the system.

Defines error classes for handling rule violation scenarios.
"""

from building_blocks.foundation.errors.base import CombinedErrors, Error


class RuleViolationError(Error):
    """Base class for rule violation errors."""

    ...


class CombinedRuleViolationErrors(CombinedErrors[RuleViolationError]):
    """Aggregates multiple rule violation errors for easier handling and reporting."""

    ...
