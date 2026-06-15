"""Protocol for classes that support the auto-freeze mechanism."""

from typing import Protocol, Sequence


class SupportsAutoFreeze(Protocol):  # pragma: no cover
    """Contract for classes compatible with the @auto_freeze decorator.

    Implementers must provide methods to transition instances to an immutable
    state. The @auto_freeze decorator calls these methods based on class
    configuration.

    **Traditional class** — the simplest use case: a plain Python class
    that becomes immutable after ``__init__``:

    ```python
    from forging_blocks.foundation.autofreeze import auto_freeze
    from forging_blocks.foundation.errors import (
        CantModifyImmutableAttributeError,
    )


    @auto_freeze
    class Money:
        def __init__(self, amount: int, currency: str) -> None:
            if amount < 0:
                raise ValueError("Amount cannot be negative")
            self._amount = amount
            self._currency = currency

        def freeze_instance(self) -> None:
            object.__setattr__(self, "_Money__frozen", True)

        def __setattr__(self, name: str, value: object) -> None:
            if getattr(self, "_Money__frozen", False):
                raise CantModifyImmutableAttributeError(
                    class_name=self.__class__.__name__,
                    attribute_name=name,
                )
            object.__setattr__(self, name, value)
    ```

    **Regular dataclass** — ``@auto_freeze`` adds post-init immutability
    to a dataclass that would otherwise allow mutation:

    ```python
    from dataclasses import dataclass

    from forging_blocks.foundation.autofreeze import auto_freeze
    from forging_blocks.foundation.errors import (
        CantModifyImmutableAttributeError,
    )


    @auto_freeze
    @dataclass
    class Point:
        x: float
        y: float

        def freeze_instance(self) -> None:
            object.__setattr__(self, "_Point__frozen", True)

        def __setattr__(self, name: str, value: object) -> None:
            if getattr(self, "_Point__frozen", False):
                raise CantModifyImmutableAttributeError(
                    class_name=self.__class__.__name__,
                    attribute_name=name,
                )
            object.__setattr__(self, name, value)
    ```

    **Selective freezing (Entities)** — freeze only specific attributes
    (e.g., identity fields) while keeping others mutable:

    ```python
    from forging_blocks.foundation.autofreeze import auto_freeze
    from forging_blocks.foundation.errors import (
        CantModifyImmutableAttributeError,
    )


    @auto_freeze(attrs=["_user_id", "_email"])
    class User:
        def __init__(self, user_id: str, email: str, name: str) -> None:
            self._user_id = user_id
            self._email = email
            self._name = name

        def freeze_attributes(self, attrs: Sequence[str]) -> None:
            frozen_attrs = getattr(self, "_User__frozen_attrs", set())
            frozen_attrs.update(attrs)
            object.__setattr__(self, "_User__frozen_attrs", frozen_attrs)

        def __setattr__(self, name: str, value: object) -> None:
            frozen_attrs = getattr(self, "_User__frozen_attrs", set())
            if name in frozen_attrs:
                raise CantModifyImmutableAttributeError(
                    class_name=self.__class__.__name__,
                    attribute_name=name,
                )
            object.__setattr__(self, name, value)
    ```
    """

    def freeze_instance(self) -> None:
        """Transition the instance into an immutable state.

        Called automatically by @auto_freeze after __init__ completes
        (when used without the attrs parameter).

        Responsibilities:
            - Mark the instance as frozen.
            - Prevent future attribute modifications.
            - Raise CantModifyImmutableAttributeError on __setattr__.

        Notes:
            - Implementation details are class-specific.
            - May use internal flags or other mechanisms.
        """
        ...

    def freeze_attributes(self, attrs: Sequence[str]) -> None:
        """Selectively freeze specific attributes.

        Optional method for classes that support partial freezing.
        If not implemented, freeze_instance() is called instead.

        Args:
            attrs: Attribute names to freeze (e.g., ["_id"]).

        Notes:
            - Useful for Entities where only identity should be immutable.
            - Default behavior (if not overridden): freeze_instance().
        """
        ...
