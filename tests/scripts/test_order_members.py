# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from pathlib import Path

import libcst as cst
import pytest
from scripts.order_members import (
    ORDER_PRIORITY,
    ReorderClassMembers,
    classify_attribute,
    classify_member,
    get_attribute_name,
    has_decorator,
    is_docstring_stmt,
    main,
    reorder_file,
)


def _parse_member(code: str, member_index: int = 0) -> cst.CSTNode:
    tree = cst.parse_module(code)
    stmt = tree.body[0]
    assert isinstance(stmt, cst.ClassDef)
    return stmt.body.body[member_index]


def _parse_fn(code: str, member_index: int = 0) -> cst.FunctionDef:
    member = _parse_member(code, member_index)
    assert isinstance(member, cst.FunctionDef)
    return member


@pytest.mark.unit
class TestHasDecorator:
    def test_when_name_decorator_matches_then_returns_true(self) -> None:
        fn = _parse_fn("class Foo:\n    @property\n    def x(self): return 42\n")

        assert has_decorator(fn, "property") is True

    def test_when_attribute_decorator_matches_then_returns_true(self) -> None:
        fn = _parse_fn("class Foo:\n    @some.attr\n    def x(self): pass\n")

        assert has_decorator(fn, "attr") is True

    def test_when_no_decorator_then_returns_false(self) -> None:
        fn = _parse_fn("class Foo:\n    def x(self): pass\n")

        assert has_decorator(fn, "property") is False

    def test_when_wrong_name_then_returns_false(self) -> None:
        fn = _parse_fn("class Foo:\n    @classmethod\n    def x(cls): pass\n")

        assert has_decorator(fn, "property") is False


@pytest.mark.unit
class TestIsDocstringStmt:
    def test_when_string_literal_then_returns_true(self) -> None:
        member = _parse_member('class Foo:\n    """Docstring."""\n')

        assert is_docstring_stmt(member) is True

    def test_when_non_string_expression_then_returns_false(self) -> None:
        member = _parse_member("class Foo:\n    x = 1\n")

        assert is_docstring_stmt(member) is False

    def test_when_non_simple_statement_then_returns_false(self) -> None:
        tree = cst.parse_module("class Foo:\n    pass\n")
        class_def = tree.body[0]
        assert isinstance(class_def, cst.ClassDef)

        assert is_docstring_stmt(class_def) is False


@pytest.mark.unit
class TestGetAttributeName:
    def test_when_annotated_assignment_then_returns_name(self) -> None:
        member = _parse_member("class Foo:\n    x: int = 1\n")

        result = get_attribute_name(member)

        assert result == "x"

    def test_when_regular_assignment_then_returns_name(self) -> None:
        member = _parse_member("class Foo:\n    x = 1\n")

        result = get_attribute_name(member)

        assert result == "x"

    def test_when_non_assignment_then_returns_none(self) -> None:
        member = _parse_member("class Foo:\n    pass\n")

        result = get_attribute_name(member)

        assert result is None


@pytest.mark.unit
class TestClassifyAttribute:
    @pytest.mark.parametrize(
        "name,expected",
        [
            pytest.param("MAX_SIZE", "class_constant", id="all_caps_with_underscore"),
            pytest.param("DEFAULT", "class_constant", id="all_caps_long"),
            pytest.param("A", "class_variable", id="single_uppercase"),
            pytest.param("x", "class_variable", id="lowercase_public"),
            pytest.param("_x", "protected_class_var", id="single_underscore_prefix"),
            pytest.param("__x", "private_class_var", id="double_underscore_prefix"),
            pytest.param("__dunder__", "protected_class_var", id="dunder_name"),
            pytest.param("A_B", "class_constant", id="caps_with_underscore_short"),
        ],
    )
    def test_classify_attribute(self, name: str, expected: str) -> None:
        assert classify_attribute(name) == expected


