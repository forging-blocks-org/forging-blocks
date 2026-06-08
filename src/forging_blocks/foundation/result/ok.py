"""Ok variant of the Result type — represents a successful computation.

Wrap a value with ``Ok(value)`` and chain operations without fear of
:class:`Err` short-circuits leaking into your logic.  This is the *right*
side of the Either monad (the ``Right`` in Haskell / Scala).
"""

from collections.abc import Callable

from forging_blocks.foundation.errors import ResultAccessError

from .result import Result


class Ok[ValueType, ErrorType]:
    """Represents a successful result, holding a value of type ``ValueType``."""

    __match_args__ = ("_value",)

    def __init__(self, value: ValueType) -> None:
        """Wrap ``value`` as a successful :class:`Result`."""
        self._value = value

    def __repr__(self) -> str:
        """Return a debug-friendly repr like ``Ok(value)``."""
        return f"Ok({self._value!r})"

    def __str__(self) -> str:
        """Return a user-friendly string like ``Ok(value)``."""
        return f"Ok({self._value})"

    def __eq__(self, other: object) -> bool:
        """Two Oks are equal when their wrapped values are equal."""
        return isinstance(other, Ok) and self._value == other._value

    def __hash__(self) -> int:
        """Hash based on the wrapped value."""
        return hash(self._value)

    @property
    def is_ok(self) -> bool:
        """Always ``True`` — this variant holds a success value."""
        return True

    @property
    def is_err(self) -> bool:
        """Always ``False`` — this variant does not hold an error."""
        return False

    @property
    def value(self) -> ValueType:
        """The wrapped success value."""
        return self._value

    @property
    def error(self) -> ErrorType:
        """Raises :class:`ResultAccessError` — there is no error to access."""
        raise ResultAccessError.cannot_access_error()

    def map[MappedValueType](
        self,
        fn: Callable[[ValueType], MappedValueType],
    ) -> Result[MappedValueType, ErrorType]:
        """Apply ``fn`` to the wrapped value and wrap the result in a new Ok.

        This is the Functor map — ``fmap`` in Haskell, ``.map`` on Scala's
        ``Option`` / ``Either``.
        """
        return Ok(fn(self._value))

    def map_error[MappedErrorType](
        self,
        fn: Callable[[ErrorType], MappedErrorType],
    ) -> Result[ValueType, MappedErrorType]:
        """Pass through unchanged — there is no error to transform."""
        return Ok(self._value)

    def flat_map[MappedValueType](
        self,
        fn: Callable[[ValueType], Result[MappedValueType, ErrorType]],
    ) -> Result[MappedValueType, ErrorType]:
        """Apply ``fn`` to the wrapped value and return its Result directly.

        Unlike :meth:`map`, ``fn`` itself returns a Result, so you can chain
        multiple fallible operations without nesting ``Ok(Ok(...))``.
        """
        return fn(self._value)

    def get_value_or(self, default: ValueType) -> ValueType:
        """Return the wrapped value, ignoring ``default``.

        Args:
            default: Ignored — this Result is a success.

        Returns:
            The unwrapped success value.
        """
        return self._value

    def get_value_or_else(
        self,
        fn: Callable[[ErrorType], ValueType],
    ) -> ValueType:
        """Return the wrapped value, ignoring ``fn``.

        Args:
            fn: Ignored — this Result is a success.

        Returns:
            The unwrapped success value.
        """
        return self._value
