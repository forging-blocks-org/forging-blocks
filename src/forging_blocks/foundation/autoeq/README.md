"""The `auto_eq` decorator generates `__eq__` for class instances.

Generates equality based on class fields but does **not** generate
`__hash__`. Combine with [auto_hash][] when hashability is needed.

## Usage

=== "Bare decorator"
    ```python
    from forging_blocks.foundation.autoeq import auto_eq

    @auto_eq
    class Point:
        __slots__ = ("x", "y")

        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    assert Point(1, 2) == Point(1, 2)
    ```

=== "With parameters"
    ```python
    from forging_blocks.foundation.autoeq import auto_eq

    @auto_eq(fields=["x"])
    class Point:
        __slots__ = ("x", "y")

        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    assert Point(1, 2) == Point(1, 999)
    ```

## Generated members

|Member|Description|
|---|---|
|`__eq__`|Structural equality on selected fields; type-strict (`type(self) is type(other)`)|
|`__auto_eq_fields__`|Tuple of field names used in equality|
