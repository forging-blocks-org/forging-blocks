"""Specification pattern for domain-level query predicates."""

from forging_blocks.foundation.specification import (
    AndSpecification,
    ExpressionSpecification,
    NotSpecification,
    OrSpecification,
    Specification,
)

__all__ = [
    "Specification",
    "ExpressionSpecification",
    "AndSpecification",
    "OrSpecification",
    "NotSpecification",
]
