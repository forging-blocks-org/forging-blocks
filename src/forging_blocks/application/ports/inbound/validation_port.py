"""Inbound port for domain command and query validation.

Responsibilities:
    - Validate commands and queries against business rules.
    - Return structured validation errors.

Non-Responsibilities:
    - Execute commands or queries.
    - Implement business logic directly.
"""

from abc import abstractmethod
from typing import Any

from forging_blocks.foundation.errors.rule_violation_error import RuleViolationError
from forging_blocks.foundation.ports import InboundPort


class ValidationPort(InboundPort):
    """Inbound port for domain command and query validation.

    Responsibilities:
        - Inspect command and query payloads for rule violations.
        - Return a list of ``RuleViolationError`` instances.

    Non-Responsibilities:
        - Enforce authorization (handled by ``AuthorizationPort``).
        - Modify command or query state.
    """

    @abstractmethod
    async def validate_command(self, command: Any) -> list[RuleViolationError]:
        """Validate a domain command."""
        ...

    @abstractmethod
    async def validate_query(self, query: Any) -> list[RuleViolationError]:
        """Validate a domain query."""
        ...
