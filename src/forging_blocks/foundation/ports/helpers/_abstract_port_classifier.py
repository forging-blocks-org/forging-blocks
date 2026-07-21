"""Classification of port types as abstract or concrete.

Used during ``__init_subclass__`` validation to skip abstract
intermediate classes such as ``UseCasePort`` or ``CommandHandlerPort``.
"""


class AbstractPortClassifier:
    """Determines whether a port class is abstract."""

    def __init__(self, cls: type) -> None:
        self._cls = cls

    def is_abstract(self) -> bool:
        """Return ``True`` when the class has unimplemented abstract methods."""
        abstract_methods: frozenset[object] = getattr(self._cls, "__abstractmethods__", frozenset())
        return bool(abstract_methods)
