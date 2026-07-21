"""Tests for the check_methods structural subtype utility."""

import pytest

from forging_blocks.foundation.ports import check_methods


@pytest.mark.unit
class TestCheckMethods:
    def test_returns_true_when_all_methods_present(self) -> None:
        """Returns True when the class has all requested callable attributes."""

        class HasBoth:
            def foo(self) -> None: ...

            def bar(self) -> None: ...

        assert check_methods(HasBoth, "foo", "bar")

    def test_returns_false_when_method_missing(self) -> None:
        """Returns False when a requested method is absent."""

        class HasOne:
            def foo(self) -> None: ...

        assert not check_methods(HasOne, "foo", "bar")

    def test_returns_false_when_all_methods_missing(self) -> None:
        """Returns False when no requested methods exist."""

        class HasNone: ...

        assert not check_methods(HasNone, "foo")

    def test_returns_false_for_non_callable_attribute(self) -> None:
        """Returns False when the attribute exists but is not callable."""

        class HasAttr:
            foo = 42

        assert not check_methods(HasAttr, "foo")

    def test_no_method_names_returns_true(self) -> None:
        """Vacuous truth: all() over empty iterable is True."""
        assert check_methods(int)
