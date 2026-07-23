"""The `auto_hash` decorator generates `__hash__` for class instances.

Does **not** generate ``__eq__`` or apply ``auto_freeze``. Combine with
`auto_eq` for explicit equality,
and `auto_freeze` for immutability.

## Usage

=== "Bare decorator"
    ```python
    from forging_blocks.foundation.autohash import auto_hash

    @auto_hash
    class Point:
        __slots__ = ("x", "y")

        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    p1 = Point(1, 2)
    p2 = Point(1, 2)
    assert hash(p1) == hash(p2)
    ```

=== "With parameters"
    ```python
    from forging_blocks.foundation.autohash import auto_hash

    @auto_hash(fields=["x"])
    class Point:
        __slots__ = ("x", "y")

        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    p1 = Point(1, 2)
    p2 = Point(1, 999)
    assert hash(p1) == hash(p2)
    ```

## Generated members

|Member|Description|
|---|---|
|`__hash__`|Hash computed from the selected fields (mutable values converted to hashable equivalents)|
|`__auto_hash_fields__`|Tuple of field names used in hashing|
