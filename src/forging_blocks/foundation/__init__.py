"""ForgingBlocks foundation modules."""

from .autoeq import auto_eq
from .autofreeze.auto_freeze import auto_freeze
from .autohash import auto_hash
from .debuggable import Debuggable
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
    RuleViolatedError,
    RuleViolationError,
    ValidationError,
    ValidationFailedError,
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
    "auto_freeze",
    "auto_hash",
    "ArchitectureError",
    "ConfigurationError",
    "Debuggable",
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
    "RuleViolatedError",
    "RuleViolationError",
    "runtime_final",
    "ValidationError",
    "ValidationFailedError",
    "ValidationFieldErrors",
    "ValidationRule",
]
