"""Domain value objects module.

Re-exports the ValueObject base class from the foundation layer
so that domain code can import from a natural location.
"""

from forging_blocks.foundation.value_object import ValueObject  # noqa: F401

__all__ = [
    "ValueObject",
]
