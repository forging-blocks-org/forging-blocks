"""Domain validation error module.

Auto-generated minimal module docstring.
"""

from typing import Dict, Optional

from .domain_error import DomainError


class DomainValidationError(DomainError):
    """Raised when one or more fields fail domain validation.

    Contains a mapping of field_name -> error_message(s).
    """

    def __init__(
        self,
        message: str,
        context: Optional[Dict] = None,
    ) -> None:
        if context is not None and not isinstance(context, dict):
            raise TypeError(
                "Context must be a dictionary mapping field names to error messages."
            )
        super().__init__(message)
        self.message = message
        self.context = context or {}

    def __str__(self) -> str:
        if self.context:
            return f"{self.message} | Context: {self.context}"
        return self.message
