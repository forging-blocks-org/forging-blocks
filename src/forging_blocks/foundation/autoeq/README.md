"""The `auto_eq` decorator generates `__eq__` for class instances.

Generates equality based on class fields but does **not** generate
`__hash__`. Combine with [auto_hash][] when hashability is needed.

## Usage

=== "Bare decorator"
    ```python
    from dataclasses import dataclass
    from forging_blocks.foundation.autoeq import auto_eq

    @auto_eq
    @dataclass
    class Point:
        x: int
        y: int

    assert Point(1, 2) == Point(1, 2)
    ```

=== "With parameters"
    ```python
    from dataclasses import dataclass
    from forging_blocks.foundation.autoeq import auto_eq

    @auto_eq(fields=["x"])
    @dataclass
    class Point:
        x: int
        y: int

    assert Point(1, 2) == Point(1, 999)
    ```

## Generated members

|Member|Description|
|---|---|
|`__eq__`|Structural equality on selected fields; type-strict (`type(self) is type(other)`)|
|`__auto_eq_fields__`|Tuple of field names used in equality|
