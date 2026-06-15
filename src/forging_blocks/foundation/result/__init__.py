"""Result type — a disciplined alternative to raising exceptions.

Modeled after Rust's ``Result`` enum and the ``Either`` monad from functional
programming (think ``Either`` in Scala or Haskell), the Result type makes
errors a first-class part of your return type.  Instead of scattering
try/except blocks through your code, you compose operations with
`Result.map`, `Result.flat_map`, and
`Result.map_error`.

Quick start:

    ```python
    from forging_blocks.foundation.result import Ok, Err

    Ok(42).map(lambda x: x + 1)  # -> Ok(43)

    Err("boom").map(lambda x: x + 1)  # no-op — error short-circuits -> Err("boom")
    ```
"""

from .err import Err
from .ok import Ok
from .result import Result

__all__ = ["Err", "Ok", "Result"]
