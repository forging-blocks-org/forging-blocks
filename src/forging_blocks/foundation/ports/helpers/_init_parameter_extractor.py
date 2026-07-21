"""Extract annotated ``__init__`` parameters from a class.

Uses ``get_type_hints`` to resolve stringified annotations produced by
``from __future__ import annotations``.
"""

from typing import get_type_hints


class InitParameterExtractor:
    """Extracts the annotated ``__init__`` parameters from a class."""

    def __init__(self, cls: type) -> None:
        self._cls = cls

    def extract(self) -> dict[str, type]:
        """Extract annotated parameters, excluding ``self`` and ``return``.

        Returns an empty dict when annotation resolution fails so that
        unresolvable forward references degrade gracefully.
        """
        try:
            hints = get_type_hints(self._cls.__init__, include_extras=False)
        except (TypeError, NameError):
            return {}
        hints.pop("return", None)
        return hints