@pytest.mark.unit
class TestClassifyMember:
    @pytest.mark.parametrize(
        "code,expected_priority",
        [
            pytest.param(
                'class Foo:\n    """Docstring."""\n',
                ORDER_PRIORITY.index("docstring"),
                id="docstring",
            ),
            pytest.param(
                "class Foo:\n    MAX_SIZE = 100\n",
                ORDER_PRIORITY.index("class_constant"),
                id="class_constant",
            ),
            pytest.param(
                "class Foo:\n    x = 1\n",
                ORDER_PRIORITY.index("class_variable"),
                id="class_variable",
            ),
            pytest.param(
                "class Foo:\n    _x = 1\n",
                ORDER_PRIORITY.index("protected_class_var"),
                id="protected_class_var",
            ),
            pytest.param(
                "class Foo:\n    __x = 1\n",
                ORDER_PRIORITY.index("private_class_var"),
                id="private_class_var",
            ),
            pytest.param(
                "class Foo:\n    def __new__(cls): pass\n",
                ORDER_PRIORITY.index("__new__"),
                id="new",
            ),
            pytest.param(
                "class Foo:\n    def __init__(self): pass\n",
                ORDER_PRIORITY.index("__init__"),
                id="init",
            ),
            pytest.param(
                "class Foo:\n    @property\n    def x(self): return 42\n",
                ORDER_PRIORITY.index("property"),
                id="property",
            ),
            pytest.param(
                "class Foo:\n    def __repr__(self): return ''\n",
                ORDER_PRIORITY.index("dunder"),
                id="dunder",
            ),
            pytest.param(
                "class Foo:\n    @classmethod\n    def create(cls): return cls()\n",
                ORDER_PRIORITY.index("classmethod"),
                id="classmethod",
            ),
            pytest.param(
                "class Foo:\n    @staticmethod\n    def helper(): pass\n",
                ORDER_PRIORITY.index("staticmethod"),
                id="staticmethod",
            ),
            pytest.param(
                "class Foo:\n    def public_method(self): pass\n",
                ORDER_PRIORITY.index("public_method"),
                id="public_method",
            ),
            pytest.param(
                "class Foo:\n    def _protected(self): pass\n",
                ORDER_PRIORITY.index("protected_method"),
                id="protected_method",
            ),
            pytest.param(
                "class Foo:\n    def __private(self): pass\n",
                ORDER_PRIORITY.index("private_method"),
                id="private_method",
            ),
            pytest.param(
                "class Foo:\n    pass\n",
                ORDER_PRIORITY.index("other"),
                id="other",
            ),
        ],
    )
    def test_classify_member(self, code: str, expected_priority: int) -> None:
        member = _parse_member(code, 0)

        priority, _ = classify_member(member, 0)

        assert priority == expected_priority

    def test_when_index_preserved_then_stable_sort(self) -> None:
        members = [
            _parse_member("class Foo:\n    def a(self): pass\n    def b(self): pass\n", 0),
            _parse_member("class Foo:\n    def a(self): pass\n    def b(self): pass\n", 1),
        ]

        p0, i0 = classify_member(members[0], 0)
        p1, i1 = classify_member(members[1], 1)

        assert p0 == p1
        assert i0 < i1

    def test_when_classmethod_on_protected_then_classmethod_priority(self) -> None:
        member = _parse_member(
            "class Foo:\n    @classmethod\n    def _protected_cls(cls): pass\n", 0
        )

        priority, _ = classify_member(member, 0)

        assert priority == ORDER_PRIORITY.index("classmethod")

    def test_when_staticmethod_on_protected_then_staticmethod_priority(self) -> None:
        member = _parse_member(
            "class Foo:\n    @staticmethod\n    def _protected_static(): pass\n", 0
        )

        priority, _ = classify_member(member, 0)

        assert priority == ORDER_PRIORITY.index("staticmethod")


@pytest.mark.unit
class TestReorderFile:
    def test_when_out_of_order_then_reorders(self, tmp_path: Path) -> None:
        file = tmp_path / "test.py"
        file.write_text("""class Foo:
    def bar(self):
        pass
    MAX_SIZE = 100
    def __init__(self):
        pass
""")

        result = reorder_file(file)

        assert result is True
        content = file.read_text()
        max_pos = content.index("MAX_SIZE")
        init_pos = content.index("__init__")
        bar_pos = content.index("bar")
        assert max_pos < init_pos < bar_pos

    def test_when_already_ordered_then_no_change(self, tmp_path: Path) -> None:
        original = """class Foo:
    MAX_SIZE = 100
    def __init__(self):
        pass
    def bar(self):
        pass
"""
        file = tmp_path / "test.py"
        file.write_text(original)

        result = reorder_file(file)

        assert result is False
        assert file.read_text() == original

    def test_when_syntax_error_then_returns_false(self, tmp_path: Path) -> None:
        file = tmp_path / "test.py"
        file.write_text("this is not valid python {{{")

        result = reorder_file(file)

        assert result is False

    def test_when_file_not_found_then_returns_false(self, tmp_path: Path) -> None:
        file = tmp_path / "nonexistent.py"

        result = reorder_file(file)

        assert result is False


@pytest.mark.unit
class TestReorderClassMembers:
    def test_when_empty_body_then_returns_unchanged(self) -> None:
        cls = cst.ClassDef(
            name=cst.Name("Foo"),
            body=cst.IndentedBlock(body=[]),
            decorators=[],
        )
        transformer = ReorderClassMembers()

        result = transformer.leave_ClassDef(cls, cls)

        assert result is cls


@pytest.mark.unit
class TestMain:
    def test_when_file_provided_then_processes_it(self, tmp_path: Path) -> None:
        file = tmp_path / "test.py"
        file.write_text("""class Foo:
    def bar(self):
        pass
    MAX_SIZE = 100
""")

        result = main([str(file)])

        assert result == 0
        content = file.read_text()
        assert content.index("MAX_SIZE") < content.index("bar")

    def test_when_directory_provided_then_processes_recursively(
        self, tmp_path: Path
    ) -> None:
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "a.py").write_text("class Foo:\n    pass\n")

        result = main([str(sub)])

        assert result == 0

    def test_when_no_matching_files_then_returns_zero(self) -> None:
        result = main(["/nonexistent/path"])

        assert result == 0

    def test_when_no_argv_then_uses_default_paths(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def _noop_rglob(self: Path, pattern: str) -> list[Path]:
            return []

        monkeypatch.setattr(Path, "rglob", _noop_rglob)

        result = main([])

        assert result == 0


@pytest.mark.unit
class TestMainBlock:
    def test_when_run_as_main_then_executes(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import sys

        script = (
            Path(__file__).resolve().parent.parent.parent
            / "scripts"
            / "order_members.py"
        )
        test_file = tmp_path / "test.py"
        test_file.write_text("class Foo:\n    pass\n")
        monkeypatch.setattr(sys, "argv", ["order_members.py", str(test_file)])

        code = script.read_text(encoding="utf-8")
        with pytest.raises(SystemExit):
            exec(compile(code, str(script), "exec"), {"__name__": "__main__"})
