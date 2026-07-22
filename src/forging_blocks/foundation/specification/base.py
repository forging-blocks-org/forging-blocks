"""Core specification abstraction.

Provides the foundational specification contract without any composition
implementation details or dependencies.
"""

from abc import ABC, abstractmethod


class Specification[T](ABC):
    """Abstract predicate over a candidate object.

    Specifications encapsulate business rules that can be evaluated
    against an object of type T.

    This is the minimal contract: only is_satisfied_by().
    Composition (and_, or_, not_) is added by ComposableSpecification.
    """

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Determine whether the candidate satisfies this specification.

        Args:
            candidate: The object to evaluate.

        Returns:
            True if the candidate satisfies this specification, False otherwise.
        """
