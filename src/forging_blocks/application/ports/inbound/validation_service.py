"""Inbound port for domain command and query validation."""

from abc import ABC, abstractmethod
from typing import Any

from forging_blocks.foundation.errors.rule_violation_error import RuleViolationError


class ValidationService(ABC):
    """Abstract validation service for commands and queries."""

    @abstractmethod
    async def validate_command(self, command: Any) -> list[RuleViolationError]:
        """Validate a domain command."""
        ...

    @abstractmethod
    async def validate_query(self, query: Any) -> list[RuleViolationError]:
        """Validate a domain query."""
        ...
