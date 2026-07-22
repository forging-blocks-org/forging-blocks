"""Structural subtype checking for ``__subclasshook__`` consumers."""


def check_methods(subclass: type, *method_names: str) -> bool:
    """Return ``True`` when *subclass* has all the named callable attributes."""
    return all(callable(getattr(subclass, name, None)) for name in method_names)
