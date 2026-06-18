"""Specification pattern for domain-level query predicates."""

from .composite import AndSpecification, NotSpecification, OrSpecification
from .specification import ExpressionSpecification, Specification

__all__ = [
    "Specification",
    "ExpressionSpecification",
    "AndSpecification",
    "OrSpecification",
    "NotSpecification",
]
