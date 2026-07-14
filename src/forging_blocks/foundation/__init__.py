"""ForgingBlocks foundation modules."""

from .autohash import auto_hash
from .context import AuthorizationContext, ServiceContext, TransactionContext
from .errors import (
    CantModifyImmutableAttributeError,
    CombinedErrors,
    CombinedRuleViolationErrors,
    CombinedValidationErrors,
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
from .messages import Command, Event, Message, Query
from .meta import FinalABCMeta, FinalMeta, runtime_final
from .permission import Permission
from .ports import (
    InboundPort,
    OutboundPort,
    Port,
)
from .result import Err, Ok, Result
from .rules import ValidationRule
from .specification import (
    AndSpecification,
    ComposableSpecification,
    ExpressionSpecification,
    NotSpecification,
    OrSpecification,
    Specification,
)
from .value_object import ValueObject

__all__ = [
    "auto_hash",
    "AndSpecification",
    "AuthorizationContext",
    "CombinedErrors",
    "CombinedRuleViolationErrors",
    "CombinedValidationErrors",
    "CantModifyImmutableAttributeError",
    "Command",
    "ComposableSpecification",
    "Err",
    "Error",
    "ErrorMessage",
    "ErrorMetadata",
    "Event",
    "ExpressionSpecification",
    "FieldErrors",
    "FieldReference",
    "FinalABCMeta",
    "FinalMeta",
    "Identified",
    "InboundPort",
    "Message",
    "NoneNotAllowedError",
    "NotSpecification",
    "Ok",
    "OrSpecification",
    "OutboundPort",
    "Permission",
    "Port",
    "Query",
    "Result",
    "ResultAccessError",
    "RuleViolationError",
    "runtime_final",
    "ServiceContext",
    "Specification",
    "TransactionContext",
    "ValidationError",
    "ValidationFieldErrors",
    "ValidationRule",
    "ValueObject",
]
