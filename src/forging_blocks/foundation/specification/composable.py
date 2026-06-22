"""Composable specification abstraction.

Adds fluent logical composition to the core Specification contract.
Operators are defined ONCE here and delegate to logical classes.
Subclasses inherit them automatically—no reimplementation needed.

The logical operator classes (``AndSpecification``, ``OrSpecification``,
``NotSpecification``) themselves inherit from ``ComposableSpecification`` so
that the result of a composition is itself composable. Because the operators
depend on this class for their base while this class delegates back to the
operators, importing the operators at module level would create a circular
import. The operator imports are therefore deferred into the methods that
construct them, keeping the static import graph acyclic:
``composable`` -> ``base`` and ``logical_operators`` -> ``composable`` -> ``base``.
"""

from .base import Specification


class ComposableSpecification[T](Specification[T]):
    """Specification supporting fluent logical composition.

    Provides a single definition of composition operators:
    - and_() / __and__()  → delegates to AndSpecification
    - or_()  / __or__()   → delegates to OrSpecification
    - not_() / __invert__() → delegates to NotSpecification

    Subclasses inherit these automatically. Do NOT reimplement in subclasses.
    """

    def and_(self, other: Specification[T]) -> Specification[T]:
        """Combine two specifications using logical conjunction.

        Args:
            other: The specification to AND with this one.

        Returns:
            A new AndSpecification combining both.
        """
        from .logical_operators import AndSpecification

        return AndSpecification(self, other)

    def or_(self, other: Specification[T]) -> Specification[T]:
        """Combine two specifications using logical disjunction.

        Args:
            other: The specification to OR with this one.

        Returns:
            A new OrSpecification combining both.
        """
        from .logical_operators import OrSpecification

        return OrSpecification(self, other)

    def not_(self) -> Specification[T]:
        """Create the logical negation of this specification.

        Returns:
            A new NotSpecification wrapping this one.
        """
        from .logical_operators import NotSpecification

        return NotSpecification(self)

    def __and__(self, other: Specification[T]) -> Specification[T]:
        """Operator overload for & (bitwise AND).

        Args:
            other: The specification to AND with this one.

        Returns:
            A new AndSpecification combining both.
        """
        return self.and_(other)

    def __or__(self, other: Specification[T]) -> Specification[T]:
        """Operator overload for | (bitwise OR).

        Args:
            other: The specification to OR with this one.

        Returns:
            A new OrSpecification combining both.
        """
        return self.or_(other)

    def __invert__(self) -> Specification[T]:
        """Operator overload for ~ (bitwise NOT).

        Returns:
            A new NotSpecification wrapping this one.
        """
        return self.not_()
