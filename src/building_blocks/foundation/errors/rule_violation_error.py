from building_blocks.foundation.errors.base import CombinedErrors, Error


class RuleViolationError(Error):
    """
    Base class for rule violation errors, indicating that a specific rule has been
    violated.
    """


class CombinedRuleViolationErrors(CombinedErrors[RuleViolationError]):
    """
    Aggregates multiple rule violation errors for easier handling and reporting.
    """
