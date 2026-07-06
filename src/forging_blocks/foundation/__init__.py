"""ForgingBlocks foundation modules."""

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
from .isolation_level import IsolationLevel
from .mapper import Mapper
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
    "AndSpecification",
    "AuthorizationContext",
    "CantModifyImmutableAttributeError",
    "CombinedErrors",
    "CombinedRuleViolationErrors",
    "CombinedValidationErrors",
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
    "IsolationLevel",
    "Mapper",
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
