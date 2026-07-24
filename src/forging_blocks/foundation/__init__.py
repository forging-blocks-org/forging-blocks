"""ForgingBlocks foundation modules."""

from .autoeq import auto_eq
from .autohash import auto_hash
from .errors import (
    ArchitectureError,
    CantModifyImmutableAttributeError,
    CombinedErrors,
    CombinedRuleViolationErrors,
    CombinedValidationErrors,
    ConfigurationError,
    Error,
    ErrorMessage,
    ErrorMetadata,
    FieldErrors,
    FieldReference,
    NoneNotAllowedError,
    ResultAccessError,
    RuleViolationError,
    ValidationError,
    ValidationFieldErrors,
)
from .identified import Identified
from .mapper import Mapper
from .meta import FinalABCMeta, FinalMeta, runtime_final
from .permission import Permission
from .ports import (
    InboundPort,
    OutboundPort,
    Port,
)
from .result import Err, Ok, Result
from .rules import ValidationRule

__all__ = [
    "auto_eq",
    "auto_hash",
    "ArchitectureError",
    "ConfigurationError",
    "CombinedErrors",
    "CombinedRuleViolationErrors",
    "CombinedValidationErrors",
    "CantModifyImmutableAttributeError",
    "Err",
    "Error",
    "ErrorMessage",
    "ErrorMetadata",
    "FieldErrors",
    "FieldReference",
    "FinalABCMeta",
    "FinalMeta",
    "Identified",
    "InboundPort",
    "Mapper",
    "NoneNotAllowedError",
    "Ok",
    "OutboundPort",
    "Permission",
    "Port",
    "Result",
    "ResultAccessError",
    "RuleViolationError",
    "runtime_final",
    "ValidationError",
    "ValidationFieldErrors",
    "ValidationRule",
]
