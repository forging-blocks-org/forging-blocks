"""Result type inspired by Rust's Result enum.

A disciplined alternative to raising exceptions — the Result type makes success
and failure explicit in your function signatures. Conceptually it is the same
idea as :class:`Either` in Scala or Haskell, specialised so that the *right*
side holds a success value and the *left* side holds an error.

Use :class:`Ok` to wrap a success value and :class:`Err` to wrap an error, then
compose operations with :meth:`map`, :meth:`flat_map`, and :meth:`map_error`
instead of writing try/except blocks.
"""

from collections.abc import Callable
from typing import Protocol, runtime_checkable


@runtime_checkable
class Result[ValueType, ErrorType](Protocol):
    """Protocol that defines the shared interface for :class:`Ok` and :class:`Err`."""

    @property
    def is_ok(self) -> bool:
        """Return ``True`` when this Result holds a success value (is :class:`Ok`)."""
        ...

    @property
    def is_err(self) -> bool:
        """Return ``True`` when this Result holds an error (is :class:`Err`)."""
        ...

    @property
    def value(self) -> ValueType:
        """Unwrap and return the success value.

        Raises :class:`ResultAccessError` if this Result is an :class:`Err`.
        """
        ...

    @property
    def error(self) -> ErrorType:
        """Unwrap and return the error.

        Raises :class:`ResultAccessError` if this Result is an :class:`Ok`.
        """
        ...

    def map[MappedValueType](
        self,
        fn: Callable[[ValueType], MappedValueType],
    ) -> "Result[MappedValueType, ErrorType]":
        """Transform the success value with ``fn``, passing errors through unchanged.

        This is the Functor map — ``fmap`` in Haskell, ``.map`` on Scala's
        ``Option`` / ``Either``.
        """
        ...

    def map_error[MappedErrorType](
        self,
        fn: Callable[[ErrorType], MappedErrorType],
    ) -> "Result[ValueType, MappedErrorType]":
        """Transform the error with ``fn``, passing success values through unchanged."""
        ...

    def flat_map[MappedValueType](
        self,
        fn: Callable[[ValueType], "Result[MappedValueType, ErrorType]"],
    ) -> "Result[MappedValueType, ErrorType]":
        """Chain a fallible operation that itself returns a Result.

        If Ok, call ``fn`` with the value; if Err, short-circuit unchanged.
        This is Monad's bind — ``>>=`` in Haskell, ``flatMap`` in Scala.
        """
        ...

    def get_value_or(self, default: ValueType) -> ValueType:
        """Return the wrapped success value if Ok, otherwise return the provided default.

        Args:
            default: The value to return if this result is an error.

        Returns:
            The unwrapped success value if Ok; otherwise, `default`.
        """
        ...

    def get_value_or_else(
        self,
        fn: Callable[[ErrorType], ValueType],
    ) -> ValueType:
        """Return the wrapped success value if Ok, otherwise compute one from the error.

        Applies `fn` to the wrapped error (if present) to compute and return a recovery value.
        Useful for transforming or logging errors before fallback.

        Args:
            fn: A callable that accepts the error and returns a recovery value of the same type
                as the success case.

        Returns:
            The unwrapped success value if Ok; otherwise, the result of `fn(error)`.
        """
        ...
