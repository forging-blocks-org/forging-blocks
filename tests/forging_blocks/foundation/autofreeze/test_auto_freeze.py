# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
"""Tests for the auto_freeze decorator."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from forging_blocks.foundation.autofreeze.auto_freeze import (
    _AUTO_FREEZE_MARKER,
    _AutoFreezeDecorator,
    auto_freeze,
)

# ---------------------------------------------------------------------------
# Test helpers — lightweight classes that implement SupportsAutoFreeze
# protocol via MagicMock so every call is observable.
# ---------------------------------------------------------------------------


def _make_protocol_class(
    *,
    should_freeze: bool = True,
    with_freeze_attrs: bool = True,
) -> type:
    """Create a class that implements SupportsAutoFreeze with mock tracking."""
    namespace: dict[str, Any] = {
        "should_use_internal_freezing": classmethod(
            MagicMock(return_value=should_freeze)
        ),
        "freeze_instance": MagicMock(),
        "unfreeze_instance": MagicMock(),
    }
    if with_freeze_attrs:
        namespace["freeze_attributes"] = MagicMock()
    return type("ProtocolClass", (), namespace)


def _make_minimal_class() -> type:
    """Create a class with only the three required protocol methods."""
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
            @classmethod
            def should_use_internal_freezing(cls) -> bool:
                return True

            def unfreeze_instance(self) -> None:
                pass

        with pytest.raises(TypeError, match="does not implement SupportsAutoFreeze"):
            _AutoFreezeDecorator._validate_protocol(Incomplete)

    def test_when_missing_should_use_internal_freezing_then_raises_typeerror(self) -> None:
        class Incomplete:
            def freeze_instance(self) -> None:
                pass

            def unfreeze_instance(self) -> None:
                pass

        with pytest.raises(TypeError, match="does not implement SupportsAutoFreeze"):
            _AutoFreezeDecorator._validate_protocol(Incomplete)

    def test_when_missing_unfreeze_instance_then_raises_typeerror(self) -> None:
        class Incomplete:
            @classmethod
            def should_use_internal_freezing(cls) -> bool:
                return True

            def freeze_instance(self) -> None:
                pass

        with pytest.raises(TypeError, match="does not implement SupportsAutoFreeze"):
            _AutoFreezeDecorator._validate_protocol(Incomplete)

    def test_when_missing_multiple_methods_then_lists_all_missing(self) -> None:
        class Empty:
            pass

        with pytest.raises(TypeError) as exc_info:
            _AutoFreezeDecorator._validate_protocol(Empty)

        message = str(exc_info.value)
        assert "should_use_internal_freezing" in message
        assert "freeze_instance" in message
        assert "unfreeze_instance" in message

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

    def test_when_used_without_parentheses_then_cls_is_decorated_directly(self) -> None:
        cls = _make_minimal_class()
        decorated = auto_freeze(cls)
        assert decorated is cls
        assert hasattr(decorated.__init__, _AUTO_FREEZE_MARKER)

    def test_when_used_with_parentheses_no_attrs_then_returns_callable(self) -> None:
        decorator = auto_freeze()
        assert callable(decorator)
        assert not hasattr(decorator, _AUTO_FREEZE_MARKER)

    def test_when_used_with_parentheses_and_attrs_then_returns_callable(self) -> None:
        decorator = auto_freeze(attrs=["_id"])
        assert callable(decorator)

    # -- Freezing behaviour -------------------------------------------------

    def test_when_attrs_none_then_freezes_full_instance(self) -> None:
        cls = _make_protocol_class(should_freeze=True, with_freeze_attrs=True)
        decorated = auto_freeze(cls)
        decorated()
        cls.freeze_instance.assert_called_once()  # type: ignore[attr-defined]
        cls.freeze_attributes.assert_not_called()  # type: ignore[attr-defined]

    def test_when_attrs_specified_then_freezes_only_those_attributes(self) -> None:
        cls = _make_protocol_class(should_freeze=True, with_freeze_attrs=True)
        decorated = auto_freeze(cls, attrs=["_x"])
        decorated()
        cls.freeze_attributes.assert_called_once_with(["_x"])  # type: ignore[attr-defined]
        cls.freeze_instance.assert_not_called()  # type: ignore[attr-defined]

    def test_when_attrs_empty_sequence_then_freezes_no_attributes(self) -> None:
        cls = _make_protocol_class(should_freeze=True, with_freeze_attrs=True)
        decorated = auto_freeze(cls, attrs=[])
        decorated()
        cls.freeze_attributes.assert_called_once_with([])  # type: ignore[attr-defined]

    def test_when_should_use_internal_freezing_returns_false_then_no_freeze(self) -> None:
        cls = _make_protocol_class(should_freeze=False, with_freeze_attrs=True)
        decorated = auto_freeze(cls)
        decorated()
        cls.freeze_instance.assert_not_called()  # type: ignore[attr-defined]
        cls.freeze_attributes.assert_not_called()  # type: ignore[attr-defined]

    def test_when_should_use_internal_freezing_returns_true_then_freeze_called(self) -> None:
        cls = _make_protocol_class(should_freeze=True, with_freeze_attrs=True)
        decorated = auto_freeze(cls)
        decorated()
        cls.freeze_instance.assert_called_once()  # type: ignore[attr-defined]


    # -- Idempotency --------------------------------------------------------

    def test_when_applied_twice_then_second_call_is_noop(self) -> None:
        cls = _make_minimal_class()
        first = auto_freeze(cls)
        wrapped_init_id = id(first.__init__)
        second = auto_freeze(first)
        assert second is first
        assert id(second.__init__) == wrapped_init_id

    # -- Protocol validation at decoration time ----------------------------

    def test_when_class_missing_protocol_then_raises_typeerror_at_decoration(self) -> None:
        class Invalid:
            pass
        with pytest.raises(TypeError, match="does not implement SupportsAutoFreeze"):
            auto_freeze(Invalid)

    # -- Init wrapping ------------------------------------------------------

    def test_when_instance_created_then_original_init_still_runs(self) -> None:
        class Tracked:
            @classmethod
            def should_use_internal_freezing(cls) -> bool:
                return True

            def freeze_instance(self) -> None:
                pass

            def unfreeze_instance(self) -> None:
                pass

            def __init__(self) -> None:
                self.init_was_called = True  # type: ignore[attr-defined]

        decorated = auto_freeze(Tracked)
        instance = decorated()
        assert instance.init_was_called is True  # type: ignore[attr-defined]

    def test_when_init_takes_args_then_args_are_forwarded(self) -> None:
        class ArgChecker:
            @classmethod
            def should_use_internal_freezing(cls) -> bool:
                return True

            def freeze_instance(self) -> None:
                pass

            def unfreeze_instance(self) -> None:
                pass

            def __init__(self, a: int, b: str, *, c: bool = False) -> None:
                self.a = a  # type: ignore[attr-defined]
                self.b = b  # type: ignore[attr-defined]
                self.c = c  # type: ignore[attr-defined]

        decorated = auto_freeze(ArgChecker)
        instance = decorated(42, "hello", c=True)
        assert instance.a == 42  # type: ignore[attr-defined]
        assert instance.b == "hello"  # type: ignore[attr-defined]
        assert instance.c is True  # type: ignore[attr-defined]

    def test_when_init_takes_no_args_then_instance_created(self) -> None:
        cls = _make_minimal_class()
        decorated = auto_freeze(cls)
        instance = decorated()
        assert isinstance(instance, cls)


    # -- Metadata preservation ----------------------------------------------

    def test_functools_wraps_preserves_dunder_attrs(self) -> None:
        class Documented:
            @classmethod
            def should_use_internal_freezing(cls) -> bool:
                return True

            def freeze_instance(self) -> None:
                pass

            def unfreeze_instance(self) -> None:
                pass

            def __init__(self, value: int) -> None:
                """Original docstring."""
                self.value = value  # type: ignore[attr-defined]

        decorated = auto_freeze(Documented)
        assert decorated.__init__.__name__ == "__init__"  # type: ignore[operator]
        assert decorated.__init__.__doc__ == "Original docstring."  # type: ignore[operator]
        assert decorated.__init__.__wrapped__ is not None  # type: ignore[operator]

    def test_when_wrapped_then_marker_set_on_init(self) -> None:
        cls = _make_minimal_class()
        decorated = auto_freeze(cls)
        assert hasattr(decorated.__init__, _AUTO_FREEZE_MARKER)

    # -- Freeze-after-init ordering ----------------------------------------

    def test_freeze_happens_after_init(self) -> None:
        call_record: list[str] = []

        class Ordered:
            @classmethod
            def should_use_internal_freezing(cls) -> bool:
                return True

            def freeze_instance(self) -> None:
                call_record.append("freeze")

            def unfreeze_instance(self) -> None:
                pass

            def __init__(self) -> None:
                call_record.append("init")

        decorated = auto_freeze(Ordered)
        decorated()
        assert call_record == ["init", "freeze"]

    # -- Inheritance / subclass interaction --------------------------------

    def test_subclass_inheriting_protocol_can_be_decorated(self) -> None:
        class Base:
            @classmethod
            def should_use_internal_freezing(cls) -> bool:
                return True

            def freeze_instance(self) -> None:
                pass

            def unfreeze_instance(self) -> None:
                pass

        class Child(Base):
            pass

        decorated = auto_freeze(Child)
        instance = decorated()
        assert isinstance(instance, Child)

    # -- Attrs specified but class lacks freeze_attributes -----------------

    def test_attrs_specified_class_lacks_freeze_attributes_raises_at_runtime(self) -> None:
        """When attrs is given but the class lacks freeze_attributes,
        decoration succeeds (protocol only checks the 3 required methods)
        but instantiation raises AttributeError."""
        class NoFreezeAttrs:
            @classmethod
            def should_use_internal_freezing(cls) -> bool:
                return True

            def freeze_instance(self) -> None:
                pass

            def unfreeze_instance(self) -> None:
                pass
            # freeze_attributes is intentionally missing

        decorated = auto_freeze(NoFreezeAttrs, attrs=["_x"])
        with pytest.raises(AttributeError):
            decorated()
