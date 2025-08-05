from building_blocks.abstractions.errors.base import Error


class RuleViolationError(Error):
    """
    Base class for rule/invariant violations.
    ...
    """

    def __str__(self) -> str:
        return f"Rule Violation: {super().__str__()}"
