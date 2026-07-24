"""Tests for validate_docstring_imports in the autodoc generator."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.generate_autodoc_pages import validate_docstring_imports


@pytest.mark.unit
class TestValidateDocstringImports:
    def test_when_unused_import_then_returns_warning(self, tmp_path: Path) -> None:
        src = tmp_path / "mod.py"
        src.write_text(
            '"""Module docstring.\n'
            "\n"
            "Example:\n"
            "    ```python\n"
            "    from foo import bar\n"
            "    print(1)\n"
            "    ```\n"
            '"""\n'
        )
        result = validate_docstring_imports(src)
        assert len(result) == 1
        assert "unused import 'bar'" in result[0]

    def test_when_all_imports_used_then_returns_empty(self, tmp_path: Path) -> None:
        src = tmp_path / "mod.py"
        src.write_text(
            '"""Module docstring.\n'
            "\n"
            "Example:\n"
            "    ```python\n"
            "    from foo import bar\n"
            "    print(bar)\n"
            "    ```\n"
            '"""\n'
        )
        result = validate_docstring_imports(src)
        assert result == []

    def test_when_import_as_alias_used_then_returns_empty(self, tmp_path: Path) -> None:
        src = tmp_path / "mod.py"
        src.write_text(
            '"""Module docstring.\n'
            "\n"
            "Example:\n"
            "    ```python\n"
            "    from foo import bar as baz\n"
            "    print(baz)\n"
            "    ```\n"
            '"""\n'
        )
        result = validate_docstring_imports(src)
        assert result == []

    def test_when_module_import_used_as_attr_then_returns_empty(self, tmp_path: Path) -> None:
        src = tmp_path / "mod.py"
        src.write_text(
            '"""Module docstring.\n'
            "\n"
            "Example:\n"
            "    ```python\n"
            "    import foo\n"
            "    foo.bar()\n"
            "    ```\n"
            '"""\n'
        )
        result = validate_docstring_imports(src)
        assert result == []

    def test_when_no_docstring_then_returns_empty(self, tmp_path: Path) -> None:
        src = tmp_path / "mod.py"
        src.write_text("x = 1\n")
        result = validate_docstring_imports(src)
        assert result == []

    def test_when_no_python_block_then_returns_empty(self, tmp_path: Path) -> None:
        src = tmp_path / "mod.py"
        src.write_text('"""Has docstring but no code block."""\n')
        result = validate_docstring_imports(src)
        assert result == []

    def test_when_syntax_error_in_block_then_skipped(self, tmp_path: Path) -> None:
        src = tmp_path / "mod.py"
        src.write_text(
            '"""Module docstring.\n'
            "\n"
            "Example:\n"
            "    ```python\n"
            "    this is not valid python\n"
            "    ```\n"
            '"""\n'
        )
        result = validate_docstring_imports(src)
        assert result == []

    def test_when_multiple_docstrings_then_checks_all(self, tmp_path: Path) -> None:
        src = tmp_path / "mod.py"
        src.write_text(
            '"""Module docstring.\n'
            "\n"
            "Example:\n"
            "    ```python\n"
            "    from foo import bar\n"
            "    print(1)\n"
            "    ```\n"
            '"""\n'
            "\n"
            "\n"
            "class Foo:\n"
            '    """Class docstring.\n'
            "\n"
            "    Example:\n"
            "        ```python\n"
            "        from baz import qux\n"
            "        print(1)\n"
            "        ```\n"
            '    """\n'
            "    pass\n"
        )
        result = validate_docstring_imports(src)
        assert len(result) == 2
        assert "unused import 'bar'" in result[0]
        assert "unused import 'qux'" in result[1]
