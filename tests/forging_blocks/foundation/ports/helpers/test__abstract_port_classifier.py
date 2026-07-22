"""Tests for the AbstractPortClassifier helper."""

import pytest

from forging_blocks.foundation.ports.helpers._abstract_port_classifier import (
    AbstractPortClassifier,
)


@pytest.mark.unit
class TestAbstractPortClassifier:
    def test_returns_true_for_abstract_class(self) -> None:
        """Returns True when the class has __abstractmethods__."""

        from abc import ABC, abstractmethod

        class AbstractTarget(ABC):
            @abstractmethod
            def do_it(self) -> None: ...

        classifier = AbstractPortClassifier(AbstractTarget)
        assert classifier.is_abstract() is True

    def test_returns_false_for_concrete_class(self) -> None:
        """Returns False when the class is concrete."""

        class ConcreteTarget: ...

        classifier = AbstractPortClassifier(ConcreteTarget)
        assert classifier.is_abstract() is False
