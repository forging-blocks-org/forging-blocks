"""Err variant of the Result type — represents a failed computation.

Wrap an error with ``Err(error)`` to short-circuit chains of ``map`` and
``flat_map`` calls.  This is the *left* side of the Either monad (the
``Left`` in Haskell / Scala), carrying the reason the computation could not
proceed.
"""

from collections.abc import Callable
from typing import cast

from forging_blocks.foundation.errors import ResultAccessError

from .result import Result


class Err[ValueType, ErrorType](Result[ValueType, ErrorType]):
    """Represents a failed result, holding an error of type ``ErrorType``."""

    __match_args__ = ("_error",)

    def __init__(self, error: ErrorType) -> None:
        """Wrap ``error`` as a failed ``Result``."""
        self._error = error

    def __repr__(self) -> str:
        """Return a debug-friendly repr like ``Err(error)``."""
        return f"Err({self._error!r})"

    def __str__(self) -> str:
        """Return a user-friendly string like ``Err(error)``."""
        return f"Err({self._error})"

    def __eq__(self, other: object) -> bool:
        """Two Errs are equal when their wrapped errors are equal."""
        if not isinstance(other, Err):
            return False
        return self._error == cast(Err[ValueType, ErrorType], other)._error

    def __hash__(self) -> int:
        """Hash based on the wrapped error."""
        return hash(self._error)

    @property
    def is_ok(self) -> bool:
        """Always ``False`` — this variant does not hold a success value."""
        return False

    @property
    def is_err(self) -> bool:
        """Always ``True`` — this variant holds an error."""
        return True

    @property
    def value(self) -> ValueType:
        """Raises `ResultAccessError` — there is no success value to access."""
        raise ResultAccessError.cannot_access_value()

    @property
    def error(self) -> ErrorType:
        """The wrapped error."""
        return self._error

    def map[MappedValueType](
        self,
        fn: Callable[[ValueType], MappedValueType],
    ) -> Result[MappedValueType, ErrorType]:
        """Pass through unchanged — there is no value to transform.

        This is the Functor map on the error path — the error propagates
        unchanged while ``fn`` is silently ignored.
        """
        return Err(self._error)

    def map_error[MappedErrorType](
        self,
        fn: Callable[[ErrorType], MappedErrorType],
    ) -> Result[ValueType, MappedErrorType]:
        """Apply ``fn`` to the wrapped error and wrap the result in a new Err."""
        return Err(fn(self._error))

    def flat_map[MappedValueType](
        self,
        fn: Callable[[ValueType], Result[MappedValueType, ErrorType]],
    ) -> Result[MappedValueType, ErrorType]:
        """Pass through unchanged — short-circuit the chain."""
        return Err(self._error)

    def get_value_or(self, default: ValueType) -> ValueType:
        """Return ``default`` — there is no success value.

        Args:
            default: The value to return when this result is an error.

        Returns:
            ``default``, since there is no success value to unwrap.
        """
        return default

    def get_value_or_else(
        self,
        fn: Callable[[ErrorType], ValueType],
    ) -> ValueType:
        """Call ``fn`` with the wrapped error to compute a fallback.

        Args:
            fn: A callable that accepts the error and returns a recovery value
                of the same type as the success case.

        Returns:
            The result of ``fn(error)``.
        """
        return fn(self._error)
