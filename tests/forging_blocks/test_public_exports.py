"""Tests for supported public package facades."""

import importlib
from collections.abc import Iterable
from typing import cast

import pytest


@pytest.mark.unit
class TestPublicExports:
    @pytest.mark.parametrize(
        ("module_name", "symbol_names"),
        [
            ("forging_blocks", ("__version__",)),
            ("forging_blocks.foundation", ("Debuggable",)),
            ("forging_blocks.application", ("TransactionError",)),
            (
                "forging_blocks.application.ports",
                ("AuthorizationPort", "ValidationPort"),
            ),
        ],
    )
    def test_facade_exports_include_supported_symbols(
        self,
        module_name: str,
        symbol_names: Iterable[str],
    ) -> None:
        module = importlib.import_module(module_name)
        exports = cast(list[str], getattr(module, "__all__"))

        for symbol_name in symbol_names:
            assert symbol_name in exports
            assert hasattr(module, symbol_name)

    @pytest.mark.parametrize(
        ("facade_name", "module_name", "symbol_name"),
        [
            ("foundation", "forging_blocks.foundation.debuggable", "Debuggable"),
            (
                "application",
                "forging_blocks.application.errors.transaction_error",
                "TransactionError",
            ),
            (
                "application.ports",
                "forging_blocks.application.ports.inbound.authorization_port",
                "AuthorizationPort",
            ),
            (
                "application.ports",
                "forging_blocks.application.ports.inbound.validation_port",
                "ValidationPort",
            ),
        ],
    )
    def test_facade_export_is_the_canonical_symbol(
        self,
        facade_name: str,
        module_name: str,
        symbol_name: str,
    ) -> None:
        facade = importlib.import_module(f"forging_blocks.{facade_name}")
        source = importlib.import_module(module_name)

        assert getattr(facade, symbol_name) is getattr(source, symbol_name)

    def test_root_public_manifest_contains_only_version(self) -> None:
        import forging_blocks

        exports = cast(list[str], getattr(forging_blocks, "__all__"))

        assert exports == ["__version__"]
