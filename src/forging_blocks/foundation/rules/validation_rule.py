"""Abstract base class for a synchronous validation rule."""

from abc import ABC, abstractmethod
from typing import Any

from forging_blocks.foundation.errors.rule_violation_error import RuleViolationError


class ValidationRule(ABC):
    """Abstract base class for a synchronous validation rule."""

    @abstractmethod
    def validate(self, value: Any) -> list[RuleViolationError]:
        """Validate *value* and return any errors found."""
