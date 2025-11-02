"""Domain rule violation error module.

Auto-generated minimal module docstring.
"""

from typing import Dict, Optional

from building_blocks.domain.errors.domain_error import DomainError


class DomainRuleViolationError(DomainError):
    """Base class for domain rule/invariant violations."""

    def __init__(
        self, message: str, rule: Optional[str] = None, context: Optional[Dict] = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.rule = rule
        self.context = context or {}

    def __str__(self) -> str:
        base = self.message if self.message else self.__class__.__name__
        if self.rule:
            base = f"[{self.rule}] {base}"
        if self.context:
            base = f"{base} | Context: {self.context}"
        return base
