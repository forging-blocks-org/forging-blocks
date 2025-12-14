# Getting Started

This guide walks through a small, complete example to help you get started with ForgingBlocks.

The focus is on **explicit outcomes** and **clear boundaries**, not on frameworks or infrastructure.

---

## Parsing input with Result

```python
from forging_blocks.foundation import Result, Ok, Err


def parse_int(value: str) -> Result[int, str]:
    try:
        return Ok(int(value))
    except ValueError:
        return Err(f"invalid integer: {value!r}")
```

### Using the function

```python
from forging_blocks.foundation import Ok, Err

result = parse_int("42")

match result:
    case Ok(number):
        print(f"Parsed number: {number}")
    case Err(error):
        print(f"Error: {error}")
```
