"""The `auto_freeze` decorator enforces immutability after `__init__` completes.

## Usage

=== "Bare decorator"
    ```python
    from forging_blocks.foundation.autofreeze import auto_freeze

    @auto_freeze
    class Settings:
        def __init__(self, host: str) -> None:
            self.host = host

    s = Settings("localhost")
    s.host = "other"  # Raises CantModifyImmutableAttributeError
    ```

=== "Selective freeze"
    ```python
    from forging_blocks.foundation.autofreeze import auto_freeze

    @auto_freeze(attrs=["_id"])
    class User:
        def __init__(self, user_id: str, name: str) -> None:
            self._id = user_id  # frozen
            self._name = name   # mutable
    ```

## Generated members

|Member|Description|
|---|---|
|`__setattr__` override|Blocks mutation of frozen attributes after `__init__` returns|
