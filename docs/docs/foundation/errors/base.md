# Base

This module provides the foundational error classes used across the Building Blocks framework.

It defines structured, debuggable, and composable error types that can be raised,
caught, and combined in a uniform way throughout all architectural layers.

Classes
--------

Error:
    Base class for all structured errors in the system. Inherits from
    `Exception` and `Debuggable`, allowing it to be raised and logged like
    a standard exception while carrying structured metadata.

NoneNotAllowedError
    Specialized `Error` indicating that a `None` value was provided where it
    is not allowed.

FieldErrors
    Represents validation or constraint errors associated with a single field.
    Provides iterable access to individual `Error` instances for that field.

CombinedErrors
    Aggregates multiple `Error` (or subclass) instances into one. Useful for
    collecting and raising multiple failures together (e.g., validation errors).

Notes:
-----
- All errors defined here are part of the *foundation* module and can be
  safely reused by higher components present in layer, if you have layer defined.
- Each error supports a detailed `as_debug_string()` method for rich diagnostic output.

::: building_blocks.foundation.errors.base
    options:
      show_source: true
      show_root_heading: true
