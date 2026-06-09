#!/usr/bin/env python3
"""Demo: ValueObject subclasses inherit auto-freeze with zero freeze-related code."""

from __future__ import annotations

from forging_blocks.foundation.errors.cant_modify_immutable_attribute_error import (
    CantModifyImmutableAttributeError,
)
from forging_blocks.foundation.value_object import ValueObject


class Email(ValueObject[str]):
    """Zero freeze code — no @auto_freeze, no freeze_instance, nothing."""

    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        super().__init__()
        if "@" not in value:
            raise ValueError("Invalid email format")
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @property
    def _equality_components(self) -> tuple[str]:
        return (self._value,)


class AbstractIntermediate(ValueObject[str]):
    """Abstract classes stay unfrozen."""

    __slots__ = ()

    @property
    def _equality_components(self) -> tuple[str]:
        return (self.value,)  # type: ignore[attr-defined]


class ConcreteLeaf(AbstractIntermediate):
    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        super().__init__()
        self._value = value

    @property
    def value(self) -> str:
        return self._value


def main() -> None:
    email = Email("user@example.com")

    print("1. Frozen after init:")
    try:
        email._value = "hacked@example.com"  # type: ignore[misc]
        print("   FAIL")
    except CantModifyImmutableAttributeError:
        print("   OK CantModifyImmutableAttributeError raised")

    print("\n2. Freeze methods inherited from ValueObject, not Email:")
    for m in ("freeze_instance", "unfreeze_instance", "should_use_internal_freezing"):
        owner = getattr(Email, m).__qualname__.split(".")[0]
        in_email = m in Email.__dict__
        print(f"   {m}: owned by {owner} | in Email.__dict__? {in_email}")

    print("\n3. Unfreeze -> mutate -> freeze (all inherited):")
    email.unfreeze_instance()
    email._value = "mutated@example.com"  # type: ignore[misc]
    email.freeze_instance()
    try:
        email._value = "nope@example.com"  # type: ignore[misc]
        print("   FAIL")
    except CantModifyImmutableAttributeError:
        print("   OK mutated, re-froze, can't mutate again")

    print("\n4. should_use_internal_freezing():")
    print(f"   ValueObject      -> {ValueObject.should_use_internal_freezing()} (abstract)")
    print(f"   Email            -> {Email.should_use_internal_freezing()} (concrete)")
    print(f"   AbstractIntermed -> {AbstractIntermediate.should_use_internal_freezing()} (abstract)")
    print(f"   ConcreteLeaf     -> {ConcreteLeaf.should_use_internal_freezing()} (concrete)")

    print("\n5. Abstract intermediate cannot be instantiated:")
    try:
        AbstractIntermediate()  # type: ignore[abstract]
        print("   FAIL")
    except TypeError:
        print("   OK TypeError (abstract class)")

    leaf = ConcreteLeaf("test")
    try:
        leaf._value = "nope"  # type: ignore[misc]
        print("   FAIL")
    except CantModifyImmutableAttributeError:
        print("   OK ConcreteLeaf frozen after init")

    print("\nAll checks passed - subclasses need ZERO freeze code.")


if __name__ == "__main__":
    main()
