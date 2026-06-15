# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
"""Tests for the auto_freeze decorator."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from forging_blocks.foundation.autofreeze.auto_freeze import (
    _AutoFreezeDecorator,
    auto_freeze,
)


# ---------------------------------------------------------------------------
# Test helpers — lightweight classes that implement SupportsAutoFreeze
# protocol via MagicMock so every call is observable.
# ---------------------------------------------------------------------------


def _make_protocol_class(
    *,
    with_freeze_attrs: bool = True,
) -> type:
    """Create a class that implements SupportsAutoFreeze with mock tracking."""
    freeze_instance_mock = MagicMock()
    namespace: dict[str, Any] = {
        "freeze_instance": freeze_instance_mock,
    }
    if with_freeze_attrs:
        freeze_attrs_mock = MagicMock()
        namespace["freeze_attributes"] = freeze_attrs_mock
    else:
        freeze_attrs_mock = None
    cls = type("ProtocolClass", (), namespace)
    # Store mocks as class attributes
    cls._freeze_instance_mock = freeze_instance_mock  # type: ignore[attr-defined]
    if with_freeze_attrs:
        cls._freeze_attrs_mock = freeze_attrs_mock  # type: ignore[attr-defined]
    return cls


def _make_minimal_class() -> type:
    """Create a class with only the required protocol methods."""
    return _make_protocol_class(with_freeze_attrs=False)


# ---------------------------------------------------------------------------
# Tests for _validate_protocol
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestValidateProtocol:
    """Tests for the internal _validate_protocol function."""

    def test_when_all_required_methods_present_then_returns_none(self) -> None:
        cls = _make_minimal_class()
        result = _AutoFreezeDecorator._validate_protocol(cls)
        assert result is None

    def test_when_missing_freeze_instance_then_raises_typeerror(self) -> None:
        class Incomplete:
            def freeze_attributes(self, attrs: list[str]) -> None:
                pass

        with pytest.raises(TypeError, match="does not implement SupportsAutoFreeze"):
            _AutoFreezeDecorator._validate_protocol(Incomplete)

    def test_when_missing_multiple_methods_then_lists_all_missing(self) -> None:
        class Empty:
            pass

        with pytest.raises(TypeError) as exc_info:
            _AutoFreezeDecorator._validate_protocol(Empty)

        message = str(exc_info.value)
        assert "freeze_instance" in message

    def test_when_class_has_extra_methods_then_still_validates(self) -> None:
        cls = _make_protocol_class()
        result = _AutoFreezeDecorator._validate_protocol(cls)
        assert result is None


# ---------------------------------------------------------------------------
# Tests for the auto_freeze decorator
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAutoFreezeDecorator:
    """Tests for the auto_freeze decorator public API."""

    # -- Usage modes --------------------------------------------------------

    def test_when_used_without_parentheses_then_decorates_class(self) -> None:
        cls = _make_minimal_class()
        decorated = auto_freeze(cls)
        assert decorated is cls

    def test_when_used_with_empty_parentheses_then_returns_decorator(self) -> None:
        cls = _make_minimal_class()
        decorator = auto_freeze()
        decorated = decorator(cls)
        assert decorated is cls

    def test_when_used_with_attrs_then_returns_decorator(self) -> None:
        cls = _make_minimal_class()
        decorator = auto_freeze(attrs=["_id"])
        decorated = decorator(cls)
        assert decorated is cls

    def test_when_class_already_decorated_then_returns_same_class(self) -> None:
        cls = _make_minimal_class()
        first = auto_freeze(cls)
        second = auto_freeze(first)
        assert first is second

    # -- Protocol validation ------------------------------------------------

    def test_when_class_missing_freeze_instance_then_raises_typeerror(self) -> None:
        class Incomplete:
            def freeze_attributes(self, attrs: list[str]) -> None:
                pass

        with pytest.raises(TypeError, match="does not implement SupportsAutoFreeze"):
            auto_freeze(Incomplete)

    # -- Freeze behavior ----------------------------------------------------

    def test_when_attrs_is_none_then_calls_freeze_instance(self) -> None:
        cls = _make_minimal_class()
        decorated = auto_freeze(cls)
        decorated()  # instance not used
        cls._freeze_instance_mock.assert_called_once()

    def test_when_attrs_provided_then_calls_freeze_attributes(self) -> None:
        cls = _make_protocol_class()
        decorated = auto_freeze(attrs=["_id"])(cls)
        decorated()
        cls._freeze_attrs_mock.assert_called_once_with(["_id"])
        cls._freeze_instance_mock.assert_not_called()

    def test_when_init_raises_then_freeze_not_called(self) -> None:
        cls = _make_minimal_class()

        def failing_init(self: Any, value: int) -> None:
            raise ValueError("fail")

        cls.__init__ = failing_init  # type: ignore[method-assign]

        decorated = auto_freeze(cls)

        with pytest.raises(ValueError, match="fail"):
            decorated(42)

        cls._freeze_instance_mock.assert_not_called()

    # -- Selective freezing -------------------------------------------------

    def test_when_attrs_is_list_then_passes_same_list_to_freeze_attributes(
        self,
    ) -> None:
        cls = _make_protocol_class()
        attrs = ["_id", "_created_at"]
        decorated = auto_freeze(attrs=attrs)(cls)
        decorated()
        cls._freeze_attrs_mock.assert_called_once_with(attrs)

    def test_when_attrs_is_empty_list_then_passes_empty_list(self) -> None:
        cls = _make_protocol_class()
        decorated = auto_freeze(attrs=[])(cls)
        decorated()
        cls._freeze_attrs_mock.assert_called_once_with([])

    # -- Inheritance --------------------------------------------------------

    def test_when_subclass_decorated_then_own_freeze_called(self) -> None:
        base = _make_minimal_class()
        child = _make_minimal_class()

        class ChildClass(child):  # type: ignore[misc]
            pass

        decorated = auto_freeze(ChildClass)
        decorated()
        child._freeze_instance_mock.assert_called_once()
        base._freeze_instance_mock.assert_not_called()

    # -- Edge cases ---------------------------------------------------------

    def test_when_class_has_slots_then_works_correctly(self) -> None:
        class Slotted:
            __slots__ = ("_value", "_Slotted__frozen")

            def __init__(self, value: int) -> None:
                self._value = value

            def freeze_instance(self) -> None:
                object.__setattr__(self, "_Slotted__frozen", True)

            def __setattr__(self, name: str, value: object) -> None:
                if getattr(self, "_Slotted__frozen", False):
                    raise AttributeError("frozen")
                object.__setattr__(self, name, value)

        decorated = auto_freeze(Slotted)
        instance = decorated(42)

        with pytest.raises(AttributeError):
            instance._value = 99

    def test_when_freeze_instance_is_async_then_still_works(self) -> None:
        class AsyncFreeze:
            def __init__(self) -> None:
                pass

            async def freeze_instance(self) -> None:
                pass

            def freeze_attributes(self, attrs: list[str]) -> None:
                pass

        decorated = auto_freeze(AsyncFreeze)
        instance = decorated()
        # Just ensure no error during decoration/construction
        assert instance is not None
